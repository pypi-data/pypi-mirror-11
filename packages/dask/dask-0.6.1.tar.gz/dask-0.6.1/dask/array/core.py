from __future__ import absolute_import, division, print_function

import operator
from operator import add, getitem
import inspect
from numbers import Number
from collections import Iterable, MutableMapping
from bisect import bisect
from itertools import product, count
from collections import Iterator
from functools import partial, wraps

from toolz.curried import (pipe, partition, concat, unique, pluck, join, first,
                           memoize, map, groupby, valmap, accumulate, merge,
                           curry, reduce, interleave, sliding_window, partial)
import numpy as np

from threading import Lock
from . import chunk
from .slicing import slice_array
from . import numpy_compat
from ..utils import deepmap, ignoring, repr_long_list, concrete, is_integer
from ..compatibility import unicode, long
from .. import threaded, core
from ..context import _globals


names = ('x_%d' % i for i in count(1))
tokens = ('-%d' % i for i in count(1))


def getarray(a, b, lock=None):
    """ Mimics getitem but includes call to np.asarray

    >>> getarray([1, 2, 3, 4, 5], slice(1, 4))
    array([2, 3, 4])
    """
    if isinstance(b, tuple) and any(x is None for x in b):
        b2 = tuple(x for x in b if x is not None)
        b3 = tuple(None if x is None else slice(None, None)
                    for x in b
                    if not isinstance(x, (int, long)))
        return getarray(a, b2, lock)[b3]

    if lock:
        lock.acquire()
    try:
        c = a[b]
        if type(c) != np.ndarray:
            c = np.asarray(c)
    finally:
        if lock:
            lock.release()
    return c


from .optimization import optimize


def slices_from_chunks(chunks):
    """ Translate chunks tuple to a set of slices in product order

    >>> slices_from_chunks(((2, 2), (3, 3, 3)))  # doctest: +NORMALIZE_WHITESPACE
     [(slice(0, 2, None), slice(0, 3, None)),
      (slice(0, 2, None), slice(3, 6, None)),
      (slice(0, 2, None), slice(6, 9, None)),
      (slice(2, 4, None), slice(0, 3, None)),
      (slice(2, 4, None), slice(3, 6, None)),
      (slice(2, 4, None), slice(6, 9, None))]
    """
    cumdims = [list(accumulate(add, (0,) + bds[:-1])) for bds in chunks]
    shapes = product(*chunks)
    starts = product(*cumdims)
    return [tuple(slice(s, s+dim) for s, dim in zip(start, shape))
                for start, shape in zip(starts, shapes)]


def getem(arr, chunks, shape=None):
    """ Dask getting various chunks from an array-like

    >>> getem('X', chunks=(2, 3), shape=(4, 6))  # doctest: +SKIP
    {('X', 0, 0): (getarray, 'X', (slice(0, 2), slice(0, 3))),
     ('X', 1, 0): (getarray, 'X', (slice(2, 4), slice(0, 3))),
     ('X', 1, 1): (getarray, 'X', (slice(2, 4), slice(3, 6))),
     ('X', 0, 1): (getarray, 'X', (slice(0, 2), slice(3, 6)))}

    >>> getem('X', chunks=((2, 2), (3, 3)))  # doctest: +SKIP
    {('X', 0, 0): (getarray, 'X', (slice(0, 2), slice(0, 3))),
     ('X', 1, 0): (getarray, 'X', (slice(2, 4), slice(0, 3))),
     ('X', 1, 1): (getarray, 'X', (slice(2, 4), slice(3, 6))),
     ('X', 0, 1): (getarray, 'X', (slice(0, 2), slice(3, 6)))}
    """
    chunks = normalize_chunks(chunks, shape)

    keys = list(product([arr], *[range(len(bds)) for bds in chunks]))

    values = [(getarray, arr, x) for x in slices_from_chunks(chunks)]

    return dict(zip(keys, values))


def dotmany(A, B, leftfunc=None, rightfunc=None, **kwargs):
    """ Dot product of many aligned chunks

    >>> x = np.array([[1, 2], [1, 2]])
    >>> y = np.array([[10, 20], [10, 20]])
    >>> dotmany([x, x, x], [y, y, y])
    array([[ 90, 180],
           [ 90, 180]])

    Optionally pass in functions to apply to the left and right chunks

    >>> dotmany([x, x, x], [y, y, y], rightfunc=np.transpose)
    array([[150, 150],
           [150, 150]])
    """
    if leftfunc:
        A = map(leftfunc, A)
    if rightfunc:
        B = map(rightfunc, B)
    return sum(map(partial(np.dot, **kwargs), A, B))


def lol_tuples(head, ind, values, dummies):
    """ List of list of tuple keys

    Parameters
    ----------

    head : tuple
        The known tuple so far
    ind : Iterable
        An iterable of indices not yet covered
    values : dict
        Known values for non-dummy indices
    dummies : dict
        Ranges of values for dummy indices

    Examples
    --------

    >>> lol_tuples(('x',), 'ij', {'i': 1, 'j': 0}, {})
    ('x', 1, 0)

    >>> lol_tuples(('x',), 'ij', {'i': 1}, {'j': range(3)})
    [('x', 1, 0), ('x', 1, 1), ('x', 1, 2)]

    >>> lol_tuples(('x',), 'ij', {'i': 1}, {'j': range(3)})
    [('x', 1, 0), ('x', 1, 1), ('x', 1, 2)]

    >>> lol_tuples(('x',), 'ijk', {'i': 1}, {'j': [0, 1, 2], 'k': [0, 1]}) # doctest: +NORMALIZE_WHITESPACE
    [[('x', 1, 0, 0), ('x', 1, 0, 1)],
     [('x', 1, 1, 0), ('x', 1, 1, 1)],
     [('x', 1, 2, 0), ('x', 1, 2, 1)]]
    """
    if not ind:
        return head
    if ind[0] not in dummies:
        return lol_tuples(head + (values[ind[0]],), ind[1:], values, dummies)
    else:
        return [lol_tuples(head + (v,), ind[1:], values, dummies)
                for v in dummies[ind[0]]]


def zero_broadcast_dimensions(lol, nblocks):
    """

    >>> lol = [('x', 1, 0), ('x', 1, 1), ('x', 1, 2)]
    >>> nblocks = (4, 1, 2)  # note singleton dimension in second place
    >>> lol = [[('x', 1, 0, 0), ('x', 1, 0, 1)],
    ...        [('x', 1, 1, 0), ('x', 1, 1, 1)],
    ...        [('x', 1, 2, 0), ('x', 1, 2, 1)]]

    >>> zero_broadcast_dimensions(lol, nblocks)  # doctest: +NORMALIZE_WHITESPACE
    [[('x', 1, 0, 0), ('x', 1, 0, 1)],
     [('x', 1, 0, 0), ('x', 1, 0, 1)],
     [('x', 1, 0, 0), ('x', 1, 0, 1)]]

    See Also
    --------

    lol_tuples
    """
    f = lambda t: (t[0],) + tuple(0 if d == 1 else i for i, d in zip(t[1:], nblocks))
    return deepmap(f, lol)


def broadcast_dimensions(argpairs, numblocks, sentinels=(1, (1,))):
    """ Find block dimensions from arguments

    Parameters
    ----------

    argpairs: iterable
        name, ijk index pairs
    numblocks: dict
        maps {name: number of blocks}
    sentinels: iterable (optional)
        values for singleton dimensions

    Examples
    --------

    >>> argpairs = [('x', 'ij'), ('y', 'ji')]
    >>> numblocks = {'x': (2, 3), 'y': (3, 2)}
    >>> broadcast_dimensions(argpairs, numblocks)
    {'i': 2, 'j': 3}

    Supports numpy broadcasting rules

    >>> argpairs = [('x', 'ij'), ('y', 'ij')]
    >>> numblocks = {'x': (2, 1), 'y': (1, 3)}
    >>> broadcast_dimensions(argpairs, numblocks)
    {'i': 2, 'j': 3}

    Works in other contexts too

    >>> argpairs = [('x', 'ij'), ('y', 'ij')]
    >>> d = {'x': ('Hello', 1), 'y': (1, (2, 3))}
    >>> broadcast_dimensions(argpairs, d)
    {'i': 'Hello', 'j': (2, 3)}
    """
    # List like [('i', 2), ('j', 1), ('i', 1), ('j', 2)]
    L = concat([zip(inds, dims)
                    for (x, inds), (x, dims)
                    in join(first, argpairs, first, numblocks.items())])
    g = groupby(0, L)
    g = dict((k, set([d for i, d in v])) for k, v in g.items())

    g2 = dict((k, v - set(sentinels) if len(v) > 1 else v) for k, v in g.items())

    if g2 and not set(map(len, g2.values())) == set([1]):
        raise ValueError("Shapes do not align %s" % g)

    return valmap(first, g2)


def top(func, output, out_indices, *arrind_pairs, **kwargs):
    """ Tensor operation

    Applies a function, ``func``, across blocks from many different input
    dasks.  We arrange the pattern with which those blocks interact with sets
    of matching indices.  E.g.

        top(func, 'z', 'i', 'x', 'i', 'y', 'i')

    yield an embarassingly parallel communication pattern and is read as

        z_i = func(x_i, y_i)

    More complex patterns may emerge, including multiple indices

        top(func, 'z', 'ij', 'x', 'ij', 'y', 'ji')

        $$ z_{ij} = func(x_{ij}, y_{ji}) $$

    Indices missing in the output but present in the inputs results in many
    inputs being sent to one function (see examples).

    Examples
    --------

    Simple embarassing map operation

    >>> inc = lambda x: x + 1
    >>> top(inc, 'z', 'ij', 'x', 'ij', numblocks={'x': (2, 2)})  # doctest: +SKIP
    {('z', 0, 0): (inc, ('x', 0, 0)),
     ('z', 0, 1): (inc, ('x', 0, 1)),
     ('z', 1, 0): (inc, ('x', 1, 0)),
     ('z', 1, 1): (inc, ('x', 1, 1))}

    Simple operation on two datasets

    >>> add = lambda x, y: x + y
    >>> top(add, 'z', 'ij', 'x', 'ij', 'y', 'ij', numblocks={'x': (2, 2),
    ...                                                      'y': (2, 2)})  # doctest: +SKIP
    {('z', 0, 0): (add, ('x', 0, 0), ('y', 0, 0)),
     ('z', 0, 1): (add, ('x', 0, 1), ('y', 0, 1)),
     ('z', 1, 0): (add, ('x', 1, 0), ('y', 1, 0)),
     ('z', 1, 1): (add, ('x', 1, 1), ('y', 1, 1))}

    Operation that flips one of the datasets

    >>> addT = lambda x, y: x + y.T  # Transpose each chunk
    >>> #                                        z_ij ~ x_ij y_ji
    >>> #               ..         ..         .. notice swap
    >>> top(addT, 'z', 'ij', 'x', 'ij', 'y', 'ji', numblocks={'x': (2, 2),
    ...                                                       'y': (2, 2)})  # doctest: +SKIP
    {('z', 0, 0): (add, ('x', 0, 0), ('y', 0, 0)),
     ('z', 0, 1): (add, ('x', 0, 1), ('y', 1, 0)),
     ('z', 1, 0): (add, ('x', 1, 0), ('y', 0, 1)),
     ('z', 1, 1): (add, ('x', 1, 1), ('y', 1, 1))}

    Dot product with contraction over ``j`` index.  Yields list arguments

    >>> top(dotmany, 'z', 'ik', 'x', 'ij', 'y', 'jk', numblocks={'x': (2, 2),
    ...                                                          'y': (2, 2)})  # doctest: +SKIP
    {('z', 0, 0): (dotmany, [('x', 0, 0), ('x', 0, 1)],
                            [('y', 0, 0), ('y', 1, 0)]),
     ('z', 0, 1): (dotmany, [('x', 0, 0), ('x', 0, 1)],
                            [('y', 0, 1), ('y', 1, 1)]),
     ('z', 1, 0): (dotmany, [('x', 1, 0), ('x', 1, 1)],
                            [('y', 0, 0), ('y', 1, 0)]),
     ('z', 1, 1): (dotmany, [('x', 1, 0), ('x', 1, 1)],
                            [('y', 0, 1), ('y', 1, 1)])}

    Supports Broadcasting rules

    >>> top(add, 'z', 'ij', 'x', 'ij', 'y', 'ij', numblocks={'x': (1, 2),
    ...                                                      'y': (2, 2)})  # doctest: +SKIP
    {('z', 0, 0): (add, ('x', 0, 0), ('y', 0, 0)),
     ('z', 0, 1): (add, ('x', 0, 1), ('y', 0, 1)),
     ('z', 1, 0): (add, ('x', 0, 0), ('y', 1, 0)),
     ('z', 1, 1): (add, ('x', 0, 1), ('y', 1, 1))}
    """
    numblocks = kwargs['numblocks']
    argpairs = list(partition(2, arrind_pairs))

    assert set(numblocks) == set(pluck(0, argpairs))

    all_indices = pipe(argpairs, pluck(1), concat, set)
    dummy_indices = all_indices - set(out_indices)

    # Dictionary mapping {i: 3, j: 4, ...} for i, j, ... the dimensions
    dims = broadcast_dimensions(argpairs, numblocks)

    # (0, 0), (0, 1), (0, 2), (1, 0), ...
    keytups = list(product(*[range(dims[i]) for i in out_indices]))
    # {i: 0, j: 0}, {i: 0, j: 1}, ...
    keydicts = [dict(zip(out_indices, tup)) for tup in keytups]

    # {j: [1, 2, 3], ...}  For j a dummy index of dimension 3
    dummies = dict((i, list(range(dims[i]))) for i in dummy_indices)

    # Create argument lists
    valtups = []
    for kd in keydicts:
        args = []
        for arg, ind in argpairs:
            tups = lol_tuples((arg,), ind, kd, dummies)
            tups2 = zero_broadcast_dimensions(tups, numblocks[arg])
            args.append(tups2)
        valtups.append(tuple(args))

    # Add heads to tuples
    keys = [(output,) + kt for kt in keytups]
    vals = [(func,) + vt for vt in valtups]

    return dict(zip(keys, vals))


def _concatenate2(arrays, axes=[]):
    """ Recursively Concatenate nested lists of arrays along axes

    Each entry in axes corresponds to each level of the nested list.  The
    length of axes should correspond to the level of nesting of arrays.

    >>> x = np.array([[1, 2], [3, 4]])
    >>> _concatenate2([x, x], axes=[0])
    array([[1, 2],
           [3, 4],
           [1, 2],
           [3, 4]])

    >>> _concatenate2([x, x], axes=[1])
    array([[1, 2, 1, 2],
           [3, 4, 3, 4]])

    >>> _concatenate2([[x, x], [x, x]], axes=[0, 1])
    array([[1, 2, 1, 2],
           [3, 4, 3, 4],
           [1, 2, 1, 2],
           [3, 4, 3, 4]])

    Supports Iterators
    >>> _concatenate2(iter([x, x]), axes=[1])
    array([[1, 2, 1, 2],
           [3, 4, 3, 4]])
    """
    if isinstance(arrays, Iterator):
        arrays = list(arrays)
    if len(axes) > 1:
        arrays = [_concatenate2(a, axes=axes[1:]) for a in arrays]
    return np.concatenate(arrays, axis=axes[0])


def map_blocks(func, *arrs, **kwargs):
    """ Map a function across all blocks of a dask array

    You must also specify the chunks of the resulting array.  If you don't then
    we assume that the resulting array has the same block structure as the
    input.

    >>> import dask.array as da
    >>> x = da.arange(6, chunks=3)

    >>> x.map_blocks(lambda x: x * 2).compute()
    array([ 0,  2,  4,  6,  8, 10])

    The ``da.map_blocks`` function can also accept multiple arrays

    >>> d = da.arange(5, chunks=2)
    >>> e = da.arange(5, chunks=2)

    >>> f = map_blocks(lambda a, b: a + b**2, d, e)
    >>> f.compute()
    array([ 0,  2,  6, 12, 20])

    If function changes shape of the blocks then please provide chunks
    explicitly.

    >>> y = x.map_blocks(lambda x: x[::2], chunks=((2, 2),))

    Your block function can learn where in the array it is if it supports a
    ``block_id`` keyword argument.  This will receive entries like (2, 0, 1),
    the position of the block in the dask array.

    >>> def func(block, block_id=None):
    ...     pass
    """
    if not callable(func):
        raise TypeError("First argument must be callable function, not %s\n"
                "Usage:   da.map_blocks(function, x)\n"
                "   or:   da.map_blocks(function, x, y, z)" %
                type(func).__name__)
    dtype = kwargs.get('dtype')
    assert all(isinstance(arr, Array) for arr in arrs)

    inds = [tuple(range(x.ndim))[::-1] for x in arrs]
    args = list(concat(zip(arrs, inds)))

    out_ind = tuple(range(max(x.ndim for x in arrs)))[::-1]

    result = atop(func, out_ind, *args, dtype=dtype)

    # If func has block_id as an argument then swap out func
    # for func with block_id partialed in
    try:
        spec = inspect.getargspec(func)
    except:
        spec = None
    if spec and 'block_id' in spec.args:
        for k in core.flatten(result._keys()):
            result.dask[k] = (partial(func, block_id=k[1:]),) + result.dask[k][1:]

    # Assert user specified chunks
    chunks = kwargs.get('chunks')
    if chunks is not None and chunks and not isinstance(chunks[0], tuple):
        chunks = tuple([nb * (bs,)
                        for nb, bs in zip(result.numblocks, chunks)])
    if chunks is not None:
        result._chunks = chunks

    return result


@wraps(np.squeeze)
def squeeze(a, axis=None):
    if axis is None:
        axis = tuple(i for i, d in enumerate(a.shape) if d == 1)
    b = a.map_blocks(partial(np.squeeze, axis=axis), dtype=a.dtype)
    chunks = tuple(bd for bd in b.chunks if bd != (1,))
    old_keys = list(product([b.name], *[range(len(bd)) for bd in b.chunks]))
    new_keys = list(product([b.name], *[range(len(bd)) for bd in chunks]))

    dsk = b.dask.copy()
    for o, n in zip(old_keys, new_keys):
        dsk[n] = dsk[o]
        del dsk[o]

    return Array(dsk, b.name, chunks, dtype=a.dtype)


def topk(k, x):
    """ The top k elements of an array

    Returns the k greatest elements of the array in sorted order.  Only works
    on arrays of a single dimension.

    >>> x = np.array([5, 1, 3, 6])
    >>> d = from_array(x, chunks=2)
    >>> d.topk(2).compute()
    array([6, 5])

    Runs in near linear time, returns all results in a single chunk so
    all k elements must fit in memory.
    """
    if x.ndim != 1:
        raise ValueError("Topk only works on arrays of one dimension")

    name = next(names)
    dsk = dict(((name, i), (chunk.topk, k, key))
                for i, key in enumerate(x._keys()))
    name2 = next(names)
    dsk[(name2, 0)] = (getitem,
                        (np.sort, (np.concatenate, (list, list(dsk)))),
                        slice(-1, -k - 1, -1))
    chunks = ((k,),)

    return Array(merge(dsk, x.dask), name2, chunks, dtype=x.dtype)


def compute(*args, **kwargs):
    """ Evaluate several dask arrays at once

    The result of this function is always a tuple of numpy arrays. To evaluate
    a single dask array into a numpy array, use ``myarray.compute()`` or simply
    ``np.array(myarray)``.

    Examples
    --------
    >>> import dask.array as da
    >>> d = da.ones((4, 4), chunks=(2, 2))
    >>> a = d + 1  # two different dask arrays
    >>> b = d + 2
    >>> A, B = da.compute(a, b)  # Compute both simultaneously
    """
    dsk = merge(*[arg.dask for arg in args])
    keys = [arg._keys() for arg in args]
    results = get(dsk, keys, **kwargs)

    results2 = tuple(concatenate3(x) if arg.shape else unpack_singleton(x)
                     for x, arg in zip(results, args))
    return results2


def store(sources, targets, **kwargs):
    """ Store dask arrays in array-like objects, overwrite data in target

    This stores dask arrays into object that supports numpy-style setitem
    indexing.  It stores values chunk by chunk so that it does not have to
    fill up memory.  For best performance you can align the block size of
    the storage target with the block size of your array.

    If your data fits in memory then you may prefer calling
    ``np.array(myarray)`` instead.

    Parameters
    ----------

    sources: Array or iterable of Arrays
    targets: array-like or iterable of array-likes
        These should support setitem syntax ``target[10:20] = ...``

    Examples
    --------

    >>> x = ...  # doctest: +SKIP

    >>> import h5py  # doctest: +SKIP
    >>> f = h5py.File('myfile.hdf5')  # doctest: +SKIP
    >>> dset = f.create_dataset('/data', shape=x.shape,
    ...                                  chunks=x.chunks,
    ...                                  dtype='f8')  # doctest: +SKIP

    >>> store(x, dset)  # doctest: +SKIP

    Alternatively store many arrays at the same time

    >>> store([x, y, z], [dset1, dset2, dset3])  # doctest: +SKIP
    """
    if isinstance(sources, Array):
        sources = [sources]
        targets = [targets]

    if any(not isinstance(s, Array) for s in sources):
        raise ValueError("All sources must be dask array objects")

    if len(sources) != len(targets):
        raise ValueError("Different number of sources [%d] and targets [%d]"
                         % (len(sources), len(targets)))

    updates = [insert_to_ooc(tgt, src) for tgt, src in zip(targets, sources)]
    dsk = merge([src.dask for src in sources] + updates)
    keys = [key for u in updates for key in u]
    get(dsk, keys, **kwargs)


def blockdims_from_blockshape(shape, chunks):
    """

    >>> blockdims_from_blockshape((10, 10), (4, 3))
    ((4, 4, 2), (3, 3, 3, 1))
    """
    if chunks is None:
        raise TypeError("Must supply chunks= keyword argument")
    if shape is None:
        raise TypeError("Must supply shape= keyword argument")
    if not all(map(is_integer, chunks)):
        raise ValueError("chunks can only contain integers.")
    if not all(map(is_integer, shape)):
        raise ValueError("shape can only contain integers.")
    shape = map(int, shape)
    chunks = map(int, chunks)
    return tuple((bd,) * (d // bd) + ((d % bd,) if d % bd else ())
                              for d, bd in zip(shape, chunks))


class Array(object):
    """ Parallel Array

    Parameters
    ----------

    dask : dict
        Task dependency graph
    name : string
        Name of array in dask
    shape : tuple of ints
        Shape of the entire array
    chunks: iterable of tuples
        block sizes along each dimension
    """

    __slots__ = 'dask', 'name', '_chunks', '_dtype'

    def __init__(self, dask, name, chunks, dtype=None, shape=None):
        self.dask = dask
        self.name = name
        self._chunks = normalize_chunks(chunks, shape)
        if self._chunks is None:
            raise ValueError(chunks_none_error_message)
        if dtype is not None:
            dtype = np.dtype(dtype)
        self._dtype = dtype

    @property
    def _args(self):
        return (self.dask, self.name, self.chunks, self.dtype)

    @property
    def numblocks(self):
        return tuple(map(len, self.chunks))

    @property
    def shape(self):
        return tuple(map(sum, self.chunks))

    def _get_chunks(self):
        return self._chunks

    def _set_chunks(self, chunks):
        raise TypeError("Can not set chunks directly\n\n"
            "Please use the rechunk method instead:\n"
            "  x.rechunk(%s)" % str(chunks))

    chunks = property(_get_chunks, _set_chunks, "chunks property")

    def __len__(self):
        return sum(self.chunks[0])

    def _visualize(self, optimize_graph=False):
        from dask.dot import dot_graph
        if optimize_graph:
            return dot_graph(optimize(self.dask, self._keys()))
        else:
            return dot_graph(self.dask)

    @property
    @memoize(key=lambda args, kwargs: (id(args[0]), args[0].name, args[0].chunks))
    def dtype(self):
        if self._dtype is not None:
            return self._dtype
        if self.shape:
            return self[(0,) * self.ndim].compute().dtype
        else:
            return self.compute().dtype

    def __repr__(self):
        chunks = '(' + ', '.join(map(repr_long_list, self.chunks)) + ')'
        return ("dask.array<%s, shape=%s, chunks=%s, dtype=%s>" %
                (self.name, self.shape, chunks, self._dtype))

    @property
    def ndim(self):
        return len(self.shape)

    @property
    def size(self):
        """ Number of elements in array """
        return np.prod(self.shape)

    @property
    def nbytes(self):
        """ Number of bytes in array """
        return self.size * self.dtype.itemsize

    def _keys(self, *args):
        if self.ndim == 0:
            return [(self.name,)]
        ind = len(args)
        if ind + 1 == self.ndim:
            return [(self.name,) + args + (i,)
                        for i in range(self.numblocks[ind])]
        else:
            return [self._keys(*(args + (i,)))
                        for i in range(self.numblocks[ind])]

    def __array__(self, dtype=None, **kwargs):
        x = self.compute()
        if dtype and x.dtype != dtype:
            x = x.astype(dtype)
        if not isinstance(x, np.ndarray):
            x = np.array(x)
        return x

    @wraps(store)
    def store(self, target, **kwargs):
        return store([self], [target], **kwargs)

    def to_hdf5(self, filename, datapath, **kwargs):
        """ Store array in HDF5 file

        >>> x.to_hdf5('myfile.hdf5', '/x')  # doctest: +SKIP

        Optionally provide arguments as though to ``h5py.File.create_dataset``

        >>> x.to_hdf5('myfile.hdf5', '/x', compression='lzf', shuffle=True)  # doctest: +SKIP

        See also
        --------
        da.store
        h5py.File.create_dataset
        """
        return to_hdf5(filename, datapath, self, **kwargs)

    @wraps(compute)
    def compute(self, **kwargs):
        result, = compute(self, **kwargs)
        return result

    def cache(self, store=None, **kwargs):
        """ Evaluate and cache array

        Parameters
        ----------
        store: MutableMapping or ndarray-like
            Place to put computed and cached chunks
        kwargs:
            Keyword arguments to pass on to ``get`` function for scheduling

        This triggers evaluation and store the result in either

        1.  An ndarray object supporting setitem (see da.store)
        2.  A MutableMapping like a dict or chest

        It then returns a new dask array that points to this store.
        This returns a semantically equivalent dask array.

        >>> import dask.array as da
        >>> x = da.arange(5, chunks=2)
        >>> y = 2*x + 1
        >>> z = y.cache()  # triggers computation

        >>> y.compute()  # Does entire computation
        array([1, 3, 5, 7, 9])

        >>> z.compute()  # Just pulls from store
        array([1, 3, 5, 7, 9])

        You might base a cache off of an array like a numpy array or
        h5py.Dataset.

        >>> cache = np.empty(5, dtype=x.dtype)
        >>> z = y.cache(store=cache)
        >>> cache
        array([1, 3, 5, 7, 9])

        Or one might use a MutableMapping like a dict or chest

        >>> cache = dict()
        >>> z = y.cache(store=cache)
        >>> cache  # doctest: +SKIP
        {('x', 0): array([1, 3]),
         ('x', 1): array([5, 7]),
         ('x', 2): array([9])}
        """
        if store is not None and hasattr(store, 'shape'):
            self.store(store)
            return from_array(store, chunks=self.chunks)
        if store is None:
            try:
                from chest import Chest
                store = Chest()
            except ImportError:
                if self.nbytes <= 1e9:
                    store = dict()
                else:
                    raise ValueError("No out-of-core storage found."
                        "Either:\n"
                        "1. Install ``chest``, an out-of-core dictionary\n"
                        "2. Provide an on-disk array like an h5py.Dataset") # pragma: no cover
        if isinstance(store, MutableMapping):
            name = next(names)
            dsk = dict(((name, k[1:]), (operator.setitem, store, (tuple, list(k)), k))
                    for k in core.flatten(self._keys()))
            get(merge(dsk, self.dask), list(dsk.keys()), **kwargs)

            dsk2 = dict((k, (operator.getitem, store, (tuple, list(k))))
                        for k in store)
            return Array(dsk2, self.name, chunks=self.chunks, dtype=self._dtype)

    def __int__(self):
        return int(self.compute())
    def __bool__(self):
        return bool(self.compute())
    __nonzero__ = __bool__  # python 2
    def __float__(self):
        return float(self.compute())
    def __complex__(self):
        return complex(self.compute())

    def __getitem__(self, index):
        # Field access, e.g. x['a'] or x[['a', 'b']]
        if (isinstance(index, (str, unicode)) or
            (    isinstance(index, list)
            and all(isinstance(i, (str, unicode)) for i in index))):
            if self._dtype is not None and isinstance(index, (str, unicode)):
                dt = self._dtype[index]
            elif self._dtype is not None and isinstance(index, list):
                dt = np.dtype([(name, self._dtype[name]) for name in index])
            else:
                dt = None
            return elemwise(getarray, self, index, dtype=dt)

        # Slicing
        out = next(names)
        if not isinstance(index, tuple):
            index = (index,)

        if all(isinstance(i, slice) and i == slice(None) for i in index):
            return self

        dsk, chunks = slice_array(out, self.name, self.chunks, index)

        return Array(merge(self.dask, dsk), out, chunks, dtype=self._dtype)

    @wraps(np.dot)
    def dot(self, other):
        return tensordot(self, other, axes=((self.ndim-1,), (other.ndim-2,)))

    @property
    def T(self):
        return transpose(self)

    @wraps(np.transpose)
    def transpose(self, axes=None):
        return transpose(self, axes)

    @wraps(topk)
    def topk(self, k):
        return topk(k, self)

    def astype(self, dtype, **kwargs):
        """ Copy of the array, cast to a specified type """
        return elemwise(lambda x: x.astype(dtype, **kwargs), self, dtype=dtype)

    def __abs__(self):
        return elemwise(operator.abs, self)
    def __add__(self, other):
        return elemwise(operator.add, self, other)
    def __radd__(self, other):
        return elemwise(operator.add, other, self)
    def __and__(self, other):
        return elemwise(operator.and_, self, other)
    def __rand__(self, other):
        return elemwise(operator.and_, other, self)
    def __div__(self, other):
        return elemwise(operator.div, self, other)
    def __rdiv__(self, other):
        return elemwise(operator.div, other, self)
    def __eq__(self, other):
        return elemwise(operator.eq, self, other)
    def __gt__(self, other):
        return elemwise(operator.gt, self, other)
    def __ge__(self, other):
        return elemwise(operator.ge, self, other)
    def __invert__(self):
        return elemwise(operator.invert, self)
    def __lshift__(self, other):
        return elemwise(operator.lshift, self, other)
    def __rlshift__(self, other):
        return elemwise(operator.lshift, other, self)
    def __lt__(self, other):
        return elemwise(operator.lt, self, other)
    def __le__(self, other):
        return elemwise(operator.le, self, other)
    def __mod__(self, other):
        return elemwise(operator.mod, self, other)
    def __rmod__(self, other):
        return elemwise(operator.mod, other, self)
    def __mul__(self, other):
        return elemwise(operator.mul, self, other)
    def __rmul__(self, other):
        return elemwise(operator.mul, other, self)
    def __ne__(self, other):
        return elemwise(operator.ne, self, other)
    def __neg__(self):
        return elemwise(operator.neg, self)
    def __or__(self, other):
        return elemwise(operator.or_, self, other)
    def __pos__(self):
        return self
    def __ror__(self, other):
        return elemwise(operator.or_, other, self)
    def __pow__(self, other):
        return elemwise(operator.pow, self, other)
    def __rpow__(self, other):
        return elemwise(operator.pow, other, self)
    def __rshift__(self, other):
        return elemwise(operator.rshift, self, other)
    def __rrshift__(self, other):
        return elemwise(operator.rshift, other, self)
    def __sub__(self, other):
        return elemwise(operator.sub, self, other)
    def __rsub__(self, other):
        return elemwise(operator.sub, other, self)
    def __truediv__(self, other):
        return elemwise(operator.truediv, self, other)
    def __rtruediv__(self, other):
        return elemwise(operator.truediv, other, self)
    def __floordiv__(self, other):
        return elemwise(operator.floordiv, self, other)
    def __rfloordiv__(self, other):
        return elemwise(operator.floordiv, other, self)
    def __xor__(self, other):
        return elemwise(operator.xor, self, other)
    def __rxor__(self, other):
        return elemwise(operator.xor, other, self)

    @wraps(np.any)
    def any(self, axis=None, keepdims=False):
        from .reductions import any
        return any(self, axis=axis, keepdims=keepdims)

    @wraps(np.all)
    def all(self, axis=None, keepdims=False):
        from .reductions import all
        return all(self, axis=axis, keepdims=keepdims)

    @wraps(np.min)
    def min(self, axis=None, keepdims=False):
        from .reductions import min
        return min(self, axis=axis, keepdims=keepdims)

    @wraps(np.max)
    def max(self, axis=None, keepdims=False):
        from .reductions import max
        return max(self, axis=axis, keepdims=keepdims)

    @wraps(np.argmin)
    def argmin(self, axis=None):
        from .reductions import argmin
        return argmin(self, axis=axis)

    @wraps(np.argmax)
    def argmax(self, axis=None):
        from .reductions import argmax
        return argmax(self, axis=axis)

    @wraps(np.sum)
    def sum(self, axis=None, dtype=None, keepdims=False):
        from .reductions import sum
        return sum(self, axis=axis, dtype=dtype, keepdims=keepdims)

    @wraps(np.prod)
    def prod(self, axis=None, dtype=None, keepdims=False):
        from .reductions import prod
        return prod(self, axis=axis, dtype=dtype, keepdims=keepdims)

    @wraps(np.mean)
    def mean(self, axis=None, dtype=None, keepdims=False):
        from .reductions import mean
        return mean(self, axis=axis, dtype=dtype, keepdims=keepdims)

    @wraps(np.std)
    def std(self, axis=None, dtype=None, keepdims=False, ddof=0):
        from .reductions import std
        return std(self, axis=axis, dtype=dtype, keepdims=keepdims, ddof=ddof)

    @wraps(np.var)
    def var(self, axis=None, dtype=None, keepdims=False, ddof=0):
        from .reductions import var
        return var(self, axis=axis, dtype=dtype, keepdims=keepdims, ddof=ddof)

    def moment(self, order, axis=None, dtype=None, keepdims=False, ddof=0):
        """Calculate the nth centralized moment.

        Parameters
        ----------
        order : int
            Order of the moment that is returned, must be >= 2.
        axis : int, optional
            Axis along which the central moment is computed. The default is to
            compute the moment of the flattened array.
        dtype : data-type, optional
            Type to use in computing the moment. For arrays of integer type the
            default is float64; for arrays of float types it is the same as the
            array type.
        keepdims : bool, optional
            If this is set to True, the axes which are reduced are left in the
            result as dimensions with size one. With this option, the result
            will broadcast correctly against the original array.
        ddof : int, optional
            "Delta Degrees of Freedom": the divisor used in the calculation is
            N - ddof, where N represents the number of elements. By default
            ddof is zero.

        Returns
        -------
        moment : ndarray

        References
        ----------
        .. [1] Pebay, Philippe (2008), "Formulas for Robust, One-Pass Parallel
        Computation of Covariances and Arbitrary-Order Statistical Moments"
        (PDF), Technical Report SAND2008-6212, Sandia National Laboratories

        """

        from .reductions import moment
        return moment(self, order, axis=axis, dtype=dtype, keepdims=keepdims, ddof=ddof)

    def vnorm(self, ord=None, axis=None, keepdims=False):
        """ Vector norm """
        from .reductions import vnorm
        return vnorm(self, ord=ord, axis=axis, keepdims=keepdims)

    @wraps(map_blocks)
    def map_blocks(self, func, chunks=None, dtype=None):
        return map_blocks(func, self, chunks=chunks, dtype=dtype)

    def map_overlap(self, func, depth, boundary=None, trim=True, **kwargs):
        """ Map a function over blocks of the array with some overlap

        We share neighboring zones between blocks of the array, then map a
        function, then trim away the neighboring strips.

        Parameters
        ----------

        func: function
            The function to apply to each extended block
        depth: int, tuple, or dict
            The number of cells that each block should share with its neighbors
            If a tuple or dict this can be different per axis
        boundary: str
            how to handle the boundaries.  Values include 'reflect', 'periodic'
            or any constant value like 0 or np.nan
        trim: bool
            Whether or not to trim the excess after the map function.  Set this
            to false if your mapping function does this for you.
        **kwargs:
            Other keyword arguments valid in ``map_blocks``

        Examples
        --------

        >>> x = np.array([1, 1, 2, 3, 3, 3, 2, 1, 1])
        >>> x = from_array(x, chunks=5)
        >>> def derivative(x):
        ...     return x - np.roll(x, 1)

        >>> y = x.map_overlap(derivative, depth=1, boundary=0)
        >>> y.compute()
        array([ 1,  0,  1,  1,  0,  0, -1, -1,  0])
        """
        from .ghost import map_overlap
        return map_overlap(self, func, depth, boundary, trim, **kwargs)

    @wraps(squeeze)
    def squeeze(self):
        return squeeze(self)

    def rechunk(self, chunks):
        from .rechunk import rechunk
        return rechunk(self, chunks)


def normalize_chunks(chunks, shape=None):
    """ Normalize chunks to tuple of tuples

    >>> normalize_chunks((2, 2), shape=(5, 6))
    ((2, 2, 1), (2, 2, 2))

    >>> normalize_chunks(((2, 2, 1), (2, 2, 2)), shape=(4, 6))  # Idempotent
    ((2, 2, 1), (2, 2, 2))

    >>> normalize_chunks([[2, 2], [3, 3]])  # Cleans up lists to tuples
    ((2, 2), (3, 3))

    >>> normalize_chunks(10, shape=(30, 5))  # Supports integer inputs
    ((10, 10, 10), (5,))

    >>> normalize_chunks((), shape=(0, 0))  #  respects null dimensions
    ((), ())
    """
    if chunks is None:
        raise ValueError(chunks_none_error_message)
    if isinstance(chunks, list):
        chunks = tuple(chunks)
    if isinstance(chunks, Number):
        chunks = (chunks,) * len(shape)
    if not chunks and shape and all(s == 0 for s in shape):
        chunks = ((),) * len(shape)

    if shape is not None:
        chunks = tuple(c if c is not None else s for c, s in zip(chunks, shape))

    if chunks and shape is not None:
        chunks = sum((blockdims_from_blockshape((s,), (c,))
                      if not isinstance(c, (tuple, list)) else (c,)
                      for s, c in zip(shape, chunks)), ())

    return tuple(map(tuple, chunks))


def from_array(x, chunks, name=None, lock=False):
    """ Create dask array from something that looks like an array

    Input must have a ``.shape`` and support numpy-style slicing.

    The ``chunks`` argument must be one of the following forms:

    -   a blocksize like 1000
    -   a blockshape like (1000, 1000)
    -   explicit sizes of all blocks along all dimensions
        like ((1000, 1000, 500), (400, 400)).

    Examples
    --------

    >>> x = h5py.File('...')['/data/path']  # doctest: +SKIP
    >>> a = da.from_array(x, chunks=(1000, 1000))  # doctest: +SKIP

    If your underlying datastore does not support concurrent reads then include
    the ``lock=True`` keyword argument or ``lock=mylock`` if you want multiple
    arrays to coordinate around the same lock.

    >>> a = da.from_array(x, chunks=(1000, 1000), lock=True)  # doctest: +SKIP
    """
    chunks = normalize_chunks(chunks, x.shape)
    name = name or 'from-array' + next(tokens)
    dsk = getem(name, chunks)
    if lock is True:
        lock = Lock()
    if lock:
        dsk = dict((k, v + (lock,)) for k, v in dsk.items())
    return Array(merge({name: x}, dsk), name, chunks, dtype=x.dtype)


def from_func(func, shape, dtype=None, name=None, args=(), kwargs={}):
    """ Create dask array in a single block by calling a function

    Calling the provided function with func(*args, **kwargs) should return a
    NumPy array of the indicated shape and dtype.

    Example
    -------

    >>> a = from_func(np.arange, (3,), np.int64, args=(3,))
    >>> a.compute()
    array([0, 1, 2])

    This works particularly well when coupled with dask.array functions like
    concatenate and stack:

    >>> arrays = [from_func(np.array, (), args=(n,)) for n in range(5)]
    >>> stack(arrays).compute()
    array([0, 1, 2, 3, 4])
    """
    if args or kwargs:
        func = partial(func, *args, **kwargs)
    name = name or next(names)
    dsk = {(name,) + (0,) * len(shape): (func,)}
    chunks = tuple((i,) for i in shape)
    return Array(dsk, name, chunks, dtype)


def atop(func, out_ind, *args, **kwargs):
    """ Tensor operation: Generalized inner and outer products

    A broad class of blocked algorithms and patterns can be specified with a
    concise multi-index notation.  The ``atop`` function applies an in-memory
    function across multiple blocks of multiple inputs in a variety of ways.

    Parameters
    ----------
    func: callable
        Function to apply to individual tuples of blocks
    out_ind: iterable
        Block pattern of the output, something like 'ijk' or (1, 2, 3)
    *args: sequence of Array, index pairs
        Sequence like (x, 'ij', y, 'jk', z, 'i')

    This is best explained through example.  Consider the following examples:

    Examples
    --------

    2D embarassingly parallel operation from two arrays, x, and y.

    >>> z = atop(operator.add, 'ij', x, 'ij', y, 'ij')  # z = x + y  # doctest: +SKIP

    Outer product multiplying x by y, two 1-d vectors

    >>> z = atop(operator.mul, 'ij', x, 'i', y, 'j')  # doctest: +SKIP

    z = x.T

    >>> z = atop(np.transpose, 'ji', x, 'ij')  # doctest: +SKIP

    The transpose case above is illustrative because it does same transposition
    both on each in-memory block by calling ``np.transpose`` and on the order
    of the blocks themselves, by switching the order of the index ``ij -> ji``.

    We can compose these same patterns with more variables and more complex
    in-memory functions

    z = X + Y.T

    >>> z = atop(lambda x, y: x + y.T, 'ij', x, 'ij', y, 'ji')  # doctest: +SKIP

    Any index, like ``i`` missing from the output index is interpreted as a
    contraction (note that this differs from Einstein convention; repeated
    indices do not imply contraction.)  In the case of a contraction the passed
    function should expect an iterator of blocks on any array that holds that
    index.

    Inner product multiplying x by y, two 1-d vectors

    >>> def sequence_dot(x_blocks, y_blocks):
    ...     result = 0
    ...     for x, y in zip(x_blocks, y_blocks):
    ...         result += x.dot(y)
    ...     return result

    >>> z = atop(sequence_dot, '', x, 'i', y, 'i')  # doctest: +SKIP

    Many dask.array operations are special cases of atop.  These tensor
    operations cover a broad subset of NumPy and this function has been battle
    tested, supporting tricky concepts like broadcasting.

    See also:
        top - dict formulation of this function, contains most logic
    """
    out = kwargs.pop('name', None) or next(names)
    dtype = kwargs.pop('dtype', None)
    if kwargs:
        raise TypeError("%s does not take the following keyword arguments %s" %
            (func.__name__, str(sorted(kwargs.keys()))))
    arginds = list(partition(2, args)) # [x, ij, y, jk] -> [(x, ij), (y, jk)]
    numblocks = dict([(a.name, a.numblocks) for a, ind in arginds])
    argindsstr = list(concat([(a.name, ind) for a, ind in arginds]))

    dsk = top(func, out, out_ind, *argindsstr, numblocks=numblocks)

    # Dictionary mapping {i: 3, j: 4, ...} for i, j, ... the dimensions
    shapes = dict((a.name, a.shape) for a, _ in arginds)
    nameinds = [(a.name, i) for a, i in arginds]
    dims = broadcast_dimensions(nameinds, shapes)
    shape = tuple(dims[i] for i in out_ind)

    blockdim_dict = dict((a.name, a.chunks) for a, _ in arginds)
    chunkss = broadcast_dimensions(nameinds, blockdim_dict)
    chunks = tuple(chunkss[i] for i in out_ind)

    dsks = [a.dask for a, _ in arginds]
    return Array(merge(dsk, *dsks), out, chunks, dtype=dtype)


def get(dsk, keys, get=None, **kwargs):
    """ Specialized get function

    1. Handle inlining
    2. Use custom score function
    """
    get = get or _globals['get'] or threaded.get
    dsk2 = optimize(dsk, keys, **kwargs)
    return get(dsk2, keys, **kwargs)


def unpack_singleton(x):
    """

    >>> unpack_singleton([[[[1]]]])
    1
    >>> unpack_singleton(np.array(np.datetime64('2000-01-01')))
    array(datetime.date(2000, 1, 1), dtype='datetime64[D]')
    """
    while True:
        try:
            x = x[0]
        except (IndexError, TypeError, KeyError):
            break
    return x


stacked_names = ('stack-%d' % i for i in count(1))


def stack(seq, axis=0):
    """
    Stack arrays along a new axis

    Given a sequence of dask Arrays form a new dask Array by stacking them
    along a new dimension (axis=0 by default)

    Examples
    --------

    Create slices

    >>> import dask.array as da
    >>> import numpy as np

    >>> data = [from_array(np.ones((4, 4)), chunks=(2, 2))
    ...          for i in range(3)]

    >>> x = da.stack(data, axis=0)
    >>> x.shape
    (3, 4, 4)

    >>> da.stack(data, axis=1).shape
    (4, 3, 4)

    >>> da.stack(data, axis=-1).shape
    (4, 4, 3)

    Result is a new dask Array

    See Also
    --------
    concatenate
    """
    n = len(seq)
    ndim = len(seq[0].shape)
    if axis < 0:
        axis = ndim + axis + 1
    if axis > ndim:
        raise ValueError("Axis must not be greater than number of dimensions"
                "\nData has %d dimensions, but got axis=%d" % (ndim, axis))

    assert len(set(a.chunks for a in seq)) == 1  # same chunks
    shape = seq[0].shape[:axis] + (len(seq),) + seq[0].shape[axis:]
    chunks = (  seq[0].chunks[:axis]
              + ((1,) * n,)
              + seq[0].chunks[axis:])

    name = next(stacked_names)
    keys = list(product([name], *[range(len(bd)) for bd in chunks]))

    names = [a.name for a in seq]
    inputs = [(names[key[axis+1]],) + key[1:axis + 1] + key[axis + 2:]
                for key in keys]
    values = [(getarray, inp, (slice(None, None, None),) * axis
                           + (None,)
                           + (slice(None, None, None),) * (ndim - axis))
                for inp in inputs]

    dsk = dict(zip(keys, values))
    dsk2 = merge(dsk, *[a.dask for a in seq])

    if all(a._dtype is not None for a in seq):
        dt = reduce(np.promote_types, [a._dtype for a in seq])
    else:
        dt = None

    return Array(dsk2, name, chunks, dtype=dt)


concatenate_names = ('concatenate-%d' % i for i in count(1))


def concatenate(seq, axis=0):
    """
    Concatenate arrays along an existing axis

    Given a sequence of dask Arrays form a new dask Array by stacking them
    along an existing dimension (axis=0 by default)

    Examples
    --------

    Create slices

    >>> import dask.array as da
    >>> import numpy as np

    >>> data = [from_array(np.ones((4, 4)), chunks=(2, 2))
    ...          for i in range(3)]

    >>> x = da.concatenate(data, axis=0)
    >>> x.shape
    (12, 4)

    >>> da.concatenate(data, axis=1).shape
    (4, 12)

    Result is a new dask Array

    See Also
    --------
    stack
    """
    n = len(seq)
    ndim = len(seq[0].shape)
    if axis < 0:
        axis = ndim + axis
    if axis >= ndim:
        raise ValueError("Axis must be less than than number of dimensions"
                "\nData has %d dimensions, but got axis=%d" % (ndim, axis))

    bds = [a.chunks for a in seq]

    if not all(len(set(bds[i][j] for i in range(n))) == 1
            for j in range(len(bds[0])) if j != axis):
        raise ValueError("Block shapes do not align")

    shape = (seq[0].shape[:axis]
            + (sum(a.shape[axis] for a in seq),)
            + seq[0].shape[axis + 1:])
    chunks = (  seq[0].chunks[:axis]
              + (sum([bd[axis] for bd in bds], ()),)
              + seq[0].chunks[axis + 1:])

    name = next(concatenate_names)
    keys = list(product([name], *[range(len(bd)) for bd in chunks]))

    cum_dims = [0] + list(accumulate(add, [len(a.chunks[axis]) for a in seq]))
    names = [a.name for a in seq]
    values = [(names[bisect(cum_dims, key[axis + 1]) - 1],)
                + key[1:axis + 1]
                + (key[axis + 1] - cum_dims[bisect(cum_dims, key[axis+1]) - 1],)
                + key[axis + 2:]
                for key in keys]

    dsk = dict(zip(keys, values))
    dsk2 = merge(dsk, *[a.dask for a in seq])

    if all(a._dtype is not None for a in seq):
        dt = reduce(np.promote_types, [a._dtype for a in seq])
    else:
        dt = None

    return Array(dsk2, name, chunks, dtype=dt)


@wraps(np.take)
def take(a, indices, axis=0):
    if not -a.ndim <= axis < a.ndim:
        raise ValueError('axis=(%s) out of bounds' % axis)
    if axis < 0:
        axis += a.ndim
    if isinstance(a, np.ndarray) and isinstance(indices, Array):
        return _take_dask_array_from_numpy(a, indices, axis)
    else:
        return a[(slice(None),) * axis + (indices,)]


def _take_dask_array_from_numpy(a, indices, axis):
    assert isinstance(a, np.ndarray)
    assert isinstance(indices, Array)

    return indices.map_blocks(lambda block: np.take(a, block, axis),
                              chunks=indices.chunks,
                              dtype=a.dtype)

@wraps(np.transpose)
def transpose(a, axes=None):
    axes = axes or tuple(range(a.ndim))[::-1]
    return atop(partial(np.transpose, axes=axes),
                axes,
                a, tuple(range(a.ndim)), dtype=a._dtype)


@curry
def many(a, b, binop=None, reduction=None, **kwargs):
    """
    Apply binary operator to pairwise to sequences, then reduce.

    >>> many([1, 2, 3], [10, 20, 30], mul, sum)  # dot product
    140
    """
    return reduction(map(partial(binop, **kwargs), a, b))


alphabet = 'abcdefghijklmnopqrstuvwxyz'
ALPHABET = alphabet.upper()


@wraps(np.tensordot)
def tensordot(lhs, rhs, axes=2):
    if isinstance(axes, Iterable):
        left_axes, right_axes = axes
    else:
        left_axes = tuple(range(lhs.ndim - 1, lhs.ndim - axes - 1, -1))
        right_axes = tuple(range(0, axes))

    if isinstance(left_axes, int):
        left_axes = (left_axes,)
    if isinstance(right_axes, int):
        right_axes = (right_axes,)
    if isinstance(left_axes, list):
        left_axes = tuple(left_axes)
    if isinstance(right_axes, list):
        right_axes = tuple(right_axes)

    if len(left_axes) > 1:
        raise NotImplementedError("Simultaneous Contractions of multiple "
                "indices not yet supported")

    left_index = list(alphabet[:lhs.ndim])
    right_index = list(ALPHABET[:rhs.ndim])
    out_index = left_index + right_index
    for l, r in zip(left_axes, right_axes):
        out_index.remove(right_index[r])
        out_index.remove(left_index[l])
        right_index[r] = left_index[l]

    if lhs._dtype is not None and rhs._dtype is not None :
        dt = np.promote_types(lhs._dtype, rhs._dtype)
    else:
        dt = None

    func = many(binop=np.tensordot, reduction=sum,
                axes=(left_axes, right_axes))
    return atop(func,
                out_index,
                lhs, tuple(left_index),
                rhs, tuple(right_index), dtype=dt)


def insert_to_ooc(out, arr):
    lock = Lock()

    def store(x, index):
        with lock:
            out[index] = np.asanyarray(x)
        return None

    slices = slices_from_chunks(arr.chunks)

    name = 'store-%s' % arr.name
    dsk = dict(((name,) + t[1:], (store, t, slc))
                for t, slc in zip(core.flatten(arr._keys()), slices))
    return dsk


def partial_by_order(op, other):
    """

    >>> f = partial_by_order(add, [(1, 10)])
    >>> f(5)
    15
    """
    def f(*args):
        args2 = list(args)
        for i, arg in other:
            args2.insert(i, arg)
        return op(*args2)
    return f


def elemwise(op, *args, **kwargs):
    """ Apply elementwise function across arguments

    Respects broadcasting rules

    Examples
    --------
    >>> elemwise(add, x, y)  # doctest: +SKIP
    >>> elemwise(sin, x)  # doctest: +SKIP

    See also
    --------
    atop
    """
    if not set(['name', 'dtype']).issuperset(kwargs):
        raise TypeError("%s does not take the following keyword arguments %s" %
            (op.__name__, str(sorted(set(kwargs) - set(['name', 'dtype'])))))
    name = kwargs.get('name') or next(names)
    out_ndim = max(len(arg.shape) if isinstance(arg, Array) else 0
                   for arg in args)
    expr_inds = tuple(range(out_ndim))[::-1]

    arrays = [arg for arg in args if isinstance(arg, Array)]
    other = [(i, a) for i, a in enumerate(args) if not isinstance(a, Array)]
    if any(isinstance(arg, np.ndarray) for arg in args):
        raise NotImplementedError("Dask.array operations only work on dask "
                                  "arrays, not numpy arrays.")
    if 'dtype' in kwargs:
        dt = kwargs['dtype']
    elif not all(a._dtype is not None for a in arrays):
        dt = None
    else:

        vals = [np.empty((1,) * a.ndim, dtype=a.dtype)
                if hasattr(a, 'dtype') else a
                for a in args]
        try:
            dt = op(*vals).dtype
        except AttributeError:
            dt = None

    if other:
        op2 = partial_by_order(op, other)
    else:
        op2 = op

    return atop(op2, expr_inds,
                *concat((a, tuple(range(a.ndim)[::-1])) for a in arrays),
                dtype=dt, name=name)


def wrap_elemwise(func, **kwargs):
    """ Wrap up numpy function into dask.array """
    f = partial(elemwise, func, **kwargs)
    f.__doc__ = func.__doc__
    f.__name__ = func.__name__
    return f


# ufuncs, copied from this page:
# http://docs.scipy.org/doc/numpy/reference/ufuncs.html

# math operations
logaddexp = wrap_elemwise(np.logaddexp)
logaddexp2 = wrap_elemwise(np.logaddexp2)
conj = wrap_elemwise(np.conj)
exp = wrap_elemwise(np.exp)
log = wrap_elemwise(np.log)
log2 = wrap_elemwise(np.log2)
log10 = wrap_elemwise(np.log10)
log1p = wrap_elemwise(np.log1p)
expm1 = wrap_elemwise(np.expm1)
sqrt = wrap_elemwise(np.sqrt)
square = wrap_elemwise(np.square)

# trigonometric functions
sin = wrap_elemwise(np.sin)
cos = wrap_elemwise(np.cos)
tan = wrap_elemwise(np.tan)
arcsin = wrap_elemwise(np.arcsin)
arccos = wrap_elemwise(np.arccos)
arctan = wrap_elemwise(np.arctan)
arctan2 = wrap_elemwise(np.arctan2)
hypot = wrap_elemwise(np.hypot)
sinh = wrap_elemwise(np.sinh)
cosh = wrap_elemwise(np.cosh)
tanh = wrap_elemwise(np.tanh)
arcsinh = wrap_elemwise(np.arcsinh)
arccosh = wrap_elemwise(np.arccosh)
arctanh = wrap_elemwise(np.arctanh)
deg2rad = wrap_elemwise(np.deg2rad)
rad2deg = wrap_elemwise(np.rad2deg)

# comparison functions
logical_and = wrap_elemwise(np.logical_and, dtype='bool')
logical_or = wrap_elemwise(np.logical_or, dtype='bool')
logical_xor = wrap_elemwise(np.logical_xor, dtype='bool')
logical_not = wrap_elemwise(np.logical_not, dtype='bool')
maximum = wrap_elemwise(np.maximum)
minimum = wrap_elemwise(np.minimum)
fmax = wrap_elemwise(np.fmax)
fmin = wrap_elemwise(np.fmin)

# floating functions
isreal = wrap_elemwise(np.isreal, dtype='bool')
iscomplex = wrap_elemwise(np.iscomplex, dtype='bool')
isfinite = wrap_elemwise(np.isfinite, dtype='bool')
isinf = wrap_elemwise(np.isinf, dtype='bool')
isnan = wrap_elemwise(np.isnan, dtype='bool')
signbit = wrap_elemwise(np.signbit, dtype='bool')
copysign = wrap_elemwise(np.copysign)
nextafter = wrap_elemwise(np.nextafter)
# modf: see below
ldexp = wrap_elemwise(np.ldexp)
# frexp: see below
fmod = wrap_elemwise(np.fmod)
floor = wrap_elemwise(np.floor)
ceil = wrap_elemwise(np.ceil)
trunc = wrap_elemwise(np.trunc)

# more math routines, from this page:
# http://docs.scipy.org/doc/numpy/reference/routines.math.html
degrees = wrap_elemwise(np.degrees)
radians = wrap_elemwise(np.radians)

rint = wrap_elemwise(np.rint)
fix = wrap_elemwise(np.fix)

angle = wrap_elemwise(np.angle)
real = wrap_elemwise(np.real)
imag = wrap_elemwise(np.imag)

clip = wrap_elemwise(np.clip)
fabs = wrap_elemwise(np.fabs)
sign = wrap_elemwise(np.fabs)


def frexp(x):
    tmp = elemwise(np.frexp, x)
    left = next(names)
    right = next(names)
    ldsk = dict(((left,) + key[1:], (getitem, key, 0))
                for key in core.flatten(tmp._keys()))
    rdsk = dict(((right,) + key[1:], (getitem, key, 1))
                for key in core.flatten(tmp._keys()))

    if x._dtype is not None:
        a = np.empty((1,), dtype=x._dtype)
        l, r = np.frexp(a)
        ldt = l.dtype
        rdt = r.dtype
    else:
        ldt = None
        rdt = None

    L = Array(merge(tmp.dask, ldsk), left, chunks=tmp.chunks,
                dtype=ldt)

    R = Array(merge(tmp.dask, rdsk), right, chunks=tmp.chunks,
                dtype=rdt)

    return L, R

frexp.__doc__ = np.frexp


def modf(x):
    tmp = elemwise(np.modf, x)
    left = next(names)
    right = next(names)
    ldsk = dict(((left,) + key[1:], (getitem, key, 0))
                for key in core.flatten(tmp._keys()))
    rdsk = dict(((right,) + key[1:], (getitem, key, 1))
                for key in core.flatten(tmp._keys()))

    if x._dtype is not None:
        a = np.empty((1,), dtype=x._dtype)
        l, r = np.modf(a)
        ldt = l.dtype
        rdt = r.dtype
    else:
        ldt = None
        rdt = None

    L = Array(merge(tmp.dask, ldsk), left, chunks=tmp.chunks,
                dtype=ldt)

    R = Array(merge(tmp.dask, rdsk), right, chunks=tmp.chunks,
                dtype=rdt)

    return L, R

modf.__doc__ = np.modf


@wraps(np.around)
def around(x, decimals=0):
    return map_blocks(partial(np.around, decimals=decimals), x, dtype=x.dtype)


def isnull(values):
    """ pandas.isnull for dask arrays """
    import pandas as pd
    return elemwise(pd.isnull, values, dtype='bool')


def notnull(values):
    """ pandas.notnull for dask arrays """
    return ~isnull(values)


@wraps(numpy_compat.isclose)
def isclose(arr1, arr2, rtol=1e-5, atol=1e-8, equal_nan=False):
    func = partial(numpy_compat.isclose, rtol=rtol, atol=atol, equal_nan=equal_nan)
    return elemwise(func, arr1, arr2, dtype='bool')


def variadic_choose(a, *choices):
    return np.choose(a, choices)

@wraps(np.choose)
def choose(a, choices):
    return elemwise(variadic_choose, a, *choices)

where_error_message = """
The dask.array version of where only handles the three argument case.

    da.where(x > 0, x, 0)

and not the single argument case

    da.where(x > 0)

This is because dask.array operations must be able to infer the shape of their
outputs prior to execution.  The number of positive elements of x requires
execution.  See the ``np.where`` docstring for examples and the following link
for a more thorough explanation:

    http://dask.pydata.org/en/latest/array-overview.html#construct
""".strip()


chunks_none_error_message = """
You must specify a chunks= keyword argument.
This specifies the chunksize of your array blocks.

See the following documentation page for details:
  http://dask.pydata.org/en/latest/array-creation.html#chunks
""".strip()

@wraps(np.where)
def where(condition, x=None, y=None):
    if x is None or y is None:
        raise TypeError(where_error_message)
    return choose(condition, [y, x])


@wraps(chunk.coarsen)
def coarsen(reduction, x, axes, trim_excess=False):
    if (not trim_excess and
        not all(bd % div == 0 for i, div in axes.items()
                             for bd in x.chunks[i])):
        raise ValueError(
            "Coarsening factor does not align with block dimensions")

    if 'dask' in inspect.getfile(reduction):
        reduction = getattr(np, reduction.__name__)

    name = next(names)
    dsk = dict(((name,) + key[1:], (chunk.coarsen, reduction, key, axes,
                                        trim_excess))
                for key in core.flatten(x._keys()))
    chunks = tuple(tuple(int(bd // axes.get(i, 1)) for bd in bds)
                      for i, bds in enumerate(x.chunks))

    if x._dtype is not None:
        dt = reduction(np.empty((1,) * x.ndim, dtype=x.dtype)).dtype
    else:
        dt = None
    return Array(merge(x.dask, dsk), name, chunks, dtype=dt)


def split_at_breaks(array, breaks, axis=0):
    """ Split an array into a list of arrays (using slices) at the given breaks

    >>> split_at_breaks(np.arange(6), [3, 5])
    [array([0, 1, 2]), array([3, 4]), array([5])]
    """
    padded_breaks = concat([[None], breaks, [None]])
    slices = [slice(i, j) for i, j in sliding_window(2, padded_breaks)]
    preslice = (slice(None),) * axis
    split_array = [array[preslice + (s,)] for s in slices]
    return split_array


@wraps(np.insert)
def insert(arr, obj, values, axis):
    # axis is a required argument here to avoid needing to deal with the numpy
    # default case (which reshapes the array to make it flat)
    if not -arr.ndim <= axis < arr.ndim:
        raise IndexError('axis %r is out of bounds for an array of dimension '
                         '%s' % (axis, arr.ndim))
    if axis < 0:
        axis += arr.ndim

    if isinstance(obj, slice):
        obj = np.arange(*obj.indices(arr.shape[axis]))
    obj = np.asarray(obj)
    scalar_obj = obj.ndim == 0
    if scalar_obj:
        obj = np.atleast_1d(obj)

    obj = np.where(obj < 0, obj + arr.shape[axis], obj)
    if (np.diff(obj) < 0).any():
        raise NotImplementedError(
            'da.insert only implemented for monotonic ``obj`` argument')

    split_arr = split_at_breaks(arr, np.unique(obj), axis)

    if getattr(values, 'ndim', 0) == 0:
        # we need to turn values into a dask array
        name = next(names)
        dtype = getattr(values, 'dtype', type(values))
        values = Array({(name,): values}, name, chunks=(), dtype=dtype)

        values_shape = tuple(len(obj) if axis == n else s
                             for n, s in enumerate(arr.shape))
        values = broadcast_to(values, values_shape)
    elif scalar_obj:
        values = values[(slice(None),) * axis + (None,)]

    values_chunks = tuple(values_bd if axis == n else arr_bd
                          for n, (arr_bd, values_bd)
                          in enumerate(zip(arr.chunks,
                                           values.chunks)))
    values = values.rechunk(values_chunks)

    counts = np.bincount(obj)[:-1]
    values_breaks = np.cumsum(counts[counts > 0])
    split_values = split_at_breaks(values, values_breaks, axis)

    interleaved = list(interleave([split_arr, split_values]))
    interleaved = [i for i in interleaved if i.nbytes]
    return concatenate(interleaved, axis=axis)


@wraps(chunk.broadcast_to)
def broadcast_to(x, shape):
    shape = tuple(shape)
    ndim_new = len(shape) - x.ndim
    if ndim_new < 0 or any(new != old
                           for new, old in zip(shape[ndim_new:], x.shape)
                           if old != 1):
        raise ValueError('cannot broadcast shape %s to shape %s'
                         % (x.shape, shape))

    name = next(names)
    chunks = (tuple((s,) for s in shape[:ndim_new])
               + tuple(bd if old > 1 else (new,)
                       for bd, old, new in zip(x.chunks, x.shape,
                                               shape[ndim_new:])))
    dsk = dict(((name,) + (0,) * ndim_new + key[1:],
                (chunk.broadcast_to, key,
                 shape[:ndim_new] +
                 tuple(bd[i] for i, bd in zip(key[1:], chunks[ndim_new:]))))
               for key in core.flatten(x._keys()))
    return Array(merge(dsk, x.dask), name, chunks, dtype=x.dtype)


def offset_func(func, offset, *args):
    """  Offsets inputs by offset

    >>> double = lambda x: x * 2
    >>> f = offset_func(double, (10,))
    >>> f(1)
    22
    >>> f(300)
    620
    """
    def _offset(*args):
        args2 = list(map(add, args, offset))
        return func(*args2)

    with ignoring(Exception):
        _offset.__name__ = 'offset_' + func.__name__

    return _offset


fromfunction_names = ('fromfunction-%d' % i for i in count(1))

@wraps(np.fromfunction)
def fromfunction(func, chunks=None, shape=None, dtype=None):
    name = next(fromfunction_names)
    if chunks:
        chunks = normalize_chunks(chunks, shape)

    keys = list(product([name], *[range(len(bd)) for bd in chunks]))
    aggdims = [list(accumulate(add, (0,) + bd[:-1])) for bd in chunks]
    offsets = list(product(*aggdims))
    shapes = list(product(*chunks))

    values = [(np.fromfunction, offset_func(func, offset), shape)
                for offset, shape in zip(offsets, shapes)]

    dsk = dict(zip(keys, values))

    return Array(dsk, name, chunks, dtype=dtype)


@wraps(np.unique)
def unique(x):
    name = next(names)
    dsk = dict(((name, i), (np.unique, key)) for i, key in enumerate(x._keys()))
    parts = get(merge(dsk, x.dask), list(dsk.keys()))
    return np.unique(np.concatenate(parts))


@wraps(np.bincount)
def bincount(x, weights=None, minlength=None):
    if minlength is None:
        raise TypeError("Must specify minlength argument in da.bincount")
    assert x.ndim == 1
    if weights is not None:
        assert weights.chunks == x.chunks

    # Call np.bincount on each block, possibly with weights
    name = 'bincount' + next(tokens)
    if weights is not None:
        dsk = dict(((name, i),
                    (np.bincount, (x.name, i), (weights.name, i), minlength))
                    for i, _ in enumerate(x._keys()))
        dtype = 'f8'
    else:
        dsk = dict(((name, i),
                    (np.bincount, (x.name, i), None, minlength))
                    for i, _ in enumerate(x._keys()))
        dtype = 'i8'

    # Sum up all of the intermediate bincounts per block
    name = 'bincount-sum' + next(tokens)
    dsk[(name, 0)] = (np.sum, (list, list(dsk)), 0)

    chunks = ((minlength,),)

    dsk.update(x.dask)
    if weights is not None:
        dsk.update(weights.dask)

    return Array(dsk, name, chunks, dtype)

def histogram(a, bins=None, range=None, normed=False, weights=None, density=None):
    """
    Blocked variant of numpy.histogram.

    Follows the signature of numpy.histogram exactly with the following
    exceptions:

    - either the ``bins`` or ``range`` argument is required as computing
      ``min`` and ``max`` over blocked arrays is an expensive operation
      that must be performed explicitly.

    - ``weights`` must be a dask.array.Array with the same block structure
       as ``a``.

    Original signature follows below.
    """ + np.histogram.__doc__
    if bins is None or (range is None and bins is None):
        raise ValueError('dask.array.histogram requires either bins '
                         'or bins and range to be defined.')

    if weights is not None and weights.chunks != a.chunks:
        raise ValueError('Input array and weights must have the same '
                         'chunked structure')

    if not np.iterable(bins):
        mn, mx = range
        if mn == mx:
            mn -= 0.5
            mx += 0.5

        bins = np.linspace(mn, mx, bins + 1, endpoint=True)

    nchunks = len(list(core.flatten(a._keys())))
    chunks = ((1,) * nchunks, (len(bins) - 1,))

    name1 = 'histogram-sum' + next(tokens)


    # Map the histogram to all bins
    def block_hist(x, weights=None):
        return np.histogram(x, bins, weights=weights)[0][np.newaxis]

    if weights is None:
        dsk = dict(((name1, i, 0), (block_hist, k))
                    for i, k in enumerate(core.flatten(a._keys())))
        dtype = int
    else:
        a_keys = core.flatten(a._keys())
        w_keys = core.flatten(weights._keys())
        dsk = dict(((name1, i, 0), (block_hist, k, w))
                    for i, (k, w) in enumerate(zip(a_keys, w_keys)))
        dsk.update(weights.dask)
        dtype = weights.dtype

    dsk.update(a.dask)

    mapped = Array(dsk, name1, chunks, dtype=dtype)
    n = mapped.sum(axis=0)

    # We need to replicate normed and density options from numpy
    if density is not None:
        if density:
            db = from_array(np.diff(bins).astype(float), chunks=n.chunks)
            return n/db/n.sum(), bins
        else:
            return n, bins
    else:
        # deprecated, will be removed from Numpy 2.0
        if normed:
            db = from_array(np.diff(bins).astype(float), chunks=n.chunks)
            return n/(n*db).sum(), bins
        else:
            return n, bins

def chunks_from_arrays(arrays):
    """ Chunks tuple from nested list of arrays

    >>> x = np.array([1, 2])
    >>> chunks_from_arrays([x, x])
    ((2, 2),)

    >>> x = np.array([[1, 2]])
    >>> chunks_from_arrays([[x], [x]])
    ((1, 1), (2,))

    >>> x = np.array([[1, 2]])
    >>> chunks_from_arrays([[x, x]])
    ((1,), (2, 2))

    >>> chunks_from_arrays([1, 1])
    ((1, 1),)
    """
    result = []
    dim = 0

    def shape(x):
        try:
            return x.shape
        except AttributeError:
            return (1,)

    while isinstance(arrays, (list, tuple)):
        result.append(tuple(shape(deepfirst(a))[dim] for a in arrays))
        arrays = arrays[0]
        dim += 1
    return tuple(result)


def deepfirst(seq):
    """ First element in a nested list

    >>> deepfirst([[[1, 2], [3, 4]], [5, 6], [7, 8]])
    1
    """
    if not isinstance(seq, (list, tuple)):
        return seq
    else:
        return deepfirst(seq[0])


def ndimlist(seq):
    if not isinstance(seq, (list, tuple)):
        return 0
    else:
        return 1 + ndimlist(seq[0])


def concatenate3(arrays):
    """ Recursive np.concatenate

    Input should be a nested list of numpy arrays arranged in the order they
    should appear in the array itself.  Each array should have the same number
    of dimensions as the desired output and the nesting of the lists.

    >>> x = np.array([[1, 2]])
    >>> concatenate3([[x, x, x], [x, x, x]])
    array([[1, 2, 1, 2, 1, 2],
           [1, 2, 1, 2, 1, 2]])

    >>> concatenate3([[x, x], [x, x], [x, x]])
    array([[1, 2, 1, 2],
           [1, 2, 1, 2],
           [1, 2, 1, 2]])
    """
    arrays = concrete(arrays)
    ndim = ndimlist(arrays)
    if not ndim:
        return arrays
    chunks = chunks_from_arrays(arrays)
    shape = tuple(map(sum, chunks))

    def dtype(x):
        try:
            return x.dtype
        except AttributeError:
            return type(x)

    result = np.empty(shape=shape, dtype=dtype(deepfirst(arrays)))

    for (idx, arr) in zip(slices_from_chunks(chunks), core.flatten(arrays)):
        if hasattr(arr, 'ndim'):
            while arr.ndim < ndim:
                arr = arr[None, ...]
        result[idx] = arr

    return result


def to_hdf5(filename, *args, **kwargs):
    """ Store arrays in HDF5 file

    This saves several dask arrays into several datapaths in an HDF5 file.
    It creates the necessary datasets and handles clean file opening/closing.

    >>> da.to_hdf5('myfile.hdf5', '/x', x)  # doctest: +SKIP

    or

    >>> da.to_hdf5('myfile.hdf5', {'/x': x, '/y': y})  # doctest: +SKIP

    Optionally provide arguments as though to ``h5py.File.create_dataset``

    >>> da.to_hdf5('myfile.hdf5', '/x', x, compression='lzf', shuffle=True)  # doctest: +SKIP

    This can also be used as a method on a single Array

    >>> x.to_hdf5('myfile.hdf5', '/x')  # doctest: +SKIP

    See also
    --------
    da.store
    h5py.File.create_dataset
    """
    if len(args) == 1 and isinstance(args[0], dict):
        data = args[0]
    elif (len(args) == 2 and
          isinstance(args[0], str) and
          isinstance(args[1], Array)):
        data = {args[0]: args[1]}
    else:
        raise ValueError("Please provide {'/data/path': array} dictionary")

    import h5py
    with h5py.File(filename) as f:
        dsets = [f.require_dataset(dp, shape=x.shape, dtype=x.dtype,
                                        chunks=tuple([c[0] for c in x.chunks]),
                                        **kwargs)
                    for dp, x in data.items()]
        store(list(data.values()), dsets)
