import unittest
import sys
sys.path.append('../')
from loot import Loot_bag
import sqlite3
from io import StringIO


def setUpModule():
    print('set up module')

def tearDownModule():
    print('tear down module')


class TestLootBag(unittest.TestCase):

    def create_test_conn():
        loot_db = ('/Users/nolanlittle/workspace/python/exercises/bag_o_loot/test.db')
        conn = sqlite3.connect(loot_db)
        return conn

    @classmethod
    def setUpClass(self):
        self.Loot = Loot_bag()
        self.conn = self.create_test_conn()

        tempfile = StringIO()

        for line in self.conn.iterdump():
            tempfile.write('%s\n' % line)

        tempfile.seek(0)
        with sqlite3.connect (':memory:') as conn:
            cursor = conn.cursor()
            cursor.executescript(tempfile.read())
            self.cursor = cursor
        print('Set up class')

    @classmethod
    def tearDownClass(self):
        print('Tear down class')
        self.cursor.close()
        self.conn.close()

    def test_find_child(self):
        child_name = 'Billy'
        child_id = 1
        print("WTF")
        self.assertEqual(self.Loot.find_child(child_name, self.cursor), child_id)

    def test_create_child(self):
        child_name = 'Elmo'
        response = self.Loot.create_child(child_name, self.cursor)
        print("HERE I AM", response)
        self.assertIs(type(response), int, msg=response )


