import aiosqlite
import asyncio
from src.constants import PACKAGE_DB_PATH

class Database:
    def __init__(self,):
        self.packages=[]

    async def search(self, package):
        async with aiosqlite.connect(PACKAGE_DB_PATH) as db:
            async with db.execute('SELECT * FROM packages WHERE Package=?', (package,)) as cursor:
                async for row in cursor:
                    self.packages.append(row)
        return self.packages