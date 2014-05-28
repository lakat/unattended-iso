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
                'Automated Install CD',
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


def make_mounter(file_checker=exists, binary_checker=exists, tmpmaker=None,
                 **monkey_patches):
    executor = mock.Mock()
    tmpmaker = tmpmaker or tempdir_maker.tempdirmaker()

    mounter = iso.IsoOverlay(
        'isofile', file_checker=file_checker, binary_checker=binary_checker,
        executor=executor, tmpmaker=tmpmaker)

    for k, v in monkey_patches.items():
        setattr(mounter, k, v)

    return mounter


class TestIsoOverlay(unittest.TestCase):
    def test_validate_file_exists(self):
        mounter = make_mounter(binary_checker=exists)

        self.assertTrue(mounter.validate())

    def test_validate_binary_missing(self):
        mounter = make_mounter(binary_checker=missing)

        self.assertFalse(mounter.validate())

    def test_validate_checks_for_all_binaries(self):
        mock_checker = mock.Mock()
        mock_checker.return_value = True
        mounter = make_mounter(binary_checker=mock_checker)

        mounter.validate()

        self.assertEquals(
            [
                mock.call('fuseiso'),
                mock.call('unionfs-fuse'),
            ], mock_checker.mock_calls)

    def test_validate_file_missing(self):
        mounter = make_mounter(file_checker=missing)

        self.assertFalse(mounter.validate())

    def test_mount_return_value(self):
        mounter = make_mounter()

        result = mounter.mount()

        self.assertEquals(iso.OverlaidIso(
            mounter.overlay_dir, mounter.merged_dir, mounter.executor), result)

    def test_mount_succeeds(self):
        mounter = make_mounter()

        mounter.mount()

        self.assertEquals(
            [
                mock.call(['fuseiso', 'isofile', 'tempdir0']),
                mock.call([
                    'unionfs-fuse', '-o', 'cow',
                    'tempdir1=RW:tempdir0=RO', 'tempdir2']),
            ], mounter.executor.mock_calls)

    def test_mount_sets_iso_mountpoint(self):
        mounter = make_mounter()

        mounter.mount()

        self.assertEquals('tempdir0', mounter.iso_mountpoint)

    def test_mount_sets_overlay_dir(self):
        mounter = make_mounter()

        mounter.mount()

        self.assertEquals('tempdir1', mounter.overlay_dir)

    def test_mount_sets_merged_dir(self):
        mounter = make_mounter()

        mounter.mount()

        self.assertEquals('tempdir2', mounter.merged_dir)

    def test_umount(self):
        mounter = make_mounter()
        mounter.mount()
        mounter.executor = mock.Mock()

        mounter.umount()

        self.assertEquals(
            [
                mock.call(['fusermount', '-u', 'tempdir2']),
                mock.call(['fusermount', '-u', 'tempdir0']),
            ], mounter.executor.mock_calls)

    def test___enter___returns_mount_result(self):
        mounter = make_mounter()
        mounter.validate = mock.Mock()
        mounter.mount = mock.Mock()
        mounter.mount.return_value = 'mount result'

        context = mounter.__enter__()

        self.assertEquals('mount result', context)

    def test___enter___calls_validate(self):
        mounter = make_mounter(validate=mock.Mock(), mount=mock.Mock())

        mounter.__enter__()

        mounter.validate.assert_called_once_with()

    def test___enter___calls_mount(self):
        mounter = make_mounter(validate=mock.Mock(), mount=mock.Mock())

        mounter.__enter__()

        mounter.mount.assert_called_once_with()

    def test___exit___returns_false_propagating_exception(self):
        mounter = make_mounter(
            umount=mock.Mock(),
            tmpmaker=mock.Mock(spec=tempdir_maker.TmpMaker))

        result = mounter.__exit__(None, None, None)

        self.assertFalse(result)

    def test___exit___calls_umount(self):
        mounter = make_mounter(
            umount=mock.Mock(),
            tmpmaker=mock.Mock(spec=tempdir_maker.TmpMaker))

        mounter.__exit__(None, None, None)

        mounter.umount.assert_called_once_with()

    def test___exit___cleans_up_tempdirs(self):
        mounter = make_mounter(
            umount=mock.Mock(),
            tmpmaker=mock.Mock(spec=tempdir_maker.TmpMaker))

        mounter.__exit__(None, None, None)

        mounter.tmpmaker.remove_all.assert_called_once_with()


class TestOverlaidIso(unittest.TestCase):
    @mock.patch('uiso.iso.IsoCreator')
    def test_make_iso(self, iso_creator):
        overlaid = iso.OverlaidIso(
            overlay_dir=None, merged_dir='merged', executor='executor')
        creator = iso_creator.return_value = mock.Mock()

        overlaid.write_iso('isofile')

        creator.create.assert_called_once_with()
