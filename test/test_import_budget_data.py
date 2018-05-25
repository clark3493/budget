import pathmagic
import logging
import os
import unittest

from baseline import baseline_tables
from config import TestConfig
from database_budget import BudgetDatabase
from data.import_budget_data import ImportBudgetData


class ImportBudgetDataTestCase(unittest.TestCase):

    def setUp(self):
        database = BudgetDatabase(TestConfig)
        self.imp = ImportBudgetData(database)
        self.imp.db.AUTO_DISCONNECT = False
        self.logger = logging.getLogger(__name__)
        for tbl in baseline_tables():
            self.imp.db.sql_cmd(tbl.create_cmd())

    def test_import_alias_from_file(self):
        file = os.path.join(pathmagic.cfg_dir, 'data', 'alias.csv')
        self.imp.import_alias_from_file(file,
                                        add_categories=True,
                                        add_merchants=True)
        self.assertEqual(1,1)

    def tearDown(self):
        self.imp.db.disconnect()
        os.remove(self.imp.db.DB_DIR + '\\' + self.imp.db.DATABASE_URI + '.db')


if __name__ == '__main__':
    unittest.main()