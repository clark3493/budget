import sqlite3

from src.database import Database
from datetime import date,datetime

class BudgetDatabase(Database):
    def __init__(self,configuration):
        super(BudgetDatabase, self).__init__(configuration)

    def add_account(self,
                    name,
                    balance,
                    disconnect='default'):
        try:
            # increment maximum existing ID by 1
            self.sql_cmd("SELECT MAX(ID) FROM Account", disconnect=False)
            max_id = self._cursor.fetchone()[0]
            if max_id is None:
                id = 1
            else:
                id = max_id + 1

            cols = "ID,Name,Balance,Created"
            vals = (id,name,round(float(balance),2),datetime.now())
            valstr = "?,?,?,?"

            self._cursor.execute(
                """INSERT INTO Account (%s) VALUES (%s);""" % (cols, valstr),
                vals
            )

            self.commit()

            if str(disconnect).lower() == 'true':
                self.disconnect()
            elif disconnect == 'default' and self.AUTO_DISCONNECT:
                self.disconnect()

        except Exception as e:
            if self.DEBUG is True:
                self.disconnect()
                raise
            else:
                self.logger.error("Error attempting to add account {} to {}:\n{}".format(
                    name, self.DATABASE_DIR + "\\" + self.DATABASE_URI, e))

    def add_expense_category(self, name, disconnect='default'):
        try:
            # increment maximum existing ID by 1
            self.sql_cmd("SELECT MAX(ID) FROM ExpenseCategory", disconnect=False)
            max_id = self._cursor.fetchone()[0]
            if max_id is None:
                id = 1
            else:
                id = max_id + 1

            cols = "ID,Name,Created"
            vals = (id,name,datetime.now())
            valstr = "?,?,?"

            self._cursor.execute(
                """INSERT INTO ExpenseCategory (%s) VALUES (%s);""" % (cols, valstr),
                vals
            )

            self.commit()

            if str(disconnect).lower() == 'true':
                self.disconnect()
            elif disconnect == 'default' and self.AUTO_DISCONNECT:
                self.disconnect()

        except Exception as e:
            if self.DEBUG is True:
                self.disconnect()
                raise
            else:
                self.logger.error("Error attempting to add {} category in {}:\n{}".format(
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
            # increment maximum existing ID by 1
            self.sql_cmd("SELECT MAX(ID) FROM Expense",disconnect=False)
            max_id = self._cursor.fetchone()[0]
            if max_id is None:
                id = 1
            else:
                id = max_id + 1
            
            value = round(float(value),2)
            account_id = self.get_account_id(account)
            if account_id is None:
                raise ValueError("Account '{}' could not be found in the database".format(account))
            
            cols   = "ID,Value,Account"
            vals   = (id, value, account_id)
            valstr = "?,?,?"
            
            # SHOULD ADD BETTER INPUT ERROR HANDLING HERE
            if expense_date is not None:
                cols   += ",Date"
                vals   += (expense_date,)
                valstr += ",?"
                
            if category is not None:
                cols   += ",Category"
                vals   += (category,)
                valstr += ",?"
                
            if subcategory is not None:
                cols   += ",Subcategory"
                vals   += (subcategory,)
                valstr += ",?"
                
            if flag is not None:
                cols   += ",Flag"
                vals   += (flag,)
                valstr += ",?"
                
            if payment_type is not None:
                cols   += ",PaymentType"
                vals   += (payment_type,)
                valstr += ",?"
                
            if paid_to is not None:
                cols   += ",PaidTo"
                vals   += (paid_to,)
                valstr += ",?"
            
            cols   += ",Created"
            vals   += (datetime.now(),)
            valstr += ",?"
            
            self._cursor.execute(
                """INSERT INTO Expense (%s) VALUES (%s);""" % (cols,valstr),
                vals
                )

            self.commit()

            self.update_account_balance(account, value, disconnect=False)
            
            if str(disconnect).lower() == 'true':
                self.disconnect()
            elif disconnect == 'default' and self.AUTO_DISCONNECT:
                self.disconnect()
            
        except Exception as e:
            if self.DEBUG is True:
                self.disconnect()
                raise
            else:
                self.logger.error("Error attempting to add {} expense to {} in {}:\n{}".format(
                    value, account, self.DATABASE_DIR + "\\" + self.DATABASE_URI, e))

    def add_expense_subcategory(self, name, parent_category, disconnect='default'):
        try:
            max_id = self.get("MAX(ID)", "ExpenseSubCategory")[0][0]
            if max_id is None:
                id = 1
            else:
                id = max_id + 1

            parent_id = self.get("ID","ExpenseCategory","Name='{}'".format(parent_category),
                                 disconnect=False)

            if parent_id == []:
                msg = "Error attempting to add expense sub-category.\n"
                msg += "Parent category {} could not be found".format(parent_category)
                raise ValueError(msg)

            cols = "ID,Name,ParentCategory,Created"
            vals = (id, name, parent_id[0][0], datetime.now())
            valstr = "?,?,?,?"

            self._cursor.execute(
                """INSERT INTO ExpenseSubCategory (%s) VALUES (%s);""" % (cols, valstr),
                vals
            )

            self.commit()

            if str(disconnect).lower() == 'true':
                self.disconnect()
            elif disconnect == 'default' and self.AUTO_DISCONNECT:
                self.disconnect()

        except Exception as e:
            if self.DEBUG is True:
                self.disconnect()
                raise
            else:
                self.logger.error("Error attempting to add {} category in {}:\n{}".format(
                    name, self.DATABASE_DIR + "\\" + self.DATABASE_URI, e))

    def get_account_id(self, account,disconnect=False):
        self.sql_cmd("SELECT ID FROM Account WHERE Name = '" + account + "'",disconnect=False)
        id = self._cursor.fetchone()[0]

        if str(disconnect).lower() == 'true':
            self.disconnect()
        elif disconnect == 'default' and self.AUTO_DISCONNECT:
            self.disconnect()

        return id

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

            if str(disconnect).lower() == 'true':
                self.disconnect()
            elif disconnect == 'default' and self.AUTO_DISCONNECT:
                self.disconnect()

        except Exception as e:
            if self.DEBUG is True:
                self.disconnect()
                raise
            else:
                self.logger.error("Error attempting to update account {} in {}:\n{}".format(
                    account, self.DATABASE_DIR + "\\" + self.DATABASE_URI, e))