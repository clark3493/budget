import pathmagic
from database import Database
from datetime import datetime


class BudgetDatabase(Database):
    def __init__(self, configuration):
        super(BudgetDatabase, self).__init__(configuration)

    def add_account(self,
                    name,
                    balance,
                    disconnect='default'):
        try:
            columns = ('ID', 'Name', 'Balance', 'Created')
            values = (None, name, round(float(balance), 2), datetime.now())

            self.insert('Account', columns, values)
            self.handle_connection(disconnect)

        except Exception as e:
            if self.DEBUG is True:
                self.disconnect()
                raise
            else:
                self.logger.error("Error attempting to add account {} to {}:\n{}".format(
                    name, self.DATABASE_DIR + "\\" + self.DATABASE_URI, e))

    def add_expense(self,
                    value,
                    account,
                    expense_date=None,
                    category=None,
                    subcategory=None,
                    flag=None,
                    payment_type=None,
                    paid_to=None,
                    disconnect='default'):
        
        try:
            value = round(float(value),2)
            account_id = self.get_account_id(account)
            if account_id is None:
                raise ValueError("Account '{}' could not be found in the database".format(account))
            
            columns = ('ID', 'Value', 'Account')
            values  = (None, value, account_id)
            
            # SHOULD ADD BETTER INPUT ERROR HANDLING HERE
            if expense_date is not None:
                columns += ('Date',)
                values  += (expense_date,)
                
            if category is not None:
                columns += ('Category',)
                values  += (category,)
                
            if subcategory is not None:
                columns += ('Subcategory',)
                values  += (subcategory,)
                
            if flag is not None:
                columns += ('Flag',)
                values  += (flag,)
                
            if payment_type is not None:
                columns += ('PaymentType',)
                values  += (payment_type,)
                
            if paid_to is not None:
                columns += ('PaidTo',)
                values  += (paid_to,)
            
            columns += ('Created',)
            values  += (datetime.now(),)

            self.insert('Expense', columns, values)
            self.update_account_balance(account, value, disconnect=False)
            self.handle_connection(disconnect)
            
        except Exception as e:
            if self.DEBUG is True:
                self.disconnect()
                raise
            else:
                self.logger.error("Error attempting to add {} expense to {} in {}:\n{}".format(
                    value, account, self.DATABASE_DIR + "\\" + self.DATABASE_URI, e))

    def add_expense_category(self, name, disconnect='default'):
        try:
            columns = ('ID', 'Name', 'Created')
            values = (None, name, datetime.now())

            self.insert('ExpenseCategory', columns, values)
            self.handle_connection(disconnect)

        except Exception as e:
            if self.DEBUG is True:
                self.disconnect()
                raise
            else:
                self.logger.error("Error attempting to add {} category in {}:\n{}".format(
                    name, self.DATABASE_DIR + "\\" + self.DATABASE_URI, e))

    def add_expense_recipient(self, name, disconnect='default'):
        try:
            columns = ('ID', 'Name', 'Created')
            values = (None, name, datetime.now())

            self.insert('ExpenseRecipient', columns, values)
            self.handle_connection(disconnect)

        except Exception as e:
            if self.DEBUG is True:
                self.disconnect()
                raise
            else:
                self.logger.error("Error attempting to add {} ExpenseRecipient in {}:\n{}".format(
                    name, self.DATABASE_DIR + "\\" + self.DATABASE_URI, e))

    def add_expense_recipient_alias(self,
                                    recipient,
                                    alias,
                                    alias_type='CONTAINS',
                                    disconnect='default'):
        try:
            valid_alias_types = ['CONTAINS',
                                 'ENDS WITH',
                                 'EQUALS',
                                 'STARTS WITH']
            if alias_type not in valid_alias_types:
                raise ValueError("{} is not a valid alias type".format(alias_type))

            recipient_id = self.get('ID', 'ExpenseRecipient',
                                    "Name='{}'".format(recipient))[0][0]
            if not recipient_id:
                raise ValueError("{} ExpenseRecipient could not be found".format(recipient))

            columns = ('ID', 'Recipient', 'Alias', 'AliasType', 'Created')
            values = (None, recipient_id, alias, alias_type, datetime.now())

            self.insert('ExpenseRecipientAlias', columns, values)
            self.handle_connection(disconnect)

        except Exception as e:
            if self.DEBUG is True:
                self.disconnect()
                raise
            else:
                self.logger.error("Error attempting to add {} ExpenseRecipientAlias in {}:\n{}".format(
                    alias, self.DATABASE_DIR + "\\" + self.DATABASE_URI, e))

    def add_expense_subcategory(self, name, parent_category, disconnect='default'):
        try:
            parent_id = self.get("ID","ExpenseCategory","Name='{}'".format(parent_category))

            if not parent_id:
                msg = "Error attempting to add expense sub-category.\n"
                msg += "Parent category {} could not be found".format(parent_category)
                raise ValueError(msg)

            columns = ('ID', 'Name', 'ParentCategory', 'Created')
            values = (None, name, parent_id[0][0], datetime.now())

            self.insert('ExpenseSubCategory', columns, values)
            self.handle_connection(disconnect)

        except Exception as e:
            if self.DEBUG is True:
                self.disconnect()
                raise
            else:
                self.logger.error("Error attempting to add {} category in {}:\n{}".format(
                    name, self.DATABASE_DIR + "\\" + self.DATABASE_URI, e))

    def add_payment_type(self, name, disconnect='default'):
        try:
            columns = ('ID', 'Name', 'Created')
            values = (None, name, datetime.now())

            self.insert('PaymentType', columns, values)
            self.handle_connection(disconnect)

        except Exception as e:
            if self.DEBUG is True:
                self.disconnect()
                raise
            else:
                self.logger.error("Error attempting to add {} PaymentType in {}:\n{}".format(
                    name, self.DATABASE_DIR + "\\" + self.DATABASE_URI, e))

    def get_account_id(self, account, disconnect=False):
        self.sql_cmd("SELECT ID FROM Account WHERE Name = '" + account + "'",disconnect=False)
        act_id = self._cursor.fetchone()[0]
        self.handle_connection(disconnect)

        return act_id

    def update_account_balance(self, account, delta, disconnect='default'):
        try:
            self.sql_cmd("SELECT Balance FROM Account WHERE Name = '" + account + "'",disconnect=False)
            balance = self._cursor.fetchone()[0]
            if balance is None:
                raise ValueError("Account '{}' was not found".format(account))

            balance += delta

            cmd = "UPDATE Account SET Balance = "
            cmd += str(balance)
            cmd += " WHERE Name = '"
            cmd += account + "'"

            self.sql_cmd(cmd, disconnect=False)

            self.commit()
            self.handle_connection(disconnect)

        except Exception as e:
            if self.DEBUG is True:
                self.disconnect()
                raise
            else:
                self.logger.error("Error attempting to update account {} in {}:\n{}".format(
                    account, self.DATABASE_DIR + "\\" + self.DATABASE_URI, e))
