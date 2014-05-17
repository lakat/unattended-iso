import unittest
from pkg_resources import iter_entry_points

from uiso.ubuntu import build


class TestSetup(unittest.TestCase):
    def test_entry_point(self):
        entry_point, = list(iter_entry_points('console_scripts', 'uiso-build'))

        self.assertEquals(build.main, entry_point.load())
