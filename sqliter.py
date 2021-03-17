import sqlite3


class SQLighter:

    def __init__(self, tables):
        self.connection = sqlite3.connect(tables)
        self.cursor = self.connection.cursor()

    def create(self):
        command = (
            """
            CREATE TABLE IF NOT EXISTS animals (
                id INTEGER NOT NULL PRIMARY KEY,
                letter TEXT,
                animal TEXT
                )
            """
        )
        with self.connection:
            return self.cursor.execute(command)

    def add_animal(self, letter, animal):
        with self.connection:
            self.cursor.execute("INSERT or IGNORE into 'animals' ('letter', 'animal') VALUES(?,?)", (letter, animal))
