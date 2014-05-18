import os
import tempfile
import shutil
import subprocess

from uiso import iso
from uiso import tempdir_maker


def binary_checker(fname):
    import distutils
    return bool(distutils.spawn.find_executable(fname))


def overlaid(iso_file):
    tmp_maker = tempdir_maker.TmpMaker(tempfile.mkdtemp, shutil.rmtree)
    return iso.IsoOverlay(iso_file,
                          file_checker=os.path.exists,
                          executor=subprocess.call,
                          tmpmaker=tmp_maker,
                          binary_checker=binary_checker)
