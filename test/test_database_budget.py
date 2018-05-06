import pathmagic  # noqa
import os
import unittest
from baseline import *
from config import TestConfig
from database_budget import BudgetDatabase


class BudgetDatabaseTestCase(unittest.TestCase):
    """
    DESCRIPTION
    """
    def setUp(self):
        """
        Create a temporary database for testing
        """
        self.db = BudgetDatabase(TestConfig)
        self.db.AUTO_DISCONNECT = False
        for tbl in baseline_tables():
            self.db.sql_cmd(tbl.create_cmd())

    def test_add_account(self):
        self.db.add_account("TestAccount", 0.)
        self.db.sql_cmd("SELECT * FROM Account")
        actual = self.db._cursor.fetchall()
        expected = (1, 'TestAccount', 0.)
        self.assertEqual(expected, actual[0][:-1])

    def test_add_expense(self):
        self.db.add_account("TestAccount", 100.)
        self.db.add_expense(-25, "TestAccount")
        self.db.sql_cmd("SELECT * FROM Expense WHERE Account=1")
        actual = self.db._cursor.fetchall()
        expected = (1, -25, 1, None, None, None, None, None, None)
        self.assertEqual(expected, actual[0][:-1])

    def test_add_expense_category(self):
        self.db.add_expense_category("Food")
        actual = self.db.get("*", "ExpenseCategory")[0][:-1]
        expected = (1, "Food")
        self.assertEqual(expected, actual)

    def test_add_expense_debits_account(self):
        self.db.add_account("TestAccount", 100.)
        self.db.add_expense(-25, "TestAccount")
        self.db.sql_cmd("SELECT Balance FROM Account WHERE Name='TestAccount'")
        actual = self.db._cursor.fetchall()
        expected = 75.
        self.assertEqual(expected, actual[0][0])

    def test_add_expense_to_new_account_raises_value_error(self):
        """
        DESCRIPTION
        """
        self.assertRaises(ValueError, self.db.add_expense, "TestAccount", 1)

    def test_add_expense_subcategory(self):
        self.db.add_expense_category("Food")
        self.db.add_expense_subcategory("Pizza", "Food")
        actual = self.db.get("*","ExpenseSubCategory")[0][:-1]
        expected = (1, "Pizza", 1)
        self.assertEqual(expected, actual)

    def test_add_expense_subcategory_without_parent_raises_value_error(self):
        self.assertRaises(ValueError, self.db.add_expense_subcategory, "Pizza", "Food")

    def tearDown(self):
        """
        Delete the temporary database
        """
        self.db.disconnect()
        os.remove(self.db.DB_DIR + '\\' + self.db.DATABASE_URI + '.db')

