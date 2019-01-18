import sqlite3
import sys

# sys.argv is a list of the passed in args from the command line

loot_db = '/Users/nolanlittle/workspace/python/exercises/bag_o_loot/bag_o_loot.db'


class Loot_bag:
    def find_child(self, child_name):
        """checks the db to see if child exists, if child doesn't exist it creates the child in the db.

        Arguments:
            child_name {string} -- first name of a child

        Returns:
            int -- ChildId from db, child_id
        """

        with sqlite3.connect(loot_db) as conn:
            cursor = conn.cursor()
            cursor.execute(f'''SELECT c.ChildId
                                FROM Children c
                                WHERE c.Name = '{child_name}' ''')
            child_id = cursor.fetchone()

            if child_id == None:
                 return self.create_child(child_name)
            else:
                return(child_id[0])

    def create_child(self, child_name):
        """creates a child in the db

        Arguments:
            child_name {string} -- the first name of a child

        Returns:
            integer -- ChildId from db response
        """

        with sqlite3.connect(loot_db) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO Children
                VALUES (?, ?)
                ''', (None, child_name)
            )
            return cursor.lastrowid

    def add_toy(self, child_name, toy_name):
        """Adds a toy in the db

        Arguments:
            child_name {string} -- Name of child that the toy is for
            toy_name {string} -- name of toy
        """

        with sqlite3.connect(loot_db) as conn:
            cursor = conn.cursor()

            child_id = self.find_child(child_name)
            cursor.execute(
                '''
                INSERT INTO Toys
                VALUES(?, ?, ?, ?)
                ''', (None, toy_name, child_id, 0)
            )


if __name__ == "__main__":
    loot = Loot_bag()
    loot.add_toy('Goony', 'basket')
