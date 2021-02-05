import sqlite3

class Database:
    """
    Main database connection class.
    Returns a cursor object.
    """
    def __init__(self, path_to_db="database.db"):
        self._db = path_to_db

    def __enter__(self):
        self._conn = sqlite3.connect(self._db)
        cursor = self._conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS cards (id INTEGER PRIMARY KEY, front TEXT, back TEXT)")
        
        return cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._conn.commit()
        self._conn.close()

class Flashcards:
    """
    Base class that interacts with the database.
    Only class methods and variables.
    """
    db_file = "database.db"

    @classmethod
    def set_db_file(cls, path):
        cls.db_file = path

    @classmethod
    def add(cls, _front, _back):
        with Database(cls.db_file) as db:
            db.execute("INSERT INTO cards VALUES (NULL,?,?)",(_front, _back))

    @classmethod
    def view(cls):
        with Database(cls.db_file) as db:
            db.execute("SELECT * FROM cards")
            rows = db.fetchall()

        return rows

    @classmethod
    def update(cls, _id, _front, _back):
        with Database(cls.db_file) as db:
            db.execute("UPDATE cards SET front=?, back=? WHERE id=?",(_front, _back, _id))

    @classmethod
    def delete(cls, _id):
        with Database(cls.db_file) as db:
            db.execute("DELETE FROM cards WHERE id=?",(_id,))

    @classmethod
    def delete_all(cls):
        with Database(cls.db_file) as db:
            db.execute("DELETE FROM cards")
    


    
