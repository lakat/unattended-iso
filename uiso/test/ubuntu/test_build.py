import unittest

from uiso.ubuntu import build


class TestGetParamsOrDie(unittest.TestCase):
    def test_no_parameters_command_quits(self):
        with self.assertRaises(SystemExit):
            build.get_args_or_die([])

    def test_mandatory_parameters_provided(self):
        options = build.get_args_or_die(['official', 'automated'])

        self.assertEquals('official', options.base_iso)
        self.assertEquals('automated', options.remastered_iso)

    def test_post_install_parameter_missing(self):
        options = build.get_args_or_die(['a', 'b'])

        self.assertEquals(None, options.post_install_script)

    def test_post_install_parameter_specified(self):
        options = build.get_args_or_die(
            ['a', 'b', '--post-install-script=somefile'])

        self.assertEquals('somefile', options.post_install_script)


class TestContentsOf(unittest.TestCase):
    def test_post_install_script(self):
        post_install = build.contents_of('post_install.sh')

        self.assertTrue(post_install.startswith('#!/bin/bash'))
