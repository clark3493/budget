import pathmagic  # noqa
import os
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

    def test_get(self):
        """
        Verify that get() function works
        """
        populate_sample_database(self.db)
        val = self.db.get("title", "ALBUMS", "artist='Andy Hunter'")
        self.assertEqual([('Glow',),('Exodus',)], val)

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

    def test_insert(self):
        """
        Verify that the insert function works
        """
        populate_sample_database(self.db)
        columns = ('title', 'artist', 'release_date')
        values = ('TITLE', 'ARTIST', '2018')
        self.db.insert('albums', columns, values)
        actual = self.db.get('*', 'albums', "title='TITLE'")[0][:4]
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
