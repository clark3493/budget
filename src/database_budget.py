import sqlite3

from src.database import Database
from datetime import date,datetime

class BudgetDatabase(Database):
    def __init__(self,configuration):
        super(BudgetDatabase, self).__init__(configuration)
        
    def add_expense(self,
                    value,
                    account,
                    date=None,
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
            if max_id == None:
                id = 1
            else:
                id = max_id + 1
            
            value = round(float(value),2)
            
            cols   = "ID,Value,Account"
            vals   = (id,value,account)
            valstr = "?,?,?"
            
            # SHOULD ADD BETTER INPUT ERROR HANDLING HERE
            if date != None:
                cols   += ",Date"
                vals   += (date,)
                valstr += ",?"
                
            if category != None:
                cols   += ",Category"
                vals   += (category,)
                valstr += ",?"
                
            if subcategory != None:
                cols   += ",Subcategory"
                vals   += (subcategory,)
                valstr += ",?"
                
            if flag != None:
                cols   += ",Flag"
                vals   += (flag,)
                valstr += ",?"
                
            if payment_type != None:
                cols   += ",PaymentType"
                vals   += (payment_type,)
                valstr += ",?"
                
            if paid_to != None:
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
            
            if disconnect=='true' or disconnect==True:
                self.disconnect()
            elif disconnect=='default' and self.AUTO_DISCONNECT:
                self.disconnect()
            
        except:
            self.disconnect()
            raise