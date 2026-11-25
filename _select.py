import sqlite3

connection = sqlite3.connect("db.sqlite3")

cursor = connection.cursor()

command ="SELECT * FROM Users WHERE login = ? AND password = ?"
data = ("PirateToken", "137000")


cursor.execute(command, data)

user = cursor.fetchone()

print(user)

connection.commit()

connection.close()

print("Feito!")