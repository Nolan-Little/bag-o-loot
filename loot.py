import sqlite3
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

    def add_toy(self, toy_name, child_name, cursor=None):
        """Adds a toy in the db

        Arguments:
            child_name {string} -- Name of child that the toy is for
            toy_name {string} -- name of toy
        """
        def insert_toy(toy_name, child_name, cursor):
            cursor.execute(
                '''
                INSERT INTO Toys
                VALUES(?, ?, ?, ?)
                ''', (None, toy_name, child_id, 0)
            )

        if cursor == None:
            with sqlite3.connect(self.db) as conn:
                cursor = conn.cursor()
                child_id = self.find_child(child_name)
                return insert_toy(toy_name, child_name, cursor)
        else:
            return insert_toy(toy_name, child_name, cursor)

    def remove_toy(self, child_name, toy_name, cursor=None):

        def delete_toy(child_name, toy_name, cursor):
            cursor.execute(
                f'''
                DELETE FROM Toys
                WHERE Toys.ChildId IN (
	            SELECT Toys.ChildId FROM Toys
	            INNER JOIN Children c ON c.ChildId = Toys.ChildId
	            WHERE c.Name Like '{child_name}'
                ) AND Toys.name LIKE '{toy_name}'
                '''
            )

        if cursor == None:
            with sqlite3.connect(self.db) as conn:
                cursor = conn.cursor()
                return delete_toy(child_name, toy_name,cursor)

        else:
            return delete_toy(child_name, toy_name,cursor)


    def list_toys(self, cursor = None):

        def select_toys(self, cursor):
            cursor.execute(
                '''
                SELECT c.Name as child_name, group_concat(t.Name, ', ') as toys from Toys t
                INNER JOIN Children c ON c.childId = t.childId
                WHERE t.delivered != 1
                GROUP BY c.Name
                '''
            )

        if cursor == None:
            with sqlite3.connect(self.db) as conn:
                cursor = conn.cursor()
                select_toys(self, cursor)
                result = cursor.fetchall()
                for child in result:
                    print(f'{child[0]}: {child[1]}')

        else:
            select_toys(self, cursor)
            print(cursor.fetchall())


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

        if sys.argv[1] == 'add':
            print("add toy", sys.argv[2], sys.argv[3])
            l.add_toy(sys.argv[2], sys.argv[3])

        if sys.argv[1] == 'remove':
            print(f"remove {sys.argv[3]} for {sys.argv[2]}")
            l.remove_toy(sys.argv[2], sys.argv[3])

        if sys.argv[1] == 'ls':
            l.list_toys()

        else:
            print(f"sorry,{sys.argv[1]} not a valid command")