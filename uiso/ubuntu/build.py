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
        overlaid_iso.setcontents('isolinux/txt.cfg', contents_of('txt.cfg'))
        overlaid_iso.setcontents('autoinst.seed', contents_of('autoinst.seed'))

        bootconfig = overlaid_iso.getcontents('isolinux/isolinux.cfg')

        overlaid_iso.setcontents('isolinux/isolinux.cfg',
                                 bootconfig.replace("timeout 0", "timeout 1"))

        overlaid_iso.setcontents(
            'post_install.sh', post_install_contents)

        overlaid_iso.write_iso(options.remastered_iso)
