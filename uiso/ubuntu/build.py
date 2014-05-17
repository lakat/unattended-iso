import argparse
import textwrap
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


def main():
    import os
    import subprocess
    import tempfile

    options = get_args_or_die()

    tmp_maker = tempdir_maker.TmpMaker(tempfile.mkdtemp)

    mounter = iso.IsoMounter(
        options.official, os.path.exists, subprocess.call, tmp_maker)

    mounter.validate()

    mounter.mount()

    try:
        mounter.make_file_writable('isolinux/isolinux.bin')
        txt_cfg = mounter.make_file_writable('isolinux/txt.cfg')

        with open(txt_cfg, 'wb') as txt:
            txt.write(contents_of('txt.cfg'))

        with open(os.path.join(mounter.overlay_dir, 'autoinst.seed'), 'wb') as seed:
            seed.write(contents_of('preseed'))

        isolinux_cfg = mounter.make_file_writable('isolinux/isolinux.cfg')

        with open(isolinux_cfg, 'rb') as bootcfg:
            bootconfig = bootcfg.read()

        with open(isolinux_cfg, 'wb') as bootcfg:
            bootcfg.write(bootconfig.replace("timeout 0", "timeout 1"))

        if options.after_install:
            with open(options.after_install, 'rb') as after_install_file:
                after_install_script_contents = after_install_file.read()
        else:
            after_install_script_contents = contents_of('post_install.sh')

        with open(os.path.join(mounter.overlay_dir, 'after_install.sh'), 'wb') as after_install:
            after_install.write(after_install_script_contents)

        iso_maker = iso.IsoCreator(
            mounter.merged_dir, options.automated, executor=subprocess.call)

        iso_maker.create()
    finally:
        mounter.umount()
