import unittest

from uiso import ubuntu


class TestGetParamsOrDie(unittest.TestCase):
    def test_no_parameters_command_quits(self):
        with self.assertRaises(SystemExit):
            ubuntu.get_args_or_die([])

    def test_mandatory_parameters_provided(self):
        options = ubuntu.get_args_or_die(['official', 'automated'])

        self.assertEquals('official', options.official)
        self.assertEquals('automated', options.automated)

    def test_after_install_parameter_missing(self):
        options = ubuntu.get_args_or_die(['a', 'b'])

        self.assertEquals(None, options.after_install)

    def test_after_install_parameter_specified(self):
        options = ubuntu.get_args_or_die(['a', 'b', '--after-install=somefile'])

        self.assertEquals('somefile', options.after_install)


