import collections


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


class IsoOverlay(object):
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
        return OverlaidIso(self)

    def umount(self):
        self.executor(
            ['fusermount', '-u', self.merged_dir])
        self.executor(
            ['fusermount', '-u', self.iso_mountpoint])

    def __enter__(self):
        self.validate()
        return self.mount()

    def __exit__(self, exc_type, exc_value, traceback):
        self.umount()
        self.tmpmaker.remove_all()
        return False


OverlaidIsoData = collections.namedtuple('OverlaidIsoData', ['mounter'])


class OverlaidIso(OverlaidIsoData):
    def make_file_writable(self, fpath):
        import os
        import stat
        import shutil

        overlay_path = os.path.join(self.mounter.overlay_dir, fpath)
        iso_path = os.path.join(self.mounter.iso_mountpoint, fpath)

        overlay_dir = os.path.dirname(overlay_path)
        if not os.path.exists(overlay_dir):
            os.makedirs(overlay_dir)
        shutil.copy(iso_path, overlay_path)
        os.chmod(overlay_path, os.stat(overlay_path).st_mode | stat.S_IWUSR)
        return overlay_path
