
import sqlite3
import sys
import subprocess

# sys.argv is a list of the passed in args from the command line


class Loot_bag:
    def __init__(self):
        self.db = '/Users/nolanlittle/workspace/python/exercises/bag_o_loot/loot_prod_db'


    def print_help(self):
        print(f'''
        Welcome to Bag O' Loot,
        A delivery tracking app

        add: adds a toy for a child,
                format as "add toy child"

        remove: removes a toy from bag,
                format as "remove child toy"

        ls: list all toys in the bag for all children
            format as "ls child" to see the toys for a specific child

        delivered: mark a child's toys as delivered
            format as "delivered child"
        ''')


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
                WHERE c.Name LIKE '{child_name}' ''')
            child_id = cursor.fetchone()
            if child_id == None:
                return self.create_child(child_name)
            else:
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
                SELECT c.Name as child_name, group_concat(t.Name, ', ') as toys, t.Delivered
                FROM Toys t
                INNER JOIN Children c ON c.childId = t.childId
                GROUP BY c.Name
                '''
            )

        if cursor == None:
            with sqlite3.connect(self.db) as conn:
                cursor = conn.cursor()
                select_toys(self, cursor)
                return cursor.fetchall()


        else:
            select_toys(self, cursor)
            return cursor.fetchall()


    def list_child(self, child_name,  cursor = None):

        def select_child_toys(self, child_name, cursor):
            cursor.execute(
                f'''
                SELECT c.Name, group_concat(t.Name, ', '), t.Delivered
                FROM Children c
                INNER JOIN Toys t
                ON t.ChildId = c.ChildId
                WHERE c.Name LIKE '{child_name}'
                '''
            )

        if cursor == None:
            with sqlite3.connect(self.db) as conn:
                cursor = conn.cursor()
                select_child_toys(self, child_name, cursor)
                return cursor.fetchall()


        else:
            select_child_toys(self, child_name, cursor)
            return cursor.fetchall()


    def deliver_toys(self, child_name, cursor = None):

        def update_toys(self, child_name, cursor):
            cursor.execute(
                f'''
                UPDATE Toys
                SET Delivered = 1
                WHERE Toys.ChildId IN (
                SELECT t.ChildId FROM Toys t
                LEFT JOIN Children c ON c.ChildId = t.ChildId
                WHERE c.Name LIKE '{child_name}'
                )
                '''
            )

        if cursor == None:
            with sqlite3.connect(self.db) as conn:
                cursor = conn.cursor()
                update_toys(self, child_name, cursor)
                return cursor.lastrowid

        else:
            update_toys(self, child_name, cursor)
            return cursor.lastrowid


    def print_toys(self, child):
        if len(child) ==1:
            if child[0][2] ==1:
                print(f'{child[0][0]}: {child[0][1]}(delivered)')
            else:
                print(f'{child[0][0]}: {child[0][1]}')

        elif child[2] == 1:
            print(f'{child[0]}: {child[1]}(delivered)')
        else:
            print(f'{child[0]}: {child[1]}')



if __name__ == "__main__":
    l = Loot_bag()
    if len(sys.argv) < 2:
        l.print_help()
    elif sys.argv[1] == "test":
        print("testing")
        command = 'cd test; python -m unittest -v; cd ..'
        process = subprocess.Popen(command, shell=True)
    else:

        if sys.argv[1] == 'help':
            l.print_help()

        elif sys.argv[1] == 'add':
            l.add_toy(sys.argv[2], sys.argv[3])
            print(f"added a {sys.argv[2]} to the bag for {sys.argv[3]}")

        elif sys.argv[1] == 'remove':
            l.remove_toy(sys.argv[2], sys.argv[3])
            print(f"removed {sys.argv[3]} that was for {sys.argv[2]}")

        elif sys.argv[1] == 'ls' and len(sys.argv) == 3:
            child = l.list_child(sys.argv[2])
            print(f"{sys.argv[2]}'s toys:")
            l.print_toys(child)

        elif sys.argv[1] == 'ls':
            result = l.list_toys()
            for child in result:
                l.print_toys(child)

        elif sys.argv[1] == 'delivered':
            l.deliver_toys(sys.argv[2])
            print(f"delivered {sys.argv[2]}'s toys!")

        else:
            print(f"sorry,{sys.argv[1]} is not a valid command. Try 'help' to see commands")
