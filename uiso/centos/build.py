import argparse
import os

from uiso import builder


def get_args_or_die(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('base_iso')
    parser.add_argument('remastered_iso')
    parser.add_argument('--post-install-script')

    return parser.parse_args(args=args)


def contents_of(fname):
    this_path = os.path.dirname(__file__)
    data_path = os.path.join(this_path, fname)
    with open(data_path, 'rb') as data_file:
        return data_file.read()


def main():
    options = get_args_or_die()

    if options.post_install_script:
        with open(options.post_install_script, 'rb') as script_file:
            post_install_contents = script_file.read()
    else:
        post_install_contents = contents_of('post_install.sh')

    with builder.overlaid(options.base_iso) as overlaid_iso:

        overlaid_iso.setcontents(
            'isolinux/isolinux.bin',
            overlaid_iso.getcontents('isolinux/isolinux.bin'))

        if overlaid_iso.exists('RPM-GPG-KEY-CentOS-5'):
            bootconfig = contents_of('isolinux.cfg.5')
            kickstart = contents_of('ks.cfg.5')
        elif overlaid_iso.exists('RPM-GPG-KEY-CentOS-6'):
            bootconfig = contents_of('isolinux.cfg.6')
            kickstart = contents_of('ks.cfg.6')
        else:
            raise SystemExit('This version is not supported')

        overlaid_iso.setcontents('isolinux/isolinux.cfg', bootconfig)

        overlaid_iso.setcontents('ks.cfg', kickstart)
        overlaid_iso.setcontents('post_install.sh', post_install_contents)
        overlaid_iso.write_iso(options.remastered_iso)
