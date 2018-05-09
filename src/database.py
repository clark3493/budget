import logging
import sqlite3

from config import Config


class Database(Config):

    def __init__(self, configuration):
        if configuration.DATABASE_URI is None:
            raise ValueError("The input configuration is not defined")
        
        # attributes inherited from the input configuration
        self.DATABASE_URI = configuration.DATABASE_URI
        self.DEBUG   = configuration.DEBUG
        self.PROTECT = configuration.PROTECT
        self.TEST    = configuration.TEST
        
        # database attributes
        self.AUTO_DISCONNECT = True
        self._tables = self.get_tables()
        
        # database connections
        self._connection = None
        self._cursor = None

        # logging settings
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=configuration.LOGLEVEL)

    def commit(self):
        """
        Commits (save) changes to the database that have occurred since connecting
        or since last commit
        """
        try:
            self._connection.commit()
        except Exception as e:
            if self._connection is None:
                self.logger.warning("Attempted to commit, but did not have a database connection")
            else:
                if self.DEBUG is True:
                    self.disconnect()
                    raise
                else:
                    self.logger.error("Failed to commit to database:\n".format(e))

    def connect(self):
        """
        Connects to the database defined by the configuration DB_DIR and DATABASE_URI
        """
        self._connection = sqlite3.connect(self.DB_DIR + "\\" + self.DATABASE_URI + ".db")
        
    def disconnect(self):
        """
        Disconnects from the database if there is an active connection
        """
        if self._cursor is not None:
            self._cursor.close()
            self._cursor = None
        
        if self._connection is None:
            self.logger.debug("Attempted to disconnect but no active connection was found")
        else:
            self._connection.close()
            self._connection = None
            
    def drop_table(self, name, if_exists=True, override=False):
        """
        Deletes a table from the database as defined by the configuration.

        @param name: the name of the table to be dropped
        @type name: string
        @param if_exists: flag indicating whether to include IF_EXISTS in the
                          SQL command
        @type if_exists: boolean
        @param override: flag to override the configuration protection if the
                         configuration requests user confirmation before deleting
                         data
        @type override: boolean
        """
        if self.PROTECT and not override:
            msg  = "Deleting a table cannot be undone.\n"
            msg += "Are you sure you want to delete table '{}' from database\n"
            msg += "    " + self.DATABASE_DIR + "\\" + self.DATABASE_URI + ".db?\nY/N:  "
            go = input(msg.format(name))
            
            if go[0].lower() != "y":
                self.logger.info("User cancelled table drop for table '{}' in {}".format(
                        name, self.DATABASE_DIR + "\\" + self.DATABASE_URI))
                return
        
        cmd = "DROP TABLE "
        if if_exists:
            cmd += "IF EXISTS "
        cmd += name + ";"
        
        try:
            self.sql_cmd(cmd)
        except Exception as e:
            if self.DEBUG is True:
                self.disconnect()
                raise
            else:
                self.logger.error("Error attempting to delete table {} from {}:\n{}".format(
                    name,self.DATABASE_DIR + "\\" + self.DATABASE_URI,e))
            
        if self.AUTO_DISCONNECT:
            self.disconnect()
            
    def drop_tables_all(self):
        """
        Deletes all tables from the database. Cannot be undone
        """
        if self.PROTECT:    
            msg = "Deleting a table cannot be undone.\n"
            msg += "Are you sure you want to delete table ALL TABLES from database\n"
            msg += "    " + self.DATABASE_DIR + "\\" + self.DATABASE_URI + ".db?\nY/N:  "
            go = input(msg)
            
            if go[0].lower() != "y":
                self.logger.info("User cancelled table drop for all tables in {}".format(
                    self.DATABASE_DIR + "\\" + self.DATABASE_URI))
                return
        
        cursor = self.get_cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        for tbl in tables:
            cursor.execute("DROP TABLE " + tbl[0])
            
        if self.AUTO_DISCONNECT:
            self.disconnect()

    def get(self, fields, table, where=None, disconnect='default'):
        cmd = "SELECT " + fields + " FROM " + table
        if where is not None:
            cmd += " WHERE " + where
        self.sql_cmd(cmd, disconnect=False)
        val = self._cursor.fetchall()
        self.handle_connection(disconnect)

        return val

    def getone(self, fields, table, where=None, disconnect='default'):
        val = self.get(fields, table, where=where, disconnect=disconnect)
        if val:
            return val[0][0]
        else:
            return None

    def get_connection(self):
        """
        Returns an sqlite3 connection object for the database defined by the
        configuration
        
        @return: database connection
        @rtype: connection
        """
        if self._connection is None:
            self.connect()
        
        return self._connection
        
    def get_cursor(self):
        """
        Returns a cursor object for the current connection. Build a connection
        if there is none.
        
        @return: cursor to database connection
        @rtype: cursor
        """
        if self._cursor is None:
            connection = self.get_connection()
            self._cursor = connection.cursor()
            
        return self._cursor

    def get_id(self, table, field, value):
        """
        Returns the first ID for the given value of the given field in
        the indicated table, if it exists.
        If the given value is an integer, the function
        simply checks if the ID exists and returns it.
        Returns None if the corresponding entry cannot be found

        :param table: the name of the table to search
        :type table: string
        :param field: Name of the field to search if value is a string
        :type field: string
        :param value: the value in the field to search or an id number
        :type value: string or integer
        :return: ID number
        :rtype: int
        """
        if type(value) is int:
            val = self.getone('ID', table, 'ID={}'.format(value))
        else:
            strvalue = self.string_string(value)
            val = self.getone('ID', table, '{}={}'.format(field, strvalue))

        return val

    def get_tables(self):
        # PLACEHOLDER
        return None

    def handle_connection(self, disconnect):
        """
        Determines if the database connection should be closed
        based on the input parameter 'disconnect'
        True or False provide a specific instructions
        'default' disconnects if AUTO_DISCONNECT is True

        @param disconnect: disconnection flag
        @type disconnect: boolean or string
        """
        if str(disconnect).lower() == 'true':
            self.disconnect()
        elif disconnect == 'default' and self.AUTO_DISCONNECT:
            self.disconnect()

    def insert(self, table, cols, vals):
        """
        Creates a line item within the indicated table with the
        given values for the corresponding indicated columns

        @param table: table name
        @type table: string
        @param cols: column names
        @type cols: tuple(string)
        @param vals: data values
        @type vals: tuple(various)
        """
        try:
            valstr = "?," * len(cols)
            valstr = valstr[:-1]
            cursor = self.get_cursor()
            cmd = "INSERT INTO {} {} VALUES ({})".format(
                table, cols, valstr)
            cursor.execute(cmd, vals)
            self.commit()
        except sqlite3.OperationalError:
            self.disconnect()
            self.logger.error("Command='{}'\nValues={}".format(cmd, vals))
            raise
        except Exception:
            self.disconnect()
            raise

    def show_tables(self, with_data=False):
        """
        Prints the name of all tables in the database, along with other
        optional parameters
        
        @param with_data: flag to print the data for each table
        @type with_data: boolean
        """
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
        """
        Executes a general SQL command in the database
        
        @param command: the SQL command
        @type command:  string
        @param commit:  flag to commit changes before returning/disconnecting
        @type commit:   boolean
        @param disconnect:      flag to override the database AUTO_DISCONNECT setting
        @options disconnect:    'default','true','false'
        @type disconnect:       string
        """
        try:
            self._cursor = self.get_cursor()
            self._cursor.execute(command)
            
            if commit:
                self.commit()
                
        except Exception:
            if self.DEBUG is True:
                self.disconnect()
                self.logger.error(" Error during SQL command:\n{}".format(command))
                raise
            else:
                self.logger.error(" Error during SQL command:\n{}".format(command))
            
        if disconnect == 'true' or disconnect is True:
            self.disconnect()
        elif disconnect == 'default' and self.AUTO_DISCONNECT:
            self.disconnect()

    @staticmethod
    def string_string(string):
        """
        Appends apostrophes to the beginning and end of the given
        string if they do not already exists

        :param string: the string to be modified
        :type string: str
        :return: the modified string
        :rtype: str
        """
        if string[0] != "'":
            string = "'" + string
        if string[-1] != "'":
            string = string + "'"
        return string
