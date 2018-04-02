import sys
sys.path.append('..')
sys.path.append(r'C:\Projects\_budget')

from config import DevelopmentConfig

from src.database import Database
from src.table import *
from src.baseline import *

db = Database(DevelopmentConfig)

db.drop_tables_all()

for tbl in baseline_tables():
    db.sql_cmd(tbl.create_cmd())
    
db.show_tables(with_data=True)