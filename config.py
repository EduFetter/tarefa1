import sqlite3

connection = sqlite3.connect("db.sqlite3")

cursor = connection.cursor()

command = '''
CREATE TABLE IF NOT EXISTS users 
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    login TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);
'''

cursor.execute(command)

connection.commit()

connection.close()

print("Feito!")