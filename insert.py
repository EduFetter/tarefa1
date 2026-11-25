import sqlite3

connection = sqlite3.connect("db.sqlite3")

cursor = connection.cursor()

command ="INSERT INTO users (login, password) VALUES (?, ?)"
data = ("PirateToken", "137000")

cursor.execute(command, data)

connection.commit()

connection.close()

print("Feito!")