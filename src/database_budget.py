import pathmagic
from database import Database
from datetime import datetime


class BudgetDatabase(Database):
    def __init__(self, configuration):
        super(BudgetDatabase, self).__init__(configuration)

    def add_account(self,
                    name,
                    account_type,
                    start_balance,
                    disconnect='default'):
        try:
            columns = ('ID', 'Name', 'Type', 'StartBalance', 'Created')
            values = (None, name, account_type, round(float(start_balance), 2), datetime.now())

            self.insert('Account', columns, values)
            self.handle_connection(disconnect)

        except Exception as e:
            if self.DEBUG is True:
                self.disconnect()
                raise
            else:
                self.logger.error("Error attempting to add account {} to {}:\n{}".format(
                    name, self.DATABASE_DIR + "\\" + self.DATABASE_URI, e))

    def add_account_attribute(self,
                              account,
                              attribute,
                              disconnect='default'):
        try:
            account_id = self.get_id('Account', 'Name', account)
            if account_id is None:
                raise ValueError("Could not find account '{}' in database".format(account))

            attribute_id = self.get_id('Attribute', 'Name', attribute)
            if attribute_id is None:
                raise ValueError("Could not find attribute '{}' in database".format(attribute))

            columns = ('AccountID', 'AttributeID')
            values  = (account_id, attribute_id)

            self.insert('AccountAttribute', columns, values)
            self.handle_connection(disconnect)

        except Exception as e:
            if self.DEBUG is True:
                self.disconnect()
                raise
            else:
                self.logger.error("Error attempting to link attribute '{}' to account '{}' in {}:\n{}".format(
                    account, attribute, self.DATABASE_DIR + "\\" + self.DATABASE_URI, e))

    def add_alias(self,
                  account,
                  string,
                  alias_type,
                  disconnect='default'):
        try:
            account_id = self.get_id('Account', 'Name', account)
            if account_id is None:
                raise ValueError("Could not find account '{}' in database".format(account))

            columns = ('ID', 'Account', 'String', 'Type', 'Created')
            values  = (None, account_id, string, alias_type, datetime.now())

            self.insert('Alias', columns, values)
            self.handle_connection(disconnect)

        except Exception as e:
            if self.DEBUG is True:
                self.disconnect()
                raise
            else:
                self.logger.error("Error attempting to add alias '{}' for '{}' in {}:\n{}".format(
                    string, account, self.DATABASE_DIR + "\\" + self.DATABASE_URI, e))

    def add_attribute(self,
                      attribute_name,
                      disconnect='default'):
        try:
            columns = ('ID', 'Name', 'Created')
            values  = (None, attribute_name, datetime.now())

            self.insert('Attribute', columns, values)
            self.handle_connection(disconnect)

        except Exception as e:
            if self.DEBUG is True:
                self.disconnect()
                raise
            else:
                self.logger.error("Error attempting to add attribute {} to {}:\n{}".format(
                    attribute_name, self.DATABASE_DIR + "\\" + self.DATABASE_URI, e))

    def add_category(self, name, disconnect='default'):
        try:
            columns = ('ID', 'Name', 'Created')
            values= (None, name, datetime.now())

            self.insert('Category', columns, values)
            self.handle_connection(disconnect)

        except Exception as e:
            if self.DEBUG is True:
                self.disconnect()
                raise
            else:
                self.logger.error("Error attempting to add {} IncomeCategory in {}:\n{}".format(
                    name, self.DATABASE_DIR + "\\" + self.DATABASE_URI, e))

    def add_expense(self,
                    value,
                    account,
                    paid_to=None,
                    expense_date=None,
                    description=None,
                    category=None,
                    subcategory=None,
                    payment_type=None,
                    disconnect='default'):
        
        try:
            self.add_transaction(value,
                                 from_account=account,
                                 to_account=paid_to,
                                 transaction_type='Expense',
                                 transaction_date=expense_date,
                                 description=description,
                                 category=category,
                                 subcategory=subcategory,
                                 payment_type=payment_type,
                                 disconnect=disconnect)
            
        except Exception as e:
            if self.DEBUG is True:
                self.disconnect()
                raise
            else:
                self.logger.error("Error attempting to add {} expense to {} in {}:\n{}".format(
                    value, account, self.DATABASE_DIR + "\\" + self.DATABASE_URI, e))

    def add_income(self,
                   value,
                   account,
                   source=None,
                   income_date=None,
                   description=None,
                   category=None,
                   subcategory=None,
                   payment_type=None,
                   disconnect='default'):
        try:
            self.add_transaction(value,
                                 from_account=source,
                                 to_account=account,
                                 transaction_type='Income',
                                 transaction_date=income_date,
                                 description=description,
                                 category=category,
                                 subcategory=subcategory,
                                 payment_type=payment_type,
                                 disconnect=disconnect)

        except Exception as e:
            if self.DEBUG is True:
                self.disconnect()
                raise
            else:
                self.logger.error("Error attempting to add {} income to {} in {}:\n{}".format(
                    value, account, self.DATABASE_DIR + "\\" + self.DATABASE_URI, e))

    def add_subcategory(self,
                        name,
                        parent_category,
                        disconnect='default'):
        try:
            parent_id = self.get_id('Category',
                                    'Name',
                                    parent_category)
            if not parent_id:
                msg = "Error attempting to add income sub-category.\n"
                msg += "Parent category {} could not be found".format(parent_category)
                raise ValueError(msg)

            columns = ('ID', 'Name', 'Parent', 'Created')
            values = (None, name, parent_id, datetime.now())

            self.insert('SubCategory', columns, values)
            self.handle_connection(disconnect)

        except Exception as e:
            if self.DEBUG is True:
                self.disconnect()
                raise
            else:
                self.logger.error("Error attempting to add {} subcategory in {}:\n{}".format(
                    name, self.DATABASE_DIR + "\\" + self.DATABASE_URI, e))

    def add_transaction(self,
                        value,
                        from_account=None,
                        to_account=None,
                        transaction_type=None,
                        transaction_date=None,
                        description=None,
                        category=None,
                        subcategory=None,
                        payment_type=None,
                        disconnect='default'):
        try:
            value = round(float(value), 2)

            columns = ('ID', 'Value')
            values  = (None, value)

            # SHOULD ADD BETTER INPUT ERROR HANDLING HERE
            if from_account is not None:
                from_account_id = self.get_account_id(from_account)
                if from_account_id is None:
                    raise ValueError("Account '{}' could not be found in the database".format(from_account))
                else:
                    columns += ('FromAccount',)
                    values  += (from_account_id,)

            if to_account is not None:
                to_account_id = self.get_account_id(to_account)
                if to_account_id is None:
                    raise ValueError("Account '{}' could not be found in the database".format(to_account))
                else:
                    columns += ('ToAccount',)
                    values  += (to_account_id,)

            if transaction_type is not None:
                columns += ('TransactionType',)
                values  += (transaction_type,)

            if transaction_date is not None:
                columns += ('Date',)
                values  += (transaction_date,)

            if description is not None:
                columns += ('Description',)
                values  += (description,)

            if category is not None:
                columns += ('Category',)
                values  += (category,)

            if subcategory is not None:
                columns += ('SubCategory',)
                values  += (subcategory,)

            if payment_type is not None:
                columns += ('PaymentType',)
                values  += (payment_type,)

            columns += ('Created',)
            values  += (datetime.now(),)

            self.insert('Transactions', columns, values)
            #self.update_account_balance(value, from_account, to_account)
            self.handle_connection(disconnect)

        except Exception as e:
            if self.DEBUG is True:
                self.disconnect()
                raise
            else:
                self.logger.error("Error attempting to add {} transaction in {}:\n{}".format(
                    value, self.DATABASE_DIR + "\\" + self.DATABASE_URI, e))

    def add_transaction_category(self,
                                 transaction_id,
                                 category,
                                 disconnect='default'):
        try:
            category_id = self.get_id('Category', 'Name', category)
            if category_id is None:
                raise ValueError("Could not find attribute '{}' in database".format(category))

            columns = ('TransactionID', 'CategoryID')
            values  = (transaction_id, category_id)

            self.insert('TransactionCategory', columns, values)
            self.handle_connection(disconnect)

        except Exception as e:
            if self.DEBUG is True:
                self.disconnect()
                raise
            else:
                self.logger.error("Error attempting to link category '{}' to transaction '{}' in {}:\n{}".format(
                    category, transaction_id, self.DATABASE_DIR + "\\" + self.DATABASE_URI, e))

    def add_transaction_subcategory(self,
                                    transaction_id,
                                    subcategory,
                                    disconnect='default'):
        try:
            subcategory_id = self.get_id('SubCategory', 'Name', subcategory)
            if subcategory_id is None:
                raise ValueError("Could not find attribute '{}' in database".format(subcategory))

            columns = ('TransactionID', 'SubCategoryID')
            values  = (transaction_id, subcategory_id)

            self.insert('TransactionSubCategory', columns, values)
            self.handle_connection(disconnect)

        except Exception as e:
            if self.DEBUG is True:
                self.disconnect()
                raise
            else:
                self.logger.error("Error attempting to link subcategory '{}' to transaction '{}' in {}:\n{}".format(
                    subcategory, transaction_id, self.DATABASE_DIR + "\\" + self.DATABASE_URI, e))

    def get_account_id(self, account, disconnect=False):
        act_id = self.get_id('Account', 'Name', account)
        self.handle_connection(disconnect)

        return act_id


