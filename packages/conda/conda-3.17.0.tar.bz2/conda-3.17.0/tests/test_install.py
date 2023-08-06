from contextlib import contextmanager
import random
import shutil
import stat
import tempfile
import unittest
from os.path import join


from conda import install
from conda.install import PaddingError, binary_replace, update_prefix

from .decorators import skip_if_no_mock
from .helpers import mock

patch = mock.patch if mock else None


def generate_random_path():
    return '/some/path/to/file%s' % random.randint(100, 200)


class TestBinaryReplace(unittest.TestCase):

    def test_simple(self):
        self.assertEqual(
            binary_replace(b'xxxaaaaaxyz\x00zz', b'aaaaa', b'bbbbb'),
            b'xxxbbbbbxyz\x00zz')

    def test_shorter(self):
        self.assertEqual(
            binary_replace(b'xxxaaaaaxyz\x00zz', b'aaaaa', b'bbbb'),
            b'xxxbbbbxyz\x00\x00zz')

    def test_too_long(self):
        self.assertRaises(PaddingError, binary_replace,
                          b'xxxaaaaaxyz\x00zz', b'aaaaa', b'bbbbbbbb')

    def test_no_extra(self):
        self.assertEqual(binary_replace(b'aaaaa\x00', b'aaaaa', b'bbbbb'),
                         b'bbbbb\x00')

    def test_two(self):
        self.assertEqual(
            binary_replace(b'aaaaa\x001234aaaaacc\x00\x00', b'aaaaa',
                           b'bbbbb'),
            b'bbbbb\x001234bbbbbcc\x00\x00')

    def test_spaces(self):
        self.assertEqual(
            binary_replace(b' aaaa \x00', b'aaaa', b'bbbb'),
            b' bbbb \x00')

    def test_multiple(self):
        self.assertEqual(
            binary_replace(b'aaaacaaaa\x00', b'aaaa', b'bbbb'),
            b'bbbbcbbbb\x00')
        self.assertEqual(
            binary_replace(b'aaaacaaaa\x00', b'aaaa', b'bbb'),
            b'bbbcbbb\x00\x00\x00')
        self.assertRaises(PaddingError, binary_replace,
                          b'aaaacaaaa\x00', b'aaaa', b'bbbbb')


class FileTests(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.tmpfname = join(self.tmpdir, 'testfile')

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def test_default_text(self):
        with open(self.tmpfname, 'w') as fo:
            fo.write('#!/opt/anaconda1anaconda2anaconda3/bin/python\n'
                     'echo "Hello"\n')
        update_prefix(self.tmpfname, '/usr/local')
        with open(self.tmpfname, 'r') as fi:
            data = fi.read()
            self.assertEqual(data, '#!/usr/local/bin/python\n'
                                   'echo "Hello"\n')

    def test_binary(self):
        with open(self.tmpfname, 'wb') as fo:
            fo.write(b'\x7fELF.../some-placeholder/lib/libfoo.so\0')
        update_prefix(self.tmpfname, '/usr/local',
                      placeholder='/some-placeholder', mode='binary')
        with open(self.tmpfname, 'rb') as fi:
            data = fi.read()
            self.assertEqual(
                data,
                b'\x7fELF.../usr/local/lib/libfoo.so\0\0\0\0\0\0\0\0'
            )


class remove_readonly_TestCase(unittest.TestCase):
    def test_takes_three_args(self):
        with self.assertRaises(TypeError):
            install._remove_readonly()

        with self.assertRaises(TypeError):
            install._remove_readonly(True)

        with self.assertRaises(TypeError):
            install._remove_readonly(True, True)

        with self.assertRaises(TypeError):
            install._remove_readonly(True, True, True, True)

    @skip_if_no_mock
    def test_calls_os_chmod(self):
        some_path = generate_random_path()
        with patch.object(install.os, 'chmod') as chmod:
            install._remove_readonly(mock.Mock(), some_path, {})
        chmod.assert_called_with(some_path, stat.S_IWRITE)

    @skip_if_no_mock
    def test_calls_func(self):
        some_path = generate_random_path()
        func = mock.Mock()
        with patch.object(install.os, 'chmod'):
            install._remove_readonly(func, some_path, {})
        func.assert_called_with(some_path)


class rm_rf_file_and_link_TestCase(unittest.TestCase):
    @contextmanager
    def generate_mock_islink(self, value):
        with patch.object(install, 'islink', return_value=value) as islink:
            yield islink

    @contextmanager
    def generate_mock_isdir(self, value):
        with patch.object(install, 'isdir', return_value=value) as isdir:
            yield isdir

    @contextmanager
    def generate_mock_isfile(self, value):
        with patch.object(install, 'isfile', return_value=value) as isfile:
            yield isfile

    @contextmanager
    def generate_mock_unlink(self):
        with patch.object(install.os, 'unlink') as unlink:
            yield unlink

    @contextmanager
    def generate_mock_rmtree(self):
        with patch.object(install.shutil, 'rmtree') as rmtree:
            yield rmtree

    @contextmanager
    def generate_mock_sleep(self):
        with patch.object(install.time, 'sleep') as sleep:
            yield sleep

    @contextmanager
    def generate_mock_log(self):
        with patch.object(install, 'log') as log:
            yield log

    @contextmanager
    def generate_mock_on_win(self, value):
        original = install.on_win
        install.on_win = value
        yield
        install.on_win = original

    @contextmanager
    def generate_mock_check_call(self):
        with patch.object(install.subprocess, 'check_call') as check_call:
            yield check_call

    @contextmanager
    def generate_mocks(self, islink=True, isfile=True, isdir=True, on_win=False):
        with self.generate_mock_islink(islink) as mock_islink:
            with self.generate_mock_isfile(isfile) as mock_isfile:
                with self.generate_mock_isdir(isdir) as mock_isdir:
                    with self.generate_mock_unlink() as mock_unlink:
                        with self.generate_mock_rmtree() as mock_rmtree:
                            with self.generate_mock_sleep() as mock_sleep:
                                with self.generate_mock_log() as mock_log:
                                    with self.generate_mock_on_win(on_win):
                                        with self.generate_mock_check_call() as check_call:
                                            yield {
                                                'islink': mock_islink,
                                                'isfile': mock_isfile,
                                                'isdir': mock_isdir,
                                                'unlink': mock_unlink,
                                                'rmtree': mock_rmtree,
                                                'sleep': mock_sleep,
                                                'log': mock_log,
                                                'check_call': check_call,
                                            }

    def generate_directory_mocks(self, on_win=False):
        return self.generate_mocks(islink=False, isfile=False, isdir=True,
                                   on_win=on_win)

    def generate_all_false_mocks(self):
        return self.generate_mocks(False, False, False)

    @property
    def generate_random_path(self):
        return generate_random_path()

    @skip_if_no_mock
    def test_calls_islink(self):
        with self.generate_mocks() as mocks:
            some_path = self.generate_random_path
            install.rm_rf(some_path)
        mocks['islink'].assert_called_with(some_path)

    @skip_if_no_mock
    def test_calls_unlink_on_true_islink(self):
        with self.generate_mocks() as mocks:
            some_path = self.generate_random_path
            install.rm_rf(some_path)
        mocks['unlink'].assert_called_with(some_path)

    @skip_if_no_mock
    def test_does_not_call_isfile_if_islink_is_true(self):
        with self.generate_mocks() as mocks:
            some_path = self.generate_random_path
            install.rm_rf(some_path)
        self.assertFalse(mocks['isfile'].called)

    @skip_if_no_mock
    def test_calls_isfile_with_path(self):
        with self.generate_mocks(islink=False, isfile=True) as mocks:
            some_path = self.generate_random_path
            install.rm_rf(some_path)
        mocks['isfile'].assert_called_with(some_path)

    @skip_if_no_mock
    def test_calls_unlink_on_false_islink_and_true_isfile(self):
        with self.generate_mocks(islink=False, isfile=True) as mocks:
            some_path = self.generate_random_path
            install.rm_rf(some_path)
        mocks['unlink'].assert_called_with(some_path)

    @skip_if_no_mock
    def test_does_not_call_unlink_on_false_values(self):
        with self.generate_mocks(islink=False, isfile=False) as mocks:
            some_path = self.generate_random_path
            install.rm_rf(some_path)
        self.assertFalse(mocks['unlink'].called)

    @skip_if_no_mock
    def test_does_not_call_shutil_on_false_isdir(self):
        with self.generate_all_false_mocks() as mocks:
            some_path = self.generate_random_path
            install.rm_rf(some_path)
        self.assertFalse(mocks['rmtree'].called)

    @skip_if_no_mock
    def test_calls_rmtree_at_least_once_on_isdir_true(self):
        with self.generate_directory_mocks() as mocks:
            some_path = self.generate_random_path
            install.rm_rf(some_path)
        mocks['rmtree'].assert_called_with(some_path)

    @skip_if_no_mock
    def test_calls_rmtree_only_once_on_success(self):
        with self.generate_directory_mocks() as mocks:
            some_path = self.generate_random_path
            install.rm_rf(some_path)
        self.assertEqual(1, mocks['rmtree'].call_count)

    @skip_if_no_mock
    def test_raises_final_exception_if_it_cant_remove(self):
        with self.generate_directory_mocks() as mocks:
            mocks['rmtree'].side_effect = OSError
            some_path = self.generate_random_path
            with self.assertRaises(OSError):
                install.rm_rf(some_path)

    @skip_if_no_mock
    def test_retries_six_times_to_ensure_it_cant_really_remove(self):
        with self.generate_directory_mocks() as mocks:
            mocks['rmtree'].side_effect = OSError
            some_path = self.generate_random_path
            with self.assertRaises(OSError):
                install.rm_rf(some_path)
        self.assertEqual(6, mocks['rmtree'].call_count)

    @skip_if_no_mock
    def test_retries_as_many_as_max_retries_plus_one(self):
        max_retries = random.randint(7, 10)
        with self.generate_directory_mocks() as mocks:
            mocks['rmtree'].side_effect = OSError
            some_path = self.generate_random_path
            with self.assertRaises(OSError):
                install.rm_rf(some_path, max_retries=max_retries)
        self.assertEqual(max_retries + 1, mocks['rmtree'].call_count)

    @skip_if_no_mock
    def test_stops_retrying_after_success(self):
        with self.generate_directory_mocks() as mocks:
            mocks['rmtree'].side_effect = [OSError, OSError, None]
            some_path = self.generate_random_path
            install.rm_rf(some_path)
        self.assertEqual(3, mocks['rmtree'].call_count)

    @skip_if_no_mock
    def test_pauses_for_same_number_of_seconds_as_max_retries(self):
        with self.generate_directory_mocks() as mocks:
            mocks['rmtree'].side_effect = OSError
            max_retries = random.randint(1, 10)
            with self.assertRaises(OSError):
                install.rm_rf(self.generate_random_path,
                              max_retries=max_retries)

        expected = [mock.call(i) for i in range(max_retries)]
        mocks['sleep'].assert_has_calls(expected)

    @skip_if_no_mock
    def test_logs_messages_generated_for_each_retry(self):
        with self.generate_directory_mocks() as mocks:
            random_path = self.generate_random_path
            mocks['rmtree'].side_effect = OSError(random_path)
            max_retries = random.randint(1, 10)
            with self.assertRaises(OSError):
                install.rm_rf(random_path, max_retries=max_retries)

        log_template = "\n".join([
            "Unable to delete %s" % random_path,
            "%s" % OSError(random_path),
            "Retrying after %d seconds...",
        ])

        expected_call_list = [mock.call(log_template % i)
                              for i in range(max_retries)]
        mocks['log'].debug.assert_has_calls(expected_call_list)

    @skip_if_no_mock
    def test_tries_extra_kwarg_on_windows(self):
        with self.generate_directory_mocks(on_win=True) as mocks:
            random_path = self.generate_random_path
            mocks['rmtree'].side_effect = [OSError, None]
            install.rm_rf(random_path)

        expected_call_list = [
            mock.call(random_path),
            mock.call(random_path, onerror=install._remove_readonly)
        ]
        mocks['rmtree'].assert_has_calls(expected_call_list)
        self.assertEqual(2, mocks['rmtree'].call_count)


if __name__ == '__main__':
    unittest.main()
