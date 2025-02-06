import os
import shutil
import unittest
from unittest.mock import patch
from manager import copy, move_file, delete, count_files, show_files, search, get_creation_time, rename, \
    organize


class TestCopyFunctionWithMock(unittest.TestCase):
    @patch('os.path.isdir')
    @patch('os.path.isfile')
    @patch('shutil.copytree')
    @patch('shutil.copy')
    def test_copy_directory_mock(self, mock_copy, mock_copytree, mock_isfile, mock_isdir):
        mock_isdir.return_value = True
        mock_isfile.return_value = False

        copy('/source/dir', '/destination/dir')

        mock_isdir.assert_called_once_with('/source/dir')
        mock_copytree.assert_called_once_with('/source/dir', '/destination/dir')
        mock_copy.assert_not_called()

    @patch('os.path.isdir')
    @patch('os.path.isfile')
    @patch('shutil.copytree')
    @patch('shutil.copy')
    def test_copy_file_mock(self, mock_copy, mock_copytree, mock_isfile, mock_isdir):
        mock_isdir.return_value = False
        mock_isfile.return_value = True

        copy('/source/file.txt', '/destination/file.txt')

        mock_isfile.assert_called_once_with('/source/file.txt')
        mock_copy.assert_called_once_with('/source/file.txt', '/destination/file.txt')
        mock_copytree.assert_not_called()

    @patch('os.path.isdir')
    @patch('os.path.isfile')
    def test_copy_nonexistent_path_mock(self, mock_isfile, mock_isdir):
        mock_isdir.return_value = False
        mock_isfile.return_value = False

        with patch('builtins.print') as mock_print:
            copy('/nonexistent/path', '/destination')

            mock_print.assert_called_once_with("Error: file or folder doesn't exist")


class TestMoveFile(unittest.TestCase):
    @patch('shutil.move')
    def test_move_file(self, mock_move):
        with patch('builtins.print') as mock_print:
            move_file('source.txt', 'destination.txt')

            mock_move.assert_called_once_with('source.txt', 'destination.txt')

            mock_print.assert_called_once_with(
                "Your file/folder'source.txt' has been moved to  'destination.txt'"
            )


class TestDelete(unittest.TestCase):

    @patch('shutil.rmtree')
    @patch('os.path.isdir', return_value=True)
    def test_delete_directory(self, mock_isdir, mock_rmtree):
        with patch('builtins.print') as mock_print:
            delete('/path/folder')
            mock_rmtree.assert_called_once_with('/path/folder')
            mock_print.assert_called_once_with("The folder '/path/folder' is deleted")

    @patch('os.remove')
    @patch('os.path.isfile', return_value=True)
    def test_delete_file(self, mock_isfile, mock_remove):
        with patch('builtins.print') as mock_print:
            delete('/path/file.txt')
            mock_remove.assert_called_once_with('/path/file.txt')
            mock_print.assert_called_once_with("The file '/path/file.txt' is deleted")

    @patch('builtins.print')
    def test_delete_nonexistent(self, mock_print):
        delete('/path/nonexistent')
        mock_print.assert_called_once_with("Error: the file/ or folder is not found")


class TestCountFiles(unittest.TestCase):

    @patch('os.walk')
    def test_count_files(self, mock_walk):
        mock_walk.return_value = [
            ('/root', ['dir1'], ['file1.txt', 'file2.txt']),
            ('/root/dir1', [], ['file3.txt'])
        ]

        self.assertEqual(count_files('/root'), 3)


class TestShowFiles(unittest.TestCase):

    @patch('os.listdir')
    @patch('builtins.print')
    def test_show_files(self, mock_print, mock_listdir):
        mock_listdir.return_value = ['file1.txt', 'file2.txt', 'file3.txt']

        show_files('/path/to/folder')

        mock_print.assert_called_once_with('file1.txt', 'file2.txt', 'file3.txt')


class TestSearchFunction(unittest.TestCase):
    @patch('os.walk')
    def test_search_files(self, mock_walk):
        mock_walk.return_value = [
            ('D:\\Downloads', ['dir1'], ['file1.txt', 'file2.txt']),
            ('D:\\Downloads\\dir1', [], ['file3.txt'])
        ]

        result = search('D:\\Downloads', '.txt')

        # Expected result with backslashes in paths (without normalization)
        expected = ['D:\\Downloads\\file1.txt', 'D:\\Downloads\\file2.txt', 'D:\\Downloads\\dir1\\file3.txt']

        # Assert the result matches the expected output
        self.assertEqual(result, expected)


class TestRenameFunction(unittest.TestCase):
    @patch('os.rename')
    @patch('manager.get_creation_time', return_value="2025-02-06")
    def test_rename_file(self, mock_get_creation_time, mock_rename):
        src = 'path/to/file.txt'

        rename(src)

        mock_get_creation_time.assert_called_once_with(src)

        new_filename = 'path/to/file_2025-02-06.txt'
        mock_rename.assert_called_once_with(src, new_filename)


class TestOrganize(unittest.TestCase):
    class TestOrganize(unittest.TestCase):

        @patch('shutil.move')
        @patch('os.mkdir')
        @patch('os.path.exists', return_value=False)
        @patch('os.listdir', return_value=['file1.txt', 'file2.jpg', 'file3.txt'])
        def test_organize(self, mock_listdir, mock_exists, mock_mkdir, mock_move):
            organize('/mock_folder')

            mock_mkdir.assert_any_call('/mock_folder/txt')
            mock_mkdir.assert_any_call('/mock_folder/jpg')

            mock_move.assert_any_call('/mock_folder/file1.txt', '/mock_folder/txt/file1.txt')
            mock_move.assert_any_call('/mock_folder/file2.jpg', '/mock_folder/jpg/file2.jpg')
            mock_move.assert_any_call('/mock_folder/file3.txt', '/mock_folder/txt/file3.txt')

            self.assertEqual(mock_mkdir.call_count, 2)
            self.assertEqual(mock_move.call_count, 3)


if __name__ == '__main__':
    unittest.main()
