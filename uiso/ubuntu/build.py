import argparse
import os

from uiso import iso
from uiso import tempdir_maker


def get_args_or_die(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('official')
    parser.add_argument('automated')
    parser.add_argument('--after-install')

    return parser.parse_args(args=args)


def contents_of(fname):
    this_path = os.path.dirname(__file__)
    data_path = os.path.join(this_path, fname)
    with open(data_path, 'rb') as data_file:
        return data_file.read()


def binary_checker(fname):
    import distutils
    return bool(distutils.spawn.find_executable(fname))


def main():
    import os
    import subprocess
    import tempfile
    import shutil

    options = get_args_or_die()

    if options.after_install:
        with open(options.after_install, 'rb') as after_install_file:
            after_install_script_contents = after_install_file.read()
    else:
        after_install_script_contents = contents_of('post_install.sh')

    tmp_maker = tempdir_maker.TmpMaker(tempfile.mkdtemp, shutil.rmtree)

    with iso.IsoOverlay(options.official,
                        file_checker=os.path.exists,
                        executor=subprocess.call,
                        tmpmaker=tmp_maker,
                        binary_checker=binary_checker) as overlaid_iso:

        overlaid_iso.setcontents(
            'isolinux/isolinux.bin',
            overlaid_iso.getcontents('isolinux/isolinux.bin'))
        overlaid_iso.setcontents('isolinux/txt.cfg', contents_of('txt.cfg'))
        overlaid_iso.setcontents('autoinst.seed', contents_of('autoinst.seed'))

        bootconfig = overlaid_iso.getcontents('isolinux/isolinux.cfg')

        overlaid_iso.setcontents('isolinux/isolinux.cfg',
                                 bootconfig.replace("timeout 0", "timeout 1"))

        overlaid_iso.setcontents(
            'after_install.sh', after_install_script_contents)

        iso_maker = iso.IsoCreator(
            overlaid_iso.mounter.merged_dir,
            options.automated,
            executor=subprocess.call)

        iso_maker.create()
