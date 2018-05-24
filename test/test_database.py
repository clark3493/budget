import pathmagic  # noqa
import os
import sqlite3
from config import TestConfig
from database import Database

import unittest


class DatabaseTestCase(unittest.TestCase):
    """
    Simple functionality tests for the Database class
    """
    def setUp(self):
        """
        Setup a temporary database for testing
        """
        self.db = Database(TestConfig)

    def test_add_nonexistent_foreign_key_raises_integrity_error(self):
        cursor = self.db.get_cursor()
        cursor.execute("""CREATE TABLE table1
                          (ID INTEGER PRIMARY KEY NOT NULL,
                           Name TEXT);""")
        cursor.execute("""INSERT INTO table1(ID, Name) VALUES (NULL, 'name1')""")

        cursor.execute("""CREATE TABLE table2
                          (ID INTEGER PRIMARY KEY NOT NULL,
                          Ref INTEGER,
                          FOREIGN KEY(Ref) REFERENCES table1(ID));""")
        cmd = """INSERT INTO table2(ID, Ref) VALUES (1, 99)"""
        self.assertRaises(sqlite3.IntegrityError, cursor.execute, cmd)

    def test_connect(self):
        """
        Create a connection to a database
        """
        self.db.connect()
        self.assertIsNotNone(self.db._connection)

    def test_create_database(self):
        """
        Verify that a new database is created and saved
        """
        self.db.connect()
        self.db.disconnect()
        self.assertTrue(os.path.isfile(self.db.DB_DIR + '\\' + self.db.DATABASE_URI + '.db'))

    def test_disconnect(self):
        """
        Test successful disconnect
        """
        self.db.connect()
        self.db.disconnect()
        self.assertIsNone(self.db._connection)

    def test_get_with_where(self):
        """
        Verify that get() function works
        """
        populate_sample_database(self.db)
        val = self.db.get("title", "ALBUMS", where="artist='Andy Hunter'")
        self.assertEqual([('Glow',),('Exodus',)], val)

    def test_get_with_inner_join(self):
        populate_complex_database(self.db)
        actual = self.db.get(
            fields="stringB",
            table="tableA",
            inner_join="tableB ON tableA.ID=tableB.IDA",
            where="tableA.stringA='two'"
            )
        expected = [('3',)]
        self.assertEqual(expected, actual)
        actual2 = self.db.get(
            fields="stringB",
            table="tableA",
            inner_join="tableB ON tableA.ID=tableB.IDA",
            where="tableA.stringA='one'"
            )
        expected2 = [('1',), ('2',)]
        self.assertEqual(expected, actual)

    def test_getone(self):
        populate_sample_database(self.db)
        val = self.db.getone("title","ALBUMS", "artist='Andy Hunter'")
        self.assertEqual('Glow', val)

    def test_get_id_handles_field_without_apostrophes(self):
        populate_sample_database(self.db)
        id_num = self.db.get_id("ALBUMS", "artist", "Red")
        self.assertEqual(3, id_num)

    def test_get_id_with_supplied_integer(self):
        populate_sample_database(self.db)
        id_num = self.db.get_id("ALBUMS", None, 2)
        self.assertEqual(2, id_num)

    def test_get_id_with_supplied_nonexistent_integer(self):
        populate_sample_database(self.db)
        id_num = self.db.get_id("ALBUMS", None, 10)
        self.assertIsNone(id_num)

    def test_get_id_with_supplied_nonexistent_string(self):
        populate_sample_database(self.db)
        id_num = self.db.get_id("ALBUMS", "artist", "'NOT AN ENTRY'")
        self.assertIsNone(id_num)

    def test_get_id_with_supplied_string(self):
        populate_sample_database(self.db)
        id_num = self.db.get_id("ALBUMS", "artist", "'Red'")
        self.assertEqual(3, id_num)

    def test_get_last_entry(self):
        populate_sample_database(self.db)
        actual = self.db.get_last_entry('albums')
        expected = (5, 'The Good Life', 'Trip Lee', '4/10/2012',
                    'Reach Records', 'CD')
        self.assertEqual(expected, actual)

    def test_insert(self):
        """
        Verify that the insert function works
        """
        populate_sample_database(self.db)
        columns = ('title', 'artist', 'release_date')
        values = ('TITLE', 'ARTIST', '2018')
        self.db.insert('albums', columns, values)
        actual = self.db.get('*', 'albums', where="title='TITLE'")[0][:4]
        expected = (6, 'TITLE', 'ARTIST', '2018')
        self.assertEqual(expected, actual)

    def tearDown(self):
        """
        Delete the database
        """
        self.db.disconnect()
        os.remove(self.db.DB_DIR + '\\' + self.db.DATABASE_URI + '.db')


def populate_sample_database(db):
    cursor = db.get_cursor()

    # create a table
    cursor.execute("""CREATE TABLE albums
                      (ID integer primary key,
                       title text, artist text, release_date text,
                       publisher text, media_type text)
                   """)
    # insert some data
    cursor.execute("INSERT INTO ALBUMS VALUES "
                   "(1, 'Glow','Andy Hunter','7/24/2012',"
                   "'Xplore Records','MP3')")

    # save data to database
    db.commit()

    # insert multiple records using the more secure "?" method
    albums = [(None, 'Exodus', 'Andy Hunter', '7/9/2002',
               'Sparrow Records', 'CD'),
              (None, 'Until We Have Faces', 'Red', '2/1/2011',
               'Essential Records', 'CD'),
              (None, 'The End is Where We Begin', 'Thousand Foot Krutch',
               '4/17/2012', 'TFKmusic', 'CD'),
              (None, 'The Good Life', 'Trip Lee', '4/10/2012',
               'Reach Records', 'CD')]
    cursor.executemany("INSERT INTO albums VALUES (?,?,?,?,?,?)",
                       albums)
    db.commit()


def populate_complex_database(db):
    cursor = db.get_cursor()

    # create first table
    cursor.execute("""CREATE TABLE tableA
                      (ID integer primary key,
                       stringA text)
                   """)

    # create linked table
    cursor.execute("""CREATE TABLE tableB
                      (ID integer primary key,
                       stringB text,
                       IDA integer,
                       FOREIGN KEY (IDA) REFERENCES tableA(ID))
                       """)

    # insert some data
    adata = [(None, "one"), (None, "two"), (None, "three")]
    cursor.executemany("INSERT INTO tableA VALUES (?,?)", adata)
    bdata = [(None, "1", 1), (None, "2", 1), (None, "3", 2)]
    cursor.executemany("INSERT INTO tableB VALUES (?,?,?)", bdata)

    db.commit()