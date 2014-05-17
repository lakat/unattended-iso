import unittest
import mock

from uiso import iso
from uiso import tempdir_maker


class IsoCreator(unittest.TestCase):
    def test_create(self):
        creator = iso.IsoCreator('somedir', 'target.iso')
        mock_executor = mock.Mock()
        creator.executor = mock_executor

        creator.create()

        self.assertEquals([
            mock.call([
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
                '-o', 'target.iso',
                'somedir'
            ])],
            mock_executor.mock_calls)


def exists(fname):
    return True


def missing(fname):
    return False


class TestIsoMounter(unittest.TestCase):
    def test_validate_file_exists(self):
        mounter = iso.IsoMounter('isofile', file_checker=exists,
                                   binary_checker=exists)

        self.assertTrue(mounter.validate())

    def test_validate_binary_missing(self):
        mounter = iso.IsoMounter('isofile', file_checker=exists,
                                   binary_checker=missing)

        self.assertFalse(mounter.validate())

    def test_validate_checks_for_all_binaries(self):
        mock_checker = mock.Mock()
        mock_checker.return_value = True
        mounter = iso.IsoMounter('isofile', file_checker=exists,
                                   binary_checker=mock_checker)

        mounter.validate()

        self.assertEquals(
            [
                mock.call('fuseiso'),
                mock.call('unionfs-fuse'),
            ], mock_checker.mock_calls)

    def test_validate_file_missing(self):
        mounter = iso.IsoMounter('isofile', file_checker=missing)

        self.assertFalse(mounter.validate())

    def test_mount_succeeds(self):
        mounter = iso.IsoMounter(
            'isofile', executor=mock.Mock(), tmpmaker=tempdir_maker.tempdirmaker())

        mounter.mount()

        self.assertEquals(
            [
                mock.call(['fuseiso', 'isofile', 'tempdir0']),
                mock.call([
                    'unionfs-fuse', '-o', 'cow',
                    'tempdir1=RW:tempdir0=RO', 'tempdir2']),
            ], mounter.executor.mock_calls)

    def test_mount_sets_iso_mountpoint(self):
        mounter = iso.IsoMounter(
            'isofile', executor=mock.Mock(), tmpmaker=tempdir_maker.tempdirmaker())

        mounter.mount()

        self.assertEquals('tempdir0', mounter.iso_mountpoint)

    def test_mount_sets_overlay_dir(self):
        mounter = iso.IsoMounter(
            'isofile', executor=mock.Mock(), tmpmaker=tempdir_maker.tempdirmaker())

        mounter.mount()

        self.assertEquals('tempdir1', mounter.overlay_dir)

    def test_mount_sets_merged_dir(self):
        mounter = iso.IsoMounter(
            'isofile', executor=mock.Mock(), tmpmaker=tempdir_maker.tempdirmaker())

        mounter.mount()

        self.assertEquals('tempdir2', mounter.merged_dir)

    def test_umount(self):
        mounter = iso.IsoMounter(
            'isofile', executor=mock.Mock(), tmpmaker=tempdir_maker.tempdirmaker())
        mounter.mount()
        mounter.executor = mock.Mock()

        mounter.umount()

        self.assertEquals(
            [
                mock.call(['fusermount', '-u', 'tempdir2']),
                mock.call(['fusermount', '-u', 'tempdir0']),
            ], mounter.executor.mock_calls)



