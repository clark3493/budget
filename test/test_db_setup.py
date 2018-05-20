import pathmagic
import logging
import os
import unittest
from datetime import datetime

from baseline import baseline_tables
from config import TestConfig
from database_budget import BudgetDatabase
from parser_bofa import BofAParser


class DBSetupTestCase(unittest.TestCase):
    """
    Tests for setup of aliases, account names, reading
    in statements, etc.
    """
    def setUp(self):
        self.logger = logging.getLogger(__name__)
        self.db = BudgetDatabase(TestConfig)
        self.db.AUTO_DISCONNECT = False

    @classmethod
    def setUpClass(cls):
        super(DBSetupTestCase, cls).setUpClass()
        cls.STATEMENT_DIR = os.path.join(TestConfig.DB_DIR, 'statements', 'BofA')
        cls.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.DEBUG)
        cls.db = BudgetDatabase(TestConfig)
        cls.db.AUTO_DISCONNECT = False

        for tbl in baseline_tables():
            cls.db.sql_cmd(tbl.create_cmd())
        cls.add_simple_transactions()

    @classmethod
    def add_simple_account(cls, name=None):
        if name is None:
            name = 'SimpleAccount'
        try:
            cls.db.add_account(name,
                                0.,
                                datetime.now().date())
            cls.assertTrue(DBSetupTestCase(), True)
        except:
            cls.fail(DBSetupTestCase(), "add simple account failed")

    @classmethod
    def add_simple_transactions(cls, act_name=None):
        if act_name is None:
            act_name = 'SimpleAccount'
        cls.add_simple_account(act_name)
        for file in os.listdir(cls.STATEMENT_DIR):
            filename = os.path.join(cls.STATEMENT_DIR, file)
            bap = BofAParser(filename)
            transactions = bap.parse_statement()
            for t in transactions:
                try:
                    if not t[1].startswith('Beginning balance'):
                        columns = ('ID', 'FromAccount', 'Date', 'Description', 'Value', 'Created')
                        values = (None, 1) + t[:-1] + (datetime.now(),)
                        cls.db.insert('Transactions',
                                       columns,
                                       values)
                except:
                    cls.logger.debug("t = " + str(t))
                    cls.logger.debug("columns = " + str(columns))
                    cls.logger.debug("values = " + str(values))
                    raise

    @unittest.skip("Simple transactions added during class setup")
    def test_add_simple_transactions(self):
        try:
            self.add_simple_transactions()
            T = self.db.get('*', 'Transactions')
            self.logger.debug("# transactions = " + str(len(T)))
            self.logger.debug(str(T).replace('), (', ' \n'))
            self.assertTrue(True)
        except Exception as e:
            self.fail(e)

    def test_get_simple_transactions_info(self):
        t = self.db.get('*', 'Transactions')
        self.logger.debug("# transactions = " + str(len(t)))
        self.logger.debug(str(t).replace('), (', ' \n'))
        self.assertTrue(True)

    def tearDown(self):
        """
        Delete the database
        """
        self.db.disconnect()
        os.remove(self.db.DB_DIR + '\\' + self.db.DATABASE_URI + '.db')
