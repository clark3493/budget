from src.interface.cli.database_budget_cli import BudgetDatabaseCLI
import os
import unittest
from config import TestConfig


class BudgetDatabaseCLITestCase(unittest.TestCase):
    def setUp(self):
        self.cli = BudgetDatabaseCLI(TestConfig)
        self.cli.AUTO_DISCONNECT = False

    def test_main(self):
        self.cli.main()
        self.assertTrue(True)

    def tearDown(self):
        self.cli.disconnect()
        os.remove(self.cli.DB_DIR + '\\' + self.cli.DATABASE_URI + '.db')