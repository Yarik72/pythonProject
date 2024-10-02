import sqlite3


def initiate_db():
    connection = sqlite3.connect("initiate.db")
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users(
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        age INTEGER NOT NULL,
        balance INTEGER NOT NULL
    )
    ''')

    cursor.execute('''
       CREATE TABLE IF NOT EXISTS Products(
           id INTEGER PRIMARY KEY,
           title TEXT NOT NULL,
           description TEXT NOT NULL,
           price INTEGER NOT NULL
       )
       ''')

    connection.commit()
    connection.close()


def add_user(username, email, age):
    connection = sqlite3.connect("initiate.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)",
                   (username, email, age, 1000))
    connection.commit()
    connection.close()


def is_included(username):
    connection = sqlite3.connect("initiate.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Users WHERE username=?", (username,))
    user_exists = cursor.fetchone() is not None
    connection.close()
    return user_exists


def get_all_products():
    connection = sqlite3.connect("initiate.db")
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Products')
    products = cursor.fetchall()
    connection.close()
    return products
