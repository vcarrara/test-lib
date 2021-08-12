import logging
import os
import pytest
import unittest
from olympuslib.logging.logger import OlympusLogger


CUSTOM_PATH = '__OLYMPUS_PYTEST__'


@pytest.fixture(scope="class")
def delete_file_after_test():
    yield
    os.remove(CUSTOM_PATH)


class TestNoHandler(unittest.TestCase):
    def test_no_handler(self):
        logger = OlympusLogger(log_to_file=False, log_to_stdout=False)
        self.assertEqual(len(logger.handlers), 0)


class TestStreamHandlerOnly(unittest.TestCase):
    def test_stdout_only(self):
        logger = OlympusLogger(log_to_stdout=True)
        self.assertEqual(len(logger.handlers), 1)
        self.assertIsInstance(logger.handlers[0], logging.StreamHandler)

        logger = OlympusLogger()
        self.assertEqual(len(logger.handlers), 1)
        self.assertIsInstance(logger.handlers[0], logging.StreamHandler)


@pytest.mark.usefixtures('delete_file_after_test')
class TestFileHandlerOnly(unittest.TestCase):
    def test_custom(self):
        logger = OlympusLogger(log_to_stdout=False, log_to_file=True, file_path=CUSTOM_PATH)
        self.assertEqual(len(logger.handlers), 1)
        file_handler = logger.handlers[0]
        self.assertIsInstance(file_handler, logging.FileHandler)
        self.assertTrue(file_handler.baseFilename.endswith(CUSTOM_PATH))

    def test_no_file_path(self):
        with self.assertRaises(ValueError):
            logger = OlympusLogger(log_to_file=True)
            self.assertEqual(len(logger), 0)


@pytest.mark.usefixtures('delete_file_after_test')
class TestBothHandlers(unittest.TestCase):
    def test_both(self):
        logger = OlympusLogger(log_to_file=True, file_path=CUSTOM_PATH)
        self.assertEqual(len(logger.handlers), 2)

        logger = OlympusLogger(log_to_stdout=True, log_to_file=True, file_path=CUSTOM_PATH)
        self.assertEqual(len(logger.handlers), 2)
