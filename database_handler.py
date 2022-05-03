import sqlite3

# try:
#     sqliteConnection = sqlite3.connect('tabaseUser da ECG project')
#     cursor = sqliteConnection.cursor()
#     print("Database created and Successfully Connected to SQLite")

#     sqlite_select_Query = "select sqlite_version();"
#     cursor.execute(sqlite_select_Query)
#     record = cursor.fetchall()
#     print("SQLite Database Version is: ", record)
#     cursor.close()

# except sqlite3.Error as error:
#     print("Error while connecting to sqlite", error)
# finally:
#     if sqliteConnection:
#         sqliteConnection.close()
#         print("The SQLite connection is closed")



class Database_Handler():

    # TODO: Before working on this class, set up a database table for a User (ID, FName, LName, Email, Pass)

    # TODO: Connect to database file
    def __init__(self):
        try: 
            sqliteConnection = sqlite3.connect('HeartHealth.db')
            self.cursor = sqliteConnection.cursor()
            print("Database created and Successfully Connected to SQLite")
        except sqlite3.Error as error:
            print("Error while connecting to sqlite", error)

    # TODO: Set up a SQL query (and action) to insert user into DB using a Python dictionary.
    def insert_user(self, user):
        print(f"{str(tuple(user.keys()))}")
        print(f"{str(tuple(user.values()))}")
        
        # query = f"INSERT INTO User {str(tuple(user.keys()))} VALUES {str(tuple(user.values()))}"
        # self.cursor.execute(query)