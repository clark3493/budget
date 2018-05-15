import pathmagic
from datetime import date
import os
import unittest
from config import TestConfig
from parser_bofa import BofAParser


class BofAParserTestCase(unittest.TestCase):
    """
    DESCRIPTION
    """
    def setUp(self):
        """
        Stores the file path to a test statement and defines
        a parser object
        """
        filepath = os.path.join(TestConfig.DB_DIR, 'statements', 'test', 'BofACoreCheckingTest.csv')
        self.parser = BofAParser(filepath)

    def test_parse_statement(self):
        transactions = self.parser.parse_statement()
        actual = [transactions[0], transactions[-1]]
        expected = [(date(2016, 10, 26), 'Beginning balance as of 10/26/2016', None, 2223.70),
                    (date(2016, 11, 23), 'TRANSACTION99', -59.34, 2305.45)]
        self.assertEqual(expected, actual)

    def test_read_transaction(self):
        line = ['10/26/2016', 'DummyDescription', '-4.50', '125.07']
        actual = self.parser.read_transaction(line)
        expected = (date(2016, 10, 26), 'DummyDescription', -4.50, 125.07)
        self.assertEqual(expected, actual)

    def tearDown(self):
        pass