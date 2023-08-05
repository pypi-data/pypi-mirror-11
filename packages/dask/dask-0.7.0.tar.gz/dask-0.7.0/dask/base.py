import warnings
from operator import attrgetter
from hashlib import md5
from functools import partial

from toolz import merge, groupby, curry
from toolz.functoolz import Compose

from .context import _globals
from .utils import Dispatch, ignoring

__all__ = ("Base", "compute", "normalize_token", "tokenize")


class Base(object):
    """Base class for dask collections"""

    def visualize(self, filename='mydask', optimize_graph=False):
        from dask.dot import dot_graph
        if optimize_graph:
            dsk = self._optimize(self.dask, self._keys())
        else:
            dsk = self.dask
        return dot_graph(dsk, filename=filename)

    def _visualize(self, filename='mydask', optimize_graph=False):
        warn = DeprecationWarning("``_visualize`` is deprecated, use "
                                  "``visualize`` instead.")
        warnings.warn(warn)
        return self.visualize(optimize_graph)

    def compute(self, **kwargs):
        return compute(self, **kwargs)[0]

    @classmethod
    def _get(cls, dsk, keys, get=None, **kwargs):
        get = get or _globals['get'] or cls._default_get
        dsk2 = cls._optimize(dsk, keys)
        return get(dsk2, keys, **kwargs)


def compute(*args, **kwargs):
    """Compute several dask collections at once.

    Examples
    --------
    >>> import dask.array as da
    >>> a = da.arange(10, chunks=2).sum()
    >>> b = da.arange(10, chunks=2).mean()
    >>> compute(a, b)
    (45, 4.5)
    """
    groups = groupby(attrgetter('_optimize'), args)
    get = kwargs.pop('get', None) or _globals['get']

    if not get:
        get = args[0]._default_get
        if not all(a._default_get == get for a in args):
            raise ValueError("Compute called on multiple collections with "
                             "differing default schedulers. Please specify a "
                             "scheduler `get` function using either "
                             "the `get` kwarg or globally with `set_options`.")

    dsk = merge([opt(merge([v.dask for v in val]), [v._keys() for v in val])
                for opt, val in groups.items()])
    keys = [arg._keys() for arg in args]
    results = get(dsk, keys, **kwargs)
    return tuple(a._finalize(a, r) for a, r in zip(args, results))


def normalize_function(func):
    if isinstance(func, curry):
        func = func._partial
    if isinstance(func, Compose):
        first = getattr(func, 'first', None)
        funcs = reversed((first,) + func.funcs) if first else func.funcs
        return tuple(normalize_function(f) for f in funcs)
    elif isinstance(func, partial):
        kws = tuple(sorted(func.keywords.items())) if func.keywords else ()
        return (normalize_function(func.func), func.args, kws)
    else:
        return str(func)


normalize_token = Dispatch()
normalize_token.register((int, float, str, tuple, list), lambda a: a)
normalize_token.register(object,
        lambda a: normalize_function(a) if callable(a) else a)
normalize_token.register(dict, lambda a: tuple(sorted(a.items())))
with ignoring(ImportError):
    import pandas as pd
    normalize_token.register(pd.DataFrame,
            lambda a: (id(a), len(a), list(a.columns)))
    normalize_token.register(pd.Series, lambda a: (id(a), len(a), a.name))
with ignoring(ImportError):
    import numpy as np
    normalize_token.register(np.ndarray, lambda a: (id(a), a.dtype, a.shape))


def tokenize(*args):
    """ Deterministic token

    >>> tokenize([1, 2, '3'])
    '9d71491b50023b06fc76928e6eddb952'

    >>> tokenize('Hello') == tokenize('Hello')
    True
    """
    return md5(str(tuple(map(normalize_token, args))).encode()).hexdigest()
