import sqlite3
import sys
import subprocess

# sys.argv is a list of the passed in args from the command line


class Loot_bag:
    def __init__(self):
        self.db = '/Users/nolanlittle/workspace/python/exercises/bag_o_loot/loot_prod_db'

    def find_child(self, child_name, cursor=None):
        """checks the db to see if child exists, if child doesn't exist it creates the child in the db.

        Arguments:
            child_name {string} -- first name of a child

        Returns:
            int -- ChildId from db, child_id
        """
        def select_child(child_name, cursor):
            cursor.execute(f'''SELECT c.ChildId
                FROM Children c
                WHERE c.Name = '{child_name}' ''')
            child_id = cursor.fetchone()
            if child_id == None:
                return self.create_child(child_name)
            else:
                print(child_id[0])
                return(child_id[0])

        if cursor == None:
            with sqlite3.connect(self.db) as conn:
                cursor = conn.cursor()
                return select_child(child_name, cursor)

        else:
            return select_child(child_name, cursor)


    def create_child(self, child_name, cursor=None):
        """creates a child in the db

        Arguments:
            child_name {string} -- the first name of a child

        Returns:
            integer -- ChildId from db response
        """
        def insert_child(child_name, cursor):
            cursor.execute('''
                INSERT INTO Children
                VALUES (?, ?)
                ''', (None, child_name)
                    )
            print(cursor.lastrowid)
            return cursor.lastrowid

        if cursor == None:
            with sqlite3.connect(self.db) as conn:
                cursor = conn.cursor()
                return insert_child(child_name, cursor)

        else:
            return insert_child(child_name, cursor)



    def add_toy(self, child_name, toy_name):
        """Adds a toy in the db

        Arguments:
            child_name {string} -- Name of child that the toy is for
            toy_name {string} -- name of toy
        """

        with sqlite3.connect(self.db) as conn:
            cursor = conn.cursor()
            child_id = self.find_child(child_name, cursor)
            cursor.execute(
                '''
                INSERT INTO Toys
                VALUES(?, ?, ?, ?)
                ''', (None, toy_name, child_id, 0)
            )


if __name__ == "__main__":
    l = Loot_bag()
    if sys.argv[1] == "test":
        print("testing")
        command = 'cd test; python -m unittest -v; cd ..'
        process = subprocess.Popen(command, shell=True)
    else:

        if sys.argv[1] == 'find':
            print("find child")
            l.find_child(sys.argv[2])
        else:
            print(f"sorry,{sys.argv[1]} not a valid command")
