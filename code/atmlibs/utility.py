from contextlib import contextmanager
from functools import partial, reduce
import hashlib
import os
import os.path as osp
from pathlib import Path
import shutil
import tempfile

from appdirs import user_data_dir
import numpy as np

# General helpers

def compose(*funcs):
    # compose functions in order as read
    return reduce(lambda g, h: lambda x: h(g(x)), funcs, lambda x: x)

isr2 = 1/np.sqrt(2)

def hellinger(x, y):
    return isr2 * np.sqrt(((np.sqrt(x) - np.sqrt(y)) ** 2).sum())


def digest_paths(paths):
    """
      takes in a list containing paths to files
      returns digest SHA hash to be used as identifier over the whole list
    """
    SHAhash = hashlib.sha1()

    for filename in paths:

        f = open(filename, 'rb')

        while True:
            # Read files as little chunks to prevent large ram usage
            buf = f.read(4096)
            if not buf : break
            SHAhash.update(buf)
        f.close()

    return SHAhash.hexdigest()


# Directory/Path Utilities

def test_path(path):
    # tests if a path exists
    if not osp.exists(path):
        raise FileNotFoundError("File error: {} does not exist".format(path))
    return path


def location_resource(
  fname='.',
  location=user_data_dir('atm_resource', 'NASA_JPL')
  ):
    os.makedirs(location, exist_ok=True)
    return osp.join(location, fname)


def get_resource(fname='.'):
    path = location_resource(fname=fname)
    return test_path(path)


def commit_resource(full_path):
    srcdir, fname = osp.split(test_path(full_path))
    label = sign_path(full_path)
    copy_directory_files(srcdir, location_resource(), fname)
    src = partial(osp.join, location_resource())
    if osp.isfile(src(label)):
        # in order to rename on windows, target mustn't exist
        os.remove(src(fname))
    else:
        os.rename(src(fname), src(label))
    return label


def copy_directory_files(srcdir, dstdir, *filenames):
    """
      copies [filenames] from srcdir to dstdir
    """
    for filename in filenames:
        srcpath = osp.join(srcdir, filename)
        dstpath = osp.join(dstdir, filename)
        shutil.copyfile(srcpath, dstpath)


@contextmanager
def TemporaryDirectory(suffix='', prefix='tmp', dir=None, persist=False):
    """
    Like tempfile.NamedTemporaryFile, but creates a directory.
    """
    tree = tempfile.mkdtemp(suffix, prefix, dir)
    try:
        yield Path(tree)
    finally:
        if not persist:
            shutil.rmtree(tree)
