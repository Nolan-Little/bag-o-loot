import unittest
import sys
sys.path.append('../')
from main_test import Loot_bag
import sqlite3


def setUpModule():
    print('set up module')

def tearDownModule():
    print('tear down module')


class TestLootBag(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.Loot = Loot_bag()
        print('Set up class')

    @classmethod
    def tearDownClass(self):
        print('Tear down class')

    def test_find_child(self):
        child_name = 'Billy'
        child_id = 1
        self.assertEqual(self.Loot.find_child(child_name), child_id)

    def test_create_child(self):
        child_name = 'Elmo'
        response = self.Loot.create_child(child_name)
        print("HERE I AM", response)
        self.assertIs(type(response), int, msg=response )


