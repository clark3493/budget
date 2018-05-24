import pathmagic  # noqa
import contextlib
import logging
import os
import sqlite3
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
        self.db.add_account("TestAccount", 0., '10/23/2016')
        self.db.sql_cmd("SELECT * FROM Account")
        actual = self.db._cursor.fetchall()
        expected = (1, 'TestAccount', 0., '10/23/2016')
        self.assertEqual(expected, actual[0][:-1])

    def test_add_account_attribute(self):
        self.db.add_account("TestAccount", 0., '10/23/2016')
        self.db.add_account("TestAccount2", 0., '10/23/2016')
        self.db.add_attribute('TestAttribute')
        self.db.add_account_attribute('TestAccount2', 'TestAttribute')
        actual = self.db.get('*', 'AccountAttribute')[0]
        expected = (2, 1)
        self.assertEqual(expected, actual)

    def test_add_alias_for_category(self):
        self.db.add_category('TestCategory')
        self.db.add_category('TestSubCategory', 'TestCategory')
        self.db.add_alias('AliasString', 'CONTAINS', 'TestSubCategory')
        actual = self.db.get('*', 'Alias')[0][:-2]
        expected = (1, 2, None, 'AliasString', 'CONTAINS')
        self.assertEqual(expected, actual)

    def test_add_alias_for_merchant(self):
        self.db.add_merchant('TestMerchant')
        self.db.add_alias('AliasString', 'CONTAINS', None, 'TestMerchant')
        actual = self.db.get('*', 'Alias')[0][:-2]
        expected = (1, None, 1, 'AliasString', 'CONTAINS')
        self.assertEqual(expected, actual)

    def test_add_alias_with_no_subcategory_or_merchant_raises_sqlite_error(self):
        self.assertRaises(sqlite3.IntegrityError, self.db.add_alias, 'AliasString', 'CONTAINS')

    def test_add_attribute(self):
        self.db.add_attribute('TestAttribute')
        actual = self.db.get('*', 'Attribute')[0][:-1]
        expected = (1, 'TestAttribute')
        self.assertEqual(expected, actual)

    def test_add_category(self):
        self.db.add_category("TestCategory")
        actual = self.db.get('*', 'Category')[0][:-1]
        expected = (1, 'TestCategory', None)
        self.assertEqual(expected, actual)

    def test_add_expense(self):
        self.db.add_account("TestAccount", 0., '10/23/2016')
        self.db.add_expense(-25., "TestAccount")
        actual = self.db.get('*', 'Transactions')[0][:-2]
        expected = (1, -25., 1, None, 'Expense', None, None, None)
        self.assertEqual(expected, actual)

    def test_add_income(self):
        self.db.add_account("TestAccount", 0., '10/23/2016')
        self.db.add_income(25., "TestAccount")
        actual = self.db.get('*', 'Transactions')[0][:-2]
        expected = (1, 25., None, 1, 'Income', None, None, None)
        self.assertEqual(expected, actual)

    def test_add_merchant(self):
        self.db.add_merchant('Employer')
        actual = self.db.get('*', 'Merchant')[0][:-1]
        expected = (1, 'Employer')
        self.assertEqual(expected, actual)

    def test_add_subcategory(self):
        self.db.add_category("TestCategory")
        self.db.add_category("TestSubCategory", "TestCategory")
        actual = self.db.get('*', 'Category', where="Name='TestSubCategory'")[0][:-1]
        expected = (2, 'TestSubCategory', 1)
        self.assertEqual(expected, actual)

    def test_add_transaction(self):
        self.db.add_account('TestAccount', 0., '10/23/2016')
        self.db.add_transaction(-25., 'TestAccount', transaction_type='Expense')
        actual = self.db.get('*', 'Transactions')[0][:-2]
        expected = (1, -25., 1, None, 'Expense', None, None, None)
        self.assertEqual(expected, actual)

    def test_add_transaction_category(self):
        self.db.add_account('TestAccount', 0., '10/23/2016')
        self.db.add_transaction(-25., 'TestAccount', transaction_type='Expense')
        self.db.add_category("TestCategory")
        transaction_id = self.db.get_last_entry('Transactions')[0]
        self.db.add_transaction_category(transaction_id, 'TestCategory')
        actual = self.db.get('*', 'TransactionCategory')[0]
        expected = (1, 1)
        self.assertEqual(expected, actual)

    def test_build_baseline_tables(self):
        tables = self.db.get('name', 'sqlite_master', where="type='table'")
        expected = [('Account',),
                    ('AccountAttribute',),
                    ('Alias',),
                    ('Attribute',),
                    ('Category',),
                    ('Merchant',),
                    ('Transactions',),
                    ('TransactionCategory',)]
        self.assertEqual(expected, tables)

    def test_get_category_id_from_description(self):
        self.db.add_category('TestCategory')
        self.db.add_category('TestCategory2', 'TestCategory')
        self.db.add_alias('SomeString', 'CONTAINS', category='TestCategory2')
        actual = self.db.get_category_id_from_description('WordsSomeStringWords')
        expected = 2
        self.assertEqual(expected, actual)

    def test_get_category_id_from_description_multiple_aliases_returns_id(self):
        with contextlib.redirect_stdout(None):
            self.db.add_category('TestCategory')
            self.db.add_category('TestCategory2')
            self.db.add_alias('SomeString', 'CONTAINS', category='TestCategory')
            self.db.add_alias('SomeString2', 'CONTAINS', category='TestCategory2')
            actual = self.db.get_category_id_from_description('WordsSomeString2Words')
            expected = 1
            self.assertEqual(expected, actual)

    def test_get_category_id_from_description_multiple_categories_logs_warning(self):
        with contextlib.redirect_stdout(None):
            self.db.add_category('TestCategory')
            self.db.add_category('TestCategory2')
            self.db.add_alias('SomeString', 'CONTAINS', category='TestCategory')
            self.db.add_alias('SomeString2', 'CONTAINS', category='TestCategory2')
            self.db.get_category_id_from_description('WordsSomeString2Words')
            self.assertLogs(self.db.logger, logging.WARNING)

    def test_get_category_id_from_description_none_logs_info(self):
        self.db.get_category_id_from_description('SomeString')
        self.assertLogs(self.db.logger, logging.INFO)

    def test_get_category_id_from_description_none_returns_none(self):
        actual = self.db.get_category_id_from_description('SomeString')
        expected = None
        self.assertEqual(expected, actual)

    def test_get_merchant_id_from_description_contains(self):
        self.db.add_merchant('TestMerchant')
        self.db.add_merchant('TestMerchant2')
        self.db.add_alias('SomeString', 'CONTAINS', merchant='TestMerchant2')
        actual = self.db.get_merchant_id_from_description('WordsSomeStringWords')
        expected = 2
        self.assertEqual(expected, actual)

    def test_get_merchant_id_from_description_endswith(self):
        self.db.add_merchant('TestMerchant')
        self.db.add_merchant('TestMerchant2')
        self.db.add_alias('SomeString', 'ENDSWITH', merchant='TestMerchant2')
        actual = self.db.get_merchant_id_from_description('WordsSomeString')
        expected = 2
        self.assertEqual(expected, actual)

    def test_get_merchant_id_from_description_equals(self):
        self.db.add_merchant('TestMerchant')
        self.db.add_merchant('TestMerchant2')
        self.db.add_alias('SomeString', 'EQUALS', merchant='TestMerchant2')
        actual = self.db.get_merchant_id_from_description('SomeString')
        expected = 2
        self.assertEqual(expected, actual)

    def test_get_merchant_id_from_description_startswith(self):
        self.db.add_merchant('TestMerchant')
        self.db.add_merchant('TestMerchant2')
        self.db.add_alias('SomeString', 'STARTSWITH', merchant='TestMerchant2')
        actual = self.db.get_merchant_id_from_description('SomeStringWords')
        expected = 2
        self.assertEqual(expected, actual)

    def tearDown(self):
        """
        Delete the temporary database
        """
        self.db.disconnect()
        os.remove(self.db.DB_DIR + '\\' + self.db.DATABASE_URI + '.db')

