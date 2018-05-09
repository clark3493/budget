import pathmagic  # noqa
import os
import unittest
from baseline import baseline_tables
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
        expected = (1, -25., 1, None, None, None, None, None, None)
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

    def test_add_expense_recipient(self):
        self.db.add_expense_recipient("TestRecipient")
        self.db.sql_cmd("SELECT * FROM ExpenseRecipient WHERE Name='TestRecipient'")
        actual = self.db._cursor.fetchall()[0][:-1]
        expected = (1, 'TestRecipient')
        self.assertEqual(expected, actual)

    def test_add_expense_recipient_alias(self):
        self.db.add_expense_recipient("TestRecipient")
        self.db.add_expense_recipient("TestRecipient2")
        self.db.add_expense_recipient_alias("TestRecipient2","Alias")
        self.db.sql_cmd("SELECT * FROM ExpenseRecipientAlias")
        actual = self.db._cursor.fetchall()[0][:-1]
        expected = (1, 2, "Alias", "CONTAINS")
        self.assertEqual(expected, actual)

    def test_add_expense_subcategory(self):
        self.db.add_expense_category("Food")
        self.db.add_expense_subcategory("Pizza", "Food")
        actual = self.db.get("*","ExpenseSubCategory")[0][:-1]
        expected = (1, "Pizza", 1)
        self.assertEqual(expected, actual)

    def test_add_expense_subcategory_without_parent_raises_value_error(self):
        self.assertRaises(ValueError, self.db.add_expense_subcategory, "Pizza", "Food")

    def test_add_expense_to_new_account_raises_value_error(self):
        self.assertRaises(ValueError, self.db.add_expense, "TestAccount", 1)

    def test_add_income(self):
        self.db.add_account("TestAccount", 100.)
        self.db.add_income(25, "TestAccount")
        self.db.sql_cmd("SELECT * FROM Income WHERE Account=1")
        actual = self.db._cursor.fetchall()
        expected = (1, 25., 1, None, None, None, None)
        self.assertEqual(expected, actual[0][:-1])

    def test_add_income_category(self):
        self.db.add_income_category("Salary")
        actual = self.db.get("*", "IncomeCategory")[0][:-1]
        expected = (1, "Salary")
        self.assertEqual(expected, actual)

    def test_add_income_increments_account(self):
        self.db.add_account("TestAccount", 100.)
        self.db.add_expense(25, "TestAccount")
        self.db.sql_cmd("SELECT Balance FROM Account WHERE Name='TestAccount'")
        actual = self.db._cursor.fetchall()
        expected = 125.
        self.assertEqual(expected, actual[0][0])

    def test_add_income_source(self):
        self.db.add_income_source("Source")
        actual = self.db.get("*", "IncomeSource")[0][:-1]
        expected = (1, "Source")
        self.assertEqual(expected, actual)

    def test_add_income_subcategory(self):
        self.db.add_income_category("Salary")
        self.db.add_income_subcategory("Job1", "Salary")
        actual = self.db.get("*", "IncomeSubCategory")[0][:-1]
        expected = (1, "Job1", 1)
        self.assertEqual(expected, actual)

    def test_add_income_subcategory_without_parent_raises_value_error(self):
        self.assertRaises(ValueError, self.db.add_income_subcategory, "Job1", "Salary")

    def test_add_income_to_new_account_raises_value_error(self):
        self.assertRaises(ValueError, self.db.add_income, "TestAccount", 1)

    def test_add_invalid_alias_type_raises_value_error(self):
        self.assertRaises(ValueError, self.db.add_expense_recipient_alias,
                          "Rec", "Alias", "NOT A TYPE")

    def test_add_payment_type(self):
        self.db.add_payment_type("TestType")
        self.db.sql_cmd("SELECT * FROM PaymentType WHERE Name='TestType'")
        actual = self.db._cursor.fetchall()[0][:-1]
        expected = (1, "TestType")
        self.assertEqual(expected, actual)

    def tearDown(self):
        """
        Delete the temporary database
        """
        self.db.disconnect()
        os.remove(self.db.DB_DIR + '\\' + self.db.DATABASE_URI + '.db')

