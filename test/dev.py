import sys
sys.path.append('..')
sys.path.append(r'C:\Projects\_budget')

from config import DevelopmentConfig

from src.database_budget import BudgetDatabase
from src.table import *
from src.baseline import *

db = BudgetDatabase(DevelopmentConfig)

db.drop_tables_all()

for tbl in baseline_tables():
    db.sql_cmd(tbl.create_cmd())
    
db.show_tables(with_data=True)

#db.sql_cmd("""INSERT INTO Expense (
#                  ID,
#                  Value,
#                  Account)
#                  VALUES (
#                  4,
#                  123.45,
#                  'TheAccount');""", commit=True)
                  
                  
db.add_expense(1,"TestAccount")

db.show_tables(with_data=True)