from contextlib import contextmanager
import os
import shutil
from tempfile import mkdtemp

import pytest
pytest.importorskip('skimage')
from dask.array.image import imread as da_imread
import numpy as np
from skimage.io import imread, imsave


@contextmanager
def random_images(n, shape):
    dirname = mkdtemp()
    for i in range(n):
        fn = os.path.join(dirname, 'image.%d.png' % i)
        x = np.random.randint(0, 255, size=shape).astype('i1')
        imsave(fn, x)

    try:
        yield os.path.join(dirname, '*.png')
    finally:
        shutil.rmtree(dirname)


def test_imread():
    with random_images(4, (5, 6, 3)) as globstring:
        im = da_imread(globstring)
        assert im.shape == (4, 5, 6, 3)
        assert im.chunks == ((1, 1, 1, 1), (5,), (6,), (3,))
        assert im.dtype == 'uint8'

        assert im.compute().shape == (4, 5, 6, 3)
        assert im.compute().dtype == 'uint8'
