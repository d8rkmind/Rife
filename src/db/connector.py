from multiprocessing import connection
from src.constants import PACKAGE_DB_PATH
import sqlite3


class Connection:
    def __init__(self):
        self.conn = sqlite3.connect(PACKAGE_DB_PATH)
        self.cursor = self.conn.cursor()

    def __exit__(self):
        self.conn.commit()
        self.conn.close()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS packages (
            Package TEXT NOT NULL,
            Source TEXT,
            Version TEXT ,
            Repository TEXT,
            Depends TEXT,
            Description TEXT,
            Size INT ,
            SHA256 TEXT ,
            MD5sum TEXT ,
            Filename TEXT 
        )''')
