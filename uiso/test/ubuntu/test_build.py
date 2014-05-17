import unittest

from uiso.ubuntu import build


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
        options = build.get_args_or_die(
            ['a', 'b', '--after-install=somefile'])

        self.assertEquals('somefile', options.after_install)


class TestContentsOf(unittest.TestCase):
    def test_after_install_script(self):
        post_install = build.contents_of('post_install.sh')

        self.assertTrue(post_install.startswith('#!/bin/bash'))
