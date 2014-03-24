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


class TestIsoMounter(unittest.TestCase):
    def test_validate_file_exists(self):
        mounter = build.IsoMounter('isofile', file_checker=exists)

        self.assertTrue(mounter.validate())

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
                mock.call(['unionfs-fuse', 'tempdir1:tempdir0', 'tempdir2']),
            ], mounter.executor.mock_calls)

    def test_mount_return_value(self):
        mounter = build.IsoMounter(
            'isofile', executor=mock.Mock(), tmpmaker=tempdirmaker())

        result = mounter.mount()

        self.assertEquals('tempdir0', result)
