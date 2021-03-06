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

    def populate_categories(self):
        """
        Add bare minimum categories to the Category and SubCategory
        tables for use in budget database functions
        """
        self.db.add_category("Personal")
        self.db.add_category("External")

    def test_add_account(self):
        self.db.add_account("TestAccount", "Personal", 0.)
        self.db.sql_cmd("SELECT * FROM Account")
        actual = self.db._cursor.fetchall()
        expected = (1, 'TestAccount', "Personal", 0.)
        self.assertEqual(expected, actual[0][:-1])

    def test_add_account_attribute(self):
        self.db.add_account("TestAccount", "Personal", 0.)
        self.db.add_account("TestAccount2", "Personal", 0.)
        self.db.add_attribute('TestAttribute')
        self.db.add_account_attribute('TestAccount2', 'TestAttribute')
        actual = self.db.get('*', 'AccountAttribute')[0]
        expected = (2, 1)
        self.assertEqual(expected, actual)

    def test_add_alias(self):
        self.db.add_account("TestAccount", "Personal", 0.)
        self.db.add_account("TestAccount2", "Personal", 0.)
        self.db.add_alias('TestAccount2', 'Alias', 'Contains')
        actual = self.db.get('*', 'Alias')[0][:-2]
        expected = (1, 2, 'Alias', 'Contains')
        self.assertEqual(expected, actual)

    def test_add_attribute(self):
        self.db.add_attribute('TestAttribute')
        actual = self.db.get('*', 'Attribute')[0][:-1]
        expected = (1, 'TestAttribute')
        self.assertEqual(expected, actual)

    def test_add_category(self):
        self.db.add_category("TestCategory")
        actual = self.db.get('*', 'Category')[0][:-1]
        expected = (1, 'TestCategory')
        self.assertEqual(expected, actual)

    def test_add_expense(self):
        self.db.add_account("TestAccount", "Personal", 0.)
        self.db.add_expense(-25., "TestAccount")
        actual = self.db.get('*', 'Transactions')[0][:-2]
        expected = (1, -25., 1, None, 'Expense', None, None, None, None, None)
        self.assertEqual(expected, actual)

    def test_add_income(self):
        self.db.add_account("TestAccount", "Personal", 0.)
        self.db.add_income(25., "TestAccount")
        actual = self.db.get('*', 'Transactions')[0][:-2]
        expected = (1, 25., None, 1, 'Income', None, None, None, None, None)
        self.assertEqual(expected, actual)

    def test_add_subcategory(self):
        self.db.add_category("TestCategory")
        self.db.add_subcategory("TestSubCategory", "TestCategory")
        actual = self.db.get('*', 'SubCategory')[0][:-1]
        expected = (1, 'TestSubCategory', 1)
        self.assertEqual(expected, actual)

    def test_add_transaction(self):
        self.db.add_account('TestAccount', 'Personal', 0.)
        self.db.add_transaction(-25., 'TestAccount', transaction_type='Expense')
        actual = self.db.get('*', 'Transactions')[0][:-2]
        expected = (1, -25., 1, None, 'Expense', None, None, None, None, None)
        self.assertEqual(expected, actual)

    def test_add_transaction_category(self):
        self.db.add_account('TestAccount', 'Personal', 0.)
        self.db.add_transaction(-25., 'TestAccount', transaction_type='Expense')
        self.db.add_category("TestCategory")
        transaction_id = self.db.get_last_entry('Transactions')[0]
        self.db.add_transaction_category(transaction_id, 'TestCategory')
        actual = self.db.get('*', 'TransactionCategory')[0]
        expected = (1, 1)
        self.assertEqual(expected, actual)

    def test_add_transaction_subcategory(self):
        self.db.add_account('TestAccount', 'Personal', 0.)
        self.db.add_transaction(-25., 'TestAccount', transaction_type='Expense')
        self.db.add_category("TestCategory")
        self.db.add_subcategory("TestSubCategory", "TestCategory")
        transaction_id = self.db.get_last_entry('Transactions')[0]
        self.db.add_transaction_subcategory(transaction_id, 'TestSubCategory')
        actual = self.db.get('*', 'TransactionSubCategory')[0]
        expected = (1, 1)
        self.assertEqual(expected, actual)

    def test_build_baseline_tables(self):
        tables = self.db.get('name', 'sqlite_master', "type='table'")
        expected = [('Account',),
                    ('AccountAttribute',),
                    ('Alias',),
                    ('Attribute',),
                    ('Category',),
                    ('SubCategory',),
                    ('Transactions',),
                    ('TransactionCategory',),
                    ('TransactionSubCategory',)]
        self.assertEqual(expected, tables)

    def tearDown(self):
        """
        Delete the temporary database
        """
        self.db.disconnect()
        os.remove(self.db.DB_DIR + '\\' + self.db.DATABASE_URI + '.db')

