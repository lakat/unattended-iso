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


class TestTmpMaker(unittest.TestCase):
    def test_tmp_maker_registers_created_directories(self):
        fake_mkdtemp = mock.Mock()
        fake_mkdtemp.return_value = 'tmpdir'

        tmp_maker = build.TmpMaker(fake_mkdtemp)

        tmp_maker()

        self.assertEquals(['tmpdir'], tmp_maker.created_directories)
