import pathmagic
import logging
from datetime import datetime

from database import Database
from string_filter import StringFilter as Filt


class BudgetDatabase(Database):
    def __init__(self, configuration):
        super(BudgetDatabase, self).__init__(configuration)
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=configuration.LOGLEVEL)

    def add_account(self,
                    name,
                    start_balance,
                    start_date,
                    disconnect='default'):
        try:
            columns = ('ID', 'Name',
                       'StartBalance', 'StartDate', 'Created')
            values = (None, name,
                      round(float(start_balance), 2),
                      start_date,
                      datetime.now())

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
                  string,
                  alias_type,
                  category=None,
                  merchant=None,
                  disconnect='default'):
        # TODO: add ability to set transaction value limits for application of alias
        #       ex: expenses < $15 at gas stations are for food/tobacco
        try:
            columns = ('ID', 'String', 'Type')
            values  = (None, string, alias_type)

            if category is not None:
                category_id = self.get_id('Category', 'Name', category)
                if category_id is None:
                    raise ValueError("Could not find category '{}' in database".format(category))

                columns += ('CategoryID',)
                values  += (category_id,)

            if merchant is not None:
                merchant_id = self.get_id('Merchant', 'Name', merchant)
                if merchant_id is None:
                    raise ValueError("Could not find merchant '{}' in database".format(merchant))

                columns += ('MerchantID',)
                values  += (merchant_id,)

            columns += ('Created',)
            values  += (datetime.now(),)

            self.insert('Alias', columns, values)
            self.handle_connection(disconnect)

        except Exception as e:
            if self.DEBUG is True:
                self.disconnect()
                raise
            else:
                self.logger.error("Error attempting to add alias {} '{}' in {}:\n{}".format(
                    alias_type, string, self.DATABASE_DIR + "\\" + self.DATABASE_URI, e))

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

    def add_category(self,
                     name,
                     parent=None,
                     disconnect='default'):
        try:
            columns = ('ID', 'Name')
            values= (None, name)

            if parent is not None:
                parent_id = self.get_id('Category', 'Name', parent)
                if parent_id is None:
                    raise ValueError("Could not find category '{}' in database".format(parent))

                columns += ('ParentID',)
                values  += (parent_id,)

            columns += ('Created',)
            values  += (datetime.now(),)

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
                    payment_type=None,
                    disconnect='default'):
        
        try:
            self.add_transaction(value,
                                 from_account=account,
                                 to_account=paid_to,
                                 transaction_type='Expense',
                                 transaction_date=expense_date,
                                 description=description,
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
                   payment_type=None,
                   disconnect='default'):
        try:
            self.add_transaction(value,
                                 from_account=source,
                                 to_account=account,
                                 transaction_type='Income',
                                 transaction_date=income_date,
                                 description=description,
                                 payment_type=payment_type,
                                 disconnect=disconnect)

        except Exception as e:
            if self.DEBUG is True:
                self.disconnect()
                raise
            else:
                self.logger.error("Error attempting to add {} income to {} in {}:\n{}".format(
                    value, account, self.DATABASE_DIR + "\\" + self.DATABASE_URI, e))

    def add_merchant(self, name, disconnect='default'):
        try:
            columns = ('ID', 'Name', 'Created')
            values  = (None, name, datetime.now())

            self.insert('Merchant', columns, values)
            self.handle_connection(disconnect)

        except Exception as e:
            if self.DEBUG is True:
                self.disconnect()
                raise
            else:
                self.logger.error("Error attempting to add {} merchant in {}:\n{}".format(
                    name, self.DATABASE_DIR + "\\" + self.DATABASE_URI, e))

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

            columns = ('ID', 'Name', 'ParentID', 'Created')
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
                    columns += ('FromAccountID',)
                    values  += (from_account_id,)

            if to_account is not None:
                to_account_id = self.get_account_id(to_account)
                if to_account_id is None:
                    raise ValueError("Account '{}' could not be found in the database".format(to_account))
                else:
                    columns += ('ToAccountID',)
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

            if payment_type is not None:
                columns += ('PaymentType',)
                values  += (payment_type,)

            columns += ('Created',)
            values  += (datetime.now(),)

            self.insert('Transactions', columns, values)
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
                    subcategory, transaction_id, self.DB_DIR + "\\" + self.DATABASE_URI, e))

    @staticmethod
    def alias_where_filter(string):
        msg  = "(Alias.Type='CONTAINS' AND '{}' LIKE '%' || Alias.String || '%')"
        msg += " OR (Alias.Type='STARTSWITH' AND '{}' LIKE Alias.String || '%')"
        msg += " OR (Alias.Type='ENDSWITH' AND '{}' LIKE '%' || Alias.String)"
        msg += " OR (Alias.Type='EQUALS' AND '{}' LIKE Alias.String)"
        return msg.format(string, string, string, string)

    def get_account_id(self, account, disconnect=False):
        act_id = self.get_id('Account', 'Name', account)
        self.handle_connection(disconnect)

        return act_id

    def get_category_id_from_description(self,
                                         description,
                                         disconnect=False):
        try:
            id_ = self.get(fields='Category.ID',
                           table='Category',
                           inner_join='Alias ON Alias.CategoryID=Category.ID',
                           where=self.alias_where_filter(description)
                           )
            if not id_:
                self.logger.info("No matching alias found for description '{}'".format(description))
                ret = None
            elif len(id_) > 1:
                msg = "\nMore than 1 matching alias was found for description:\n"
                msg += "'{}'\n"
                msg += "Only the first category ID was returned."
                self.logger.warning(msg.format(description))
                ret = id_[0][0]
            else:
                ret = id_[0][0]

            self.handle_connection(disconnect)
            return ret

        except Exception as e:
            if self.DEBUG is True:
                self.disconnect()
                raise
            else:
                self.logger.error("Error attempting to get category ID for description '{}' in database '{}:\n{}'".format(
                    description, self.DB_DIR + '\\' + self.DATABASE_URI, e))

    def get_merchant_id_from_description(self,
                                         description,
                                         disconnect=False):
        try:
            id_ = self.get(fields='Merchant.ID',
                           table='Merchant',
                           inner_join='Alias ON Alias.MerchantID=Merchant.ID',
                           where=self.alias_where_filter(description)
                           )
            if not id_:
                self.logger.info("No matching alias found for description '{}'".format(description))
                ret = None
            elif len(id_) > 1:
                msg = "\nMore than 1 matching alias was found for description:\n"
                msg += "'{}'\n"
                msg += "Only the first merchant ID was returned."
                self.logger.warning(msg.format(description))
                ret = id_[0][0]
            else:
                ret = id_[0][0]

            self.handle_connection(disconnect)
            return ret

        except Exception as e:
            if self.DEBUG is True:
                self.disconnect()
                raise
            else:
                self.logger.error("Error attempting to get merchant ID for description '{}' in database '{}:\n{}'".format(
                    description, self.DB_DIR + '\\' + self.DATABASE_URI, e))





