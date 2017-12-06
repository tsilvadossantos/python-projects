import sqlite3

def initialize_db(databasename):
    return sqlite3.connect(databasename)

def create_user_table(databasename):
    try:
        db = initialize_db(databasename)
        # Get a cursor object
        cursor = db.cursor()
        # Check if table users does not exist and create it
        cursor.execute('CREATE TABLE IF NOT EXISTS users(username TEXT PRIMARY KEY, password TEXT)')
        # Commit the change
        db.commit()
    # Catch the exception
    except Exception as e:
        # Roll back any change if something goes wrong
        db.rollback()
        raise e
    finally:
        db.close()

def populate_users_table(databasename, username, password):
    db = initialize_db(databasename)
    create_user_table(databasename)
    cursor = db.cursor()
    cursor.execute('INSERT INTO users(username, password) VALUES(?, ?)', (username, password))
    cursor.execute('SELECT username, password FROM users')
    for row in cursor:
        print('{0} : {1}'.format(row[0], row[1]))

if __name__ == '__main__':
    username = raw_input("Inform docker registry username: ")
    password = raw_input("Inform docker registry password: ")
    populate_users_table('docker.db', username, password)
