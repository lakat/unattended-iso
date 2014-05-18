import unittest
import mock

from uiso import tempdir_maker


class TestTmpMaker(unittest.TestCase):
    def test_created_directories_registered(self):
        fake_mkdtemp = mock.Mock()
        fake_mkdtemp.return_value = 'tmpdir'

        tmp_maker = tempdir_maker.TmpMaker(fake_mkdtemp, None)

        tmp_maker()

        self.assertEquals(['tmpdir'], tmp_maker.created_directories)

    def test_remove_all_no_created_dirs_doesnt_call_rmtree(self):
        mock_rmtree = mock.Mock()

        tmp_maker = tempdir_maker.TmpMaker(None, mock_rmtree)
        tmp_maker.created_directories = []

        tmp_maker.remove_all()

        self.assertEquals([], mock_rmtree.mock_calls)

    def test_remove_all_removes_created_dirs_reversed_order(self):
        mock_rmtree = mock.Mock()

        tmp_maker = tempdir_maker.TmpMaker(None, mock_rmtree)
        tmp_maker.created_directories = ['1', '2', '3']

        tmp_maker.remove_all()

        self.assertEquals([
            mock.call('3'),
            mock.call('2'),
            mock.call('1'),
        ], mock_rmtree.mock_calls)
