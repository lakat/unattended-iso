import argparse


class IsoMounter(object):
    def __init__(self, path, file_checker=None, executor=None, tmpmaker=None,
                 binary_checker=None):
        self.path = path
        self.file_checker = file_checker
        self.executor = executor
        self.tmpmaker = tmpmaker
        self.binary_checker = binary_checker
        self.iso_mountpoint = None
        self.merged_dir = None
        self.overlay_dir = None

    def validate(self):
        if self.file_checker(self.path):
            if self.binary_checker('fuseiso'):
                if self.binary_checker('unionfs-fuse'):
                    return True
        return False

    def mount(self):
        self.iso_mountpoint = self.tmpmaker()
        self.overlay_dir = self.tmpmaker()
        self.merged_dir = self.tmpmaker()
        self.executor(
            ['fuseiso', self.path, self.iso_mountpoint])
        self.executor(
            [
                'unionfs-fuse',
                ':'.join([self.overlay_dir, self.iso_mountpoint]),
                self.merged_dir
            ]
        )


class IsoCreator(object):
    def __init__(self, source_dir, target_file):
        self.source_dir = source_dir
        self.target_file = target_file

    def create(self):
        self.executor([
            'mkisofs',
            '-r',
            '-V',
            'Automated Ubuntu Install CD',
            '-cache-inodes',
            '-J',
            '-l',
            '-b', 'isolinux/isolinux.bin',
            '-c', 'isolinux/boot.cat',
            '-no-emul-boot',
            '-boot-load-size', '4',
            '-boot-info-table',
            '-quiet',
            '-o', self.target_file,
            self.source_dir,
            ])


def get_args_or_die(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('official')
    parser.add_argument('automated')

    return parser.parse_args(args=args)


def main():
    pass
