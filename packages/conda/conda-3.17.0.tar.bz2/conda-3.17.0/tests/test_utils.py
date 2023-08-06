import random
import unittest

from .decorators import skip_if_no_mock
from .helpers import mock

from conda import utils

SOME_PREFIX = "/some/prefix"
SOME_FILES = ["a", "b", "c"]


def create_mock_open():
    return mock.patch.object(utils, "open", create=True)


def create_mock_can_open():
    can_open = mock.patch.object(utils, "can_open")
    can_open.return_value = True
    return can_open


class can_open_TestCase(unittest.TestCase):
    @skip_if_no_mock
    def test_returns_true_if_can_open(self):
        with create_mock_open():
            self.assertTrue(utils.can_open("/some/path/some/file"))

    @skip_if_no_mock
    def test_returns_false_if_unable_to_open(self):
        with create_mock_open() as o:
            o.side_effect = IOError
            self.assertFalse(utils.can_open("/some/path/some/file"))

    @skip_if_no_mock
    def test_logs_file_to_debug_log(self):
        random_file = "/some/path/to/a/file/%s" % random.randint(100, 200)
        with create_mock_open() as o:
            o.side_effect = IOError
            with mock.patch.object(utils, "stderrlog") as log:
                utils.can_open(random_file)
        log.info.assert_called_with("Unable to open %s\n" % random_file)

    @skip_if_no_mock
    def test_closes_file_handler_if_successful(self):
        with create_mock_open() as o:
            utils.can_open("/some/file")
        o.assert_has_calls([
            mock.call("/some/file", "ab"),
            mock.call().close(),
        ])


class can_open_all_TestCase(unittest.TestCase):
    @skip_if_no_mock
    def test_returns_true_if_all_files_are_openable(self):
        with create_mock_can_open():
            self.assertTrue(utils.can_open_all([
                "/some/path/a",
                "/some/path/b",
            ]))

    @skip_if_no_mock
    def test_returns_false_if_not_all_files_are_opened(self):
        with create_mock_can_open() as can_open:
            can_open.return_value = False
            self.assertFalse(utils.can_open_all([
                "/some/path/a",
                "/some/path/b",
            ]))

    @skip_if_no_mock
    def test_only_call_can_open_as_many_times_as_needed(self):
        with create_mock_can_open() as can_open:
            can_open.side_effect = [True, False, True]
            self.assertFalse(utils.can_open_all([
                "/can/open",
                "/cannot/open",
                "/can/open",
            ]))
        self.assertEqual(can_open.call_count, 2)


class can_open_all_files_in_prefix_TestCase(unittest.TestCase):
    @skip_if_no_mock
    def test_returns_true_on_success(self):
        with create_mock_open():
            self.assertTrue(utils.can_open_all_files_in_prefix(SOME_PREFIX, SOME_FILES))

    @skip_if_no_mock
    def test_returns_false_if_unable_to_open_file_for_writing(self):
        with create_mock_open() as o:
            o.side_effect = IOError
            self.assertFalse(utils.can_open_all_files_in_prefix(SOME_PREFIX, SOME_FILES))

    @skip_if_no_mock
    def test_dispatches_to_can_can_call(self):
        with mock.patch.object(utils, "can_open_all") as can_open_all:
            utils.can_open_all_files_in_prefix(SOME_PREFIX, SOME_FILES)
        self.assertTrue(can_open_all.called)

    @skip_if_no_mock
    def test_tries_to_open_all_files(self):
        random_files = ['%s' % i for i in range(random.randint(10, 20))]
        with create_mock_can_open():
            utils.can_open_all_files_in_prefix(SOME_PREFIX, random_files)

    @skip_if_no_mock
    def test_stops_checking_as_soon_as_the_first_file_fails(self):
        with create_mock_can_open() as can_open:
            can_open.side_effect = [True, False, True]
            self.assertFalse(
                utils.can_open_all_files_in_prefix(SOME_PREFIX, SOME_FILES)
            )
        self.assertEqual(can_open.call_count, 2)
