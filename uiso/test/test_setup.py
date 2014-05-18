import unittest
from pkg_resources import iter_entry_points

from uiso.ubuntu import build as ubuntu_build
from uiso.centos import build as centos_build


class TestSetup(unittest.TestCase):
    def test_ubuntu_entry_point(self):
        entry_point, = list(iter_entry_points('console_scripts',
                                              'uiso-ubuntu'))

        self.assertEquals(ubuntu_build.main, entry_point.load())

    def test_centos_entry_point(self):
        entry_point, = list(iter_entry_points('console_scripts',
                                              'uiso-centos'))

        self.assertEquals(centos_build.main, entry_point.load())
