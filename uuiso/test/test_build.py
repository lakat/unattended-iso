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


def tempdir():
    return 'tempdir'


class TestIsoMounter(unittest.TestCase):
    def test_validate_file_exists(self):
        unpacker = build.IsoMounter('isofile', file_checker=exists)

        self.assertTrue(unpacker.validate())

    def test_validate_file_missing(self):
        unpacker = build.IsoMounter('isofile', file_checker=missing)

        self.assertFalse(unpacker.validate())

    def test_unpack_succeeds(self):
        unpacker = build.IsoMounter(
            'isofile', executor=mock.Mock(), tmpmaker=tempdir)

        unpacker.mount()

        unpacker.executor.assert_called_once_with(
            ['fuseiso', 'isofile', 'tempdir'])

    def test_unpack_return_value(self):
        unpacker = build.IsoMounter(
            'isofile', executor=mock.Mock(), tmpmaker=tempdir)

        result = unpacker.mount()

        self.assertEquals('tempdir', result)
