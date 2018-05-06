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
                      (title text, artist text, release_date text,
                       publisher text, media_type text
                   """)
    # insert some data
    cursor.execute("INSERT INTO ALBUMS VALUES "
                   "('Glow','Andy Hunter','7/24/2012',"
                   "'Xplore Records','MP3')")

    # save data to database
    db.commit()

    # insert multiple records using the more secure "?" method
    albums = [('Exodus', 'Andy Hunter', '7/9/2002',
               'Sparrow Records', 'CD'),
              ('Until We Have Faces', 'Red', '2/1/2011',
               'Essential Records', 'CD'),
              ('The End is Where We Begin', 'Thousand Foot Krutch',
               '4/17/2012', 'TFKmusic', 'CD'),
              ('The Good Life', 'Trip Lee', '4/10/2012',
               'Reach Records', 'CD')]
    cursor.executemany("INSERT INTO albums VALUES (?,?,?,?,?)",
                       albums)
    db.commit()
