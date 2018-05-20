import pathmagic
import unittest
from test_database import DatabaseTestCase
from test_database_budget import BudgetDatabaseTestCase
from test_parser_bofa import BofAParserTestCase
from test_string_filter import StringFilterTestCase
from test_table import TableTestCase


def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(StringFilterTestCase))
    test_suite.addTest(unittest.makeSuite(TableTestCase))
    test_suite.addTest(unittest.makeSuite(DatabaseTestCase))
    test_suite.addTest(unittest.makeSuite(BudgetDatabaseTestCase))
    test_suite.addTest(unittest.makeSuite(BofAParserTestCase))
    return test_suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())

