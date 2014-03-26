import unittest
import mock

from uuiso import build


class TestGetParamsOrDie(unittest.TestCase):
    def test_no_parameters_command_quits(self):
        with self.assertRaises(SystemExit):
            build.get_args_or_die([])

    def test_mandatory_parameters_provided(self):
        options = build.get_args_or_die(['official', 'automated'])

        self.assertEquals('official', options.official)
        self.assertEquals('automated', options.automated)

    def test_after_install_parameter_missing(self):
        options = build.get_args_or_die(['a', 'b'])

        self.assertEquals(None, options.after_install)

    def test_after_install_parameter_specified(self):
        options = build.get_args_or_die(['a', 'b', '--after-install=somefile'])

        self.assertEquals('somefile', options.after_install)


def exists(fname):
    return True


def missing(fname):
    return False


def tempdirmaker():
    counter = []

    def tmpmaker():
        result = 'tempdir%s' % len(counter)
        counter.append('l')
        return result

    return tmpmaker


class IsoCreator(unittest.TestCase):
    def test_create(self):
        creator = build.IsoCreator('somedir', 'target.iso')
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


class TestIsoMounter(unittest.TestCase):
    def test_validate_file_exists(self):
        mounter = build.IsoMounter('isofile', file_checker=exists,
                                   binary_checker=exists)

        self.assertTrue(mounter.validate())

    def test_validate_binary_missing(self):
        mounter = build.IsoMounter('isofile', file_checker=exists,
                                   binary_checker=missing)

        self.assertFalse(mounter.validate())

    def test_validate_checks_for_all_binaries(self):
        mock_checker = mock.Mock()
        mock_checker.return_value = True
        mounter = build.IsoMounter('isofile', file_checker=exists,
                                   binary_checker=mock_checker)

        mounter.validate()

        self.assertEquals(
            [
                mock.call('fuseiso'),
                mock.call('unionfs-fuse'),
            ], mock_checker.mock_calls)

    def test_validate_file_missing(self):
        mounter = build.IsoMounter('isofile', file_checker=missing)

        self.assertFalse(mounter.validate())

    def test_mount_succeeds(self):
        mounter = build.IsoMounter(
            'isofile', executor=mock.Mock(), tmpmaker=tempdirmaker())

        mounter.mount()

        self.assertEquals(
            [
                mock.call(['fuseiso', 'isofile', 'tempdir0']),
                mock.call([
                    'unionfs-fuse', '-o', 'cow',
                    'tempdir1=RW:tempdir0=RO', 'tempdir2']),
            ], mounter.executor.mock_calls)

    def test_mount_sets_iso_mountpoint(self):
        mounter = build.IsoMounter(
            'isofile', executor=mock.Mock(), tmpmaker=tempdirmaker())

        mounter.mount()

        self.assertEquals('tempdir0', mounter.iso_mountpoint)

    def test_mount_sets_overlay_dir(self):
        mounter = build.IsoMounter(
            'isofile', executor=mock.Mock(), tmpmaker=tempdirmaker())

        mounter.mount()

        self.assertEquals('tempdir1', mounter.overlay_dir)

    def test_mount_sets_merged_dir(self):
        mounter = build.IsoMounter(
            'isofile', executor=mock.Mock(), tmpmaker=tempdirmaker())

        mounter.mount()

        self.assertEquals('tempdir2', mounter.merged_dir)

    def test_umount(self):
        mounter = build.IsoMounter(
            'isofile', executor=mock.Mock(), tmpmaker=tempdirmaker())
        mounter.mount()
        mounter.executor = mock.Mock()

        mounter.umount()

        self.assertEquals(
            [
                mock.call(['fusermount', '-u', 'tempdir2']),
                mock.call(['fusermount', '-u', 'tempdir0']),
            ], mounter.executor.mock_calls)


class TestTmpMaker(unittest.TestCase):
    def test_tmp_maker_registers_created_directories(self):
        fake_mkdtemp = mock.Mock()
        fake_mkdtemp.return_value = 'tmpdir'

        tmp_maker = build.TmpMaker(fake_mkdtemp)

        tmp_maker()

        self.assertEquals(['tmpdir'], tmp_maker.created_directories)
