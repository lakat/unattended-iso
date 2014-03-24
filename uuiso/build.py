import argparse


class IsoMounter(object):
    def __init__(self, path, file_checker=None, executor=None, tmpmaker=None):
        self.path = path
        self.file_checker = file_checker
        self.executor = executor
        self.tmpmaker = tmpmaker
        self.iso_mountpoint = None
        self.merged_dir = None
        self.overlay_dir = None

    def validate(self):
        if self.file_checker(self.path):
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


def get_args_or_die(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('official')
    parser.add_argument('automated')

    return parser.parse_args(args=args)


def main():
    pass
