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
                '-o',
                'cow',
                ':'.join(
                    [self.overlay_dir + '=RW', self.iso_mountpoint + '=RO']),
                self.merged_dir
            ]
        )

    def umount(self):
        self.executor(
            ['fusermount', '-u', self.merged_dir])
        self.executor(
            ['fusermount', '-u', self.iso_mountpoint])


class IsoCreator(object):
    def __init__(self, source_dir, target_file, executor=None):
        self.source_dir = source_dir
        self.target_file = target_file
        self.executor = executor

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


class TmpMaker(object):
    def __init__(self, mkdtemp):
        self.mkdtemp = mkdtemp
        self.created_directories = []

    def __call__(self):
        tmp_dir = self.mkdtemp()
        self.created_directories.append(tmp_dir)
        return tmp_dir


def get_args_or_die(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('official')
    parser.add_argument('automated')

    return parser.parse_args(args=args)


def main():
    import os
    import subprocess
    import tempfile
    import stat
    import shutil

    options = get_args_or_die()

    tmp_maker = TmpMaker(tempfile.mkdtemp)

    mounter = IsoMounter(
        options.official, os.path.exists, subprocess.call, tmp_maker)

    mounter.mount()

    try:
        fpath = 'isolinux/isolinux.bin'
        overlay_path = os.path.join(mounter.overlay_dir, fpath)
        iso_path = os.path.join(mounter.iso_mountpoint, fpath)

        os.makedirs(os.path.dirname(overlay_path))
        shutil.copy(iso_path, overlay_path)
        os.chmod(overlay_path, os.stat(overlay_path).st_mode | stat.S_IWUSR)

        iso_maker = IsoCreator(
            mounter.merged_dir, options.automated, executor=subprocess.call)

        iso_maker.create()
    finally:
        mounter.umount()
