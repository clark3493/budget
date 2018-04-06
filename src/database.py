import sys
#sys.path.append(r"C:\Projects\_budget")

import sqlite3
from warnings import warn
from datetime import date,datetime

from config import Config

class Database(Config):
    def __init__(self, configuration):
        if configuration.DATABASE_URI == None:
            raise ValueError("The input configuration is not defined")
        
        # attributes inherited from the input configuration
        self.DATABASE_URI = configuration.DATABASE_URI
        self.DEBUG   = configuration.DEBUG
        self.PROTECT = configuration.PROTECT
        self.TEST    = configuration.TEST
        
        # database attributes
        self.AUTO_DISCONNECT = True
        self.tables = self.get_tables()
        
        # database connections
        self._connection = None
        self._cursor = None
        
    def commit(self):
        try:
            self._connection.commit()
        except:
            if self._connection == None:
                # ADD DB DEPENDENT ERROR REPORTING HERE
                pass
            else:
                self.disconnect()
                raise
    
    
    def connect(self):
        self._connection = sqlite3.connect(self.DB_DIR + "\\" + self.DATABASE_URI + ".db")
        
    def disconnect(self):
        if self._cursor != None:
            self._cursor.close()
            self._cursor = None
        
        if self._connection == None:
            warn("No need to disconnect, no connection has been established.")
        else:
            self._connection.close()
            self._connection = None
            
    def drop_table(self,name,if_exists=True,override=False):
        
        if self.PROTECT:
            msg  = "Deleting a table cannot be undone.\n"
            msg += "Are you sure you want to delete table '{}' from database\n"
            msg += "    " + self.DATABASE_DIR + "\\" + self.DATABASE_URI + ".db?\nY/N:  "
            go = raw_input(msg)
            
            if go[0].lower() != "y":
                # ADD MESSAGE OUTPUT DEPENDING ON CONFIG KEY FOR ECHOES
                return
        
        cmd  = "DROP TABLE "
        if if_exists:
            cmd += "IF EXISTS "
        cmd += name + ";"
        
        try:
            self.sql_cmd(cmd)
        except:
            self.disconnect()
            raise
            
        if AUTO_DISONNECT:
            self.disconnect()
            
    def drop_tables_all(self):
    
        if self.PROTECT:    
            msg  = "Deleting a table cannot be undone.\n"
            msg += "Are you sure you want to delete table ALL TABLES from database\n"
            msg += "    " + self.DATABASE_DIR + "\\" + self.DATABASE_URI + ".db?\nY/N:  "
            go = raw_input(msg)
            
            if go[0].lower() != "y":
                # ADD MESSAGE OUTPUT DEPENDING ON CONFIG KEY FOR ECHOES
                return
        
        cursor = self.get_cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        for tbl in tables:
            cursor.execute("DROP TABLE " + tbl[0])
            
        if self.AUTO_DISCONNECT:
            self.disconnect()
            
    def get_connection(self):
        if self._connection == None:
            self.connect()
        
        return self._connection
        
    def get_cursor(self):
        if self._cursor == None:
            connection = self.get_connection()
            self._cursor = connection.cursor()
            
        return self._cursor
    
    def get_tables(self):
        # PLACEHOLDER
        return None
    
    def show_tables(self,with_data=False):
        try:
            cursor = self.get_cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            for tbl in tables:
                print(tbl[0])
                if with_data:
                    cursor.execute("SELECT * FROM " + tbl[0] + ";")
                    rows = cursor.fetchall()
                    for row in rows:
                        print("    " + str(row))
            
            print("")
            
        except KeyboardInterrupt:
            self.disconnect()
            print("\n\nClean exit by user")
        except Exception:
            self.disconnect()
            raise
        
        if self.AUTO_DISCONNECT:
            self.disconnect()
            
    def sql_cmd(self, command, commit=False,disconnect='default'):
        try:
            self._cursor = self.get_cursor()
            self._cursor.execute(command)
            
            if commit:
                self.commit()
                
        except:
            print(command)
            self.disconnect()
            raise
            
        if disconnect=='true' or disconnect==True:
            self.disconnect()
        elif disconnect=='default' and self.AUTO_DISCONNECT:
            self.disconnect()