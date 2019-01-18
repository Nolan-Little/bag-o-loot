import sqlite3
import sys
from io import StringIO

# sys.argv is a list of the passed in args from the command line


class Loot_bag:

    def create_conn(self):
        loot_db = ('/Users/nolanlittle/workspace/python/exercises/bag_o_loot/bag_o_loot.db')
        conn = sqlite3.connect(loot_db)
        tempfile = StringIO()

        for line in conn.iterdump():
            tempfile.write('%s\n' % line)

        conn.close()
        tempfile.seek(0)

        with sqlite3.connect (':memory:') as conn:
            cursor = conn.cursor()
            cursor.executescript(tempfile.read())
            return cursor

        # try:
        #     conn = sqlite3.connect(':memory:')
        #     print(sqlite3.version)
        # except Error as e:
        #     print(e)
        # finally:
        #     conn.close()

    def find_child(self, child_name):
        """checks the db to see if child exists, if child doesn't exist it creates the child in the db.

        Arguments:
            child_name {string} -- first name of a child

        Returns:
            int -- ChildId from db, child_id
        """

        cursor = self.create_conn()
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

        cursor = self.create_conn()
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

        cursor = self.create_conn()
        child_id = self.find_child(child_name)
        cursor.execute(
            '''
            INSERT INTO Toys
            VALUES(?, ?, ?, ?)
            ''', (None, toy_name, child_id, 0)
        )


if __name__ == "__main__":
    l = Loot_bag()
    print(l.find_child(''))