import pathmagic
import logging

from database_budget import BudgetDatabase


class ImportBudgetData(object):

    def __init__(self, database):
        """
        :param database: database to import data into
        :type database: BudgetDatabase
        """
        self.db = database
        self.db.AUTO_DISCONNECT = False
        self.logger = logging.getLogger(__name__)

    def add_nested_categories(self, categories, parent=None):
        if not categories:
            return
        if len(categories) == 1:
            self.db.add_category(categories[0], parent=parent, disconnect=False)
        else:
            self.db.add_category(categories[0], parent=parent, disconnect=False)
            self.add_nested_categories(categories[1:], parent=categories[0])

    @staticmethod
    def db_str(string):
        if type(string) is list:
            string = [s.replace("'", "") for s in string]
        else:
            string = string.replace("'", "")
        return string

    def import_alias_from_file(self, infile,
                               add_categories=False,
                               add_merchants=False):
        with open(infile) as f:
            lines = f.readlines()

        for n, line in enumerate(lines):
            (merchant, category, parent, alias_type, string) = \
                self.parse_alias_entry(line, n, infile)

            if add_categories:
                for i, cat in enumerate(category):
                    c = self.db.get('*', 'Category', where='Name LIKE "{}"'.format(cat))
                    if not c:
                        try:
                            self.add_nested_categories(self.db_str(category[i:]))
                        except Exception:
                            self.logger.error((n+1, merchant, category, parent))
                            raise

            if add_merchants:
                m = self.db.get('*', 'Merchant', where='Name LIKE "{}"'.format(merchant))
                if not m:
                    self.db.add_merchant(self.db_str(merchant), disconnect=False)

            self.db.add_alias(self.db_str(string),
                              alias_type,
                              category=self.db_str(category[-1]),
                              merchant=self.db_str(merchant),
                              disconnect=False)

    @staticmethod
    def parse_alias_entry(line, n, infile):
        merchant = None
        category = None
        parent = None
        alias_type = None
        string = None

        entries = [l.strip() for l in line.split(',')]

        hasmerchant = [i for i, x in enumerate(entries) if x.upper() == 'MERCHANT']
        hascategory = [i for i, x in enumerate(entries) if x.upper() == 'CATEGORY']
        hasparent = [i for i, x in enumerate(entries) if x.upper() == 'PARENT']
        hascontains = [i for i, x in enumerate(entries) if x.upper() == 'CONTAINS']
        hasendswith = [i for i, x in enumerate(entries) if x.upper() == 'ENDSWITH']
        hasequals = [i for i, x in enumerate(entries) if x.upper() == 'EQUALS']
        hasstartswith = [i for i, x in enumerate(entries) if x.upper() == 'STARTSWITH']

        if not hasmerchant and not hascategory:
            msg = 'Error in line number {} of file {}\n'.format(n, infile)
            msg += 'Must have either a category or merchant entry\n'
            raise ValueError(msg)

        if hasmerchant:
            merchant = entries[hasmerchant[0] + 1]
        if hascategory:
            category = entries[hascategory[0] + 1].split('.')
        if hasparent:
            parent = entries[hasparent[0] + 1]
        if len(hascontains) + len(hasendswith) + \
                len(hasequals) + len(hasstartswith) == 0:
            msg = 'Error in line number {} of file {}\n'.format(n+1, infile)
            msg += str(entries)
            msg += 'Must input alias type.'
            raise ValueError(msg)
        if len(hascontains) + len(hasendswith) + \
                len(hasequals) + len(hasstartswith) > 1:
            msg = 'Error in line number {} of file {}\n'.format(n, infile)
            msg += 'Cannot define more than one alias type.'
            raise ValueError(msg)
        if hascontains:
            alias_type = 'CONTAINS'
            string = entries[hascontains[0] + 1]
        if hasendswith:
            alias_type = 'ENDSWITH'
            string = entries[hasendswith[0] + 1]
        if hasequals:
            alias_type = 'EQUALS'
            string = entries[hasequals[0] + 1]
        if hasstartswith:
            alias_type = 'STARTSWITH'
            string = entries[hasstartswith[0] + 1]

        return (merchant, category, parent, alias_type, string)
