import unittest
import mock

from uiso import tempdir_maker


class TestTmpMaker(unittest.TestCase):
    def test_tmp_maker_registers_created_directories(self):
        fake_mkdtemp = mock.Mock()
        fake_mkdtemp.return_value = 'tmpdir'

        tmp_maker = tempdir_maker.TmpMaker(fake_mkdtemp)

        tmp_maker()

        self.assertEquals(['tmpdir'], tmp_maker.created_directories)
