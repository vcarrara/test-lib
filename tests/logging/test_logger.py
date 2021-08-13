import logging
import os
import pytest
import unittest
from olympuslib.logging.logger import OlympusLogger
from typing import List


CUSTOM_PATH = '__OLYMPUS_PYTEST__'


@pytest.fixture(scope="class")
def delete_file_after_test():
    yield
    os.remove(CUSTOM_PATH)

class TestName(unittest.TestCase):
    def test_name_is_correct(self):
        """
        When a custom name is specified it should be applied the logger
        """
        name = 'OLYMPUS_TEST_LOGGER'
        logger = OlympusLogger(name=name)
        self.assertEqual(name, logger.name)


@pytest.mark.usefixtures('delete_file_after_test')
class TestFormat(unittest.TestCase):
    def test_format_is_correct(self):
        """
        When a custom format is specified it should be applied to every handler of the logger
        """
        format = "%(message)s (%(asctime)s)"
        logger = OlympusLogger(log_to_stdout=True, log_to_file=True, file_path=CUSTOM_PATH, format=format)
        for handler in logger.handlers:
            self.assertEqual(handler.formatter._fmt, format)


@pytest.mark.usefixtures('delete_file_after_test')
class TestLevel(unittest.TestCase):
    def test_level_is_correct(self):
        """
        When a custom level is specified it should be applied to every handler of the logger and to the logger itself
        """
        level = logging.CRITICAL
        logger = OlympusLogger(log_to_stdout=True, log_to_file=True, file_path=CUSTOM_PATH, level=level)
        self.assertEqual(logger.level, level)
        for handler in logger.handlers:
            self.assertEqual(handler.level, level)


class TestNoHandler(unittest.TestCase):
    def test_no_handler(self):
        """
        Length of handlers must be 0 when log_to_file and log_to_stdout are False
        """
        logger = OlympusLogger(log_to_file=False, log_to_stdout=False)
        self.assertEqual(len(logger.handlers), 0)


class TestStreamHandlerOnly(unittest.TestCase):
    def test_stdout_only_param(self):
        """
        Length of handlers must be 1 when only log_to_stdout is True
        The handler must be an instance of StreamHandler
        """
        logger = OlympusLogger(log_to_stdout=True)
        self.assertEqual(len(logger.handlers), 1)
        self.assertIsInstance(logger.handlers[0], logging.StreamHandler)

    def test_stdout_only_no_param(self):
        """
        Length of handlers must be 1 when no parameter is set
        The handler must be an instance of StreamHandler
        """
        logger = OlympusLogger()
        self.assertEqual(len(logger.handlers), 1)
        self.assertIsInstance(logger.handlers[0], logging.StreamHandler)


@pytest.mark.usefixtures('delete_file_after_test')
class TestFileHandlerOnly(unittest.TestCase):
    def test_custom_path(self):
        """
        Length of handlers must be 1 when log_to_file is True, a file_path is set and if log_to_stdout is expressly False
        The handler must be an instance of FileHandler
        The path of the FileHandler must be the one set by params
        """
        logger = OlympusLogger(log_to_stdout=False, log_to_file=True, file_path=CUSTOM_PATH)
        self.assertEqual(len(logger.handlers), 1)
        file_handler = logger.handlers[0]
        self.assertIsInstance(file_handler, logging.FileHandler)
        self.assertTrue(file_handler.baseFilename.endswith(CUSTOM_PATH))

    def test_no_file_path(self):
        """
        A ValueError should be raised if the parameter log_to_file is True but no file_path is set
        Length of handlers should be 0
        """
        with self.assertRaises(ValueError):
            logger = OlympusLogger(log_to_file=True)
            self.assertEqual(len(logger.handlers), 0)


@pytest.mark.usefixtures('delete_file_after_test')
class TestBothHandlers(unittest.TestCase):
    def count_handlers(self, handlers: List[logging.Handler]):
        nb_of_stream_handlers = 0
        nb_of_file_handlers = 0
        for handler in handlers:
            if isinstance(handler, logging.FileHandler):
                nb_of_file_handlers = nb_of_file_handlers + 1
                continue

            if isinstance(handler, logging.StreamHandler):
                nb_of_stream_handlers = nb_of_stream_handlers + 1
                continue
        return nb_of_stream_handlers, nb_of_file_handlers

    def test_both(self):
        """
        Length of handlers must be 2 when log_to_file is True and a file_path is set
        There must be one FileHandler and one StreamHandler in the handlers list
        """
        logger = OlympusLogger(log_to_file=True, file_path=CUSTOM_PATH)
        self.assertEqual(len(logger.handlers), 2)

        nb_of_stream_handlers, nb_of_file_handlers = self.count_handlers(logger.handlers)
        self.assertEqual(nb_of_stream_handlers, 1)
        self.assertEqual(nb_of_file_handlers, 1)

    def test_both_express(self):
        """
        Length of handlers must be 2 when log_to_file is True, log_to_stdout is True and a file_path is set
        There must be one FileHandler and one StreamHandler in the handlers listThere must be one FileHandler and one StreamHandler in the handlers list
        """
        logger = OlympusLogger(log_to_stdout=True, log_to_file=True, file_path=CUSTOM_PATH)
        self.assertEqual(len(logger.handlers), 2)

        nb_of_stream_handlers, nb_of_file_handlers = self.count_handlers(logger.handlers)
        self.assertEqual(nb_of_stream_handlers, 1)
        self.assertEqual(nb_of_file_handlers, 1)
