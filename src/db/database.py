from src.constants import PACKAGE_DB_PATH
import sqlite3


class Database:
    def __init__(self,):
        self.packages = []
        self.conn = sqlite3.connect(PACKAGE_DB_PATH)
        self.cursor = self.conn.cursor()

    def __exit__(self):
        self.conn.commit()
        self.conn.close()

    def search(self, package):
        self.cursor.execute(
            f"SELECT Package,Version,Repository,Depends,Size,SHA256,MD5sum,Filename FROM packages WHERE Package = '{package}'")
        return self.cursor.fetchall()
    
    def search_by_dep(self, package,repo):
        self.cursor.execute(
            f"SELECT Package,Version,Repository,Depends,Size,SHA256,MD5sum,Filename FROM packages WHERE Package = '{package}' AND instr(Repository,'{repo}')")
        return self.cursor.fetchone()

