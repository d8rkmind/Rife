
from src.db.database import Database
from src.console.print import print as _print
import asyncio
from asyncio import tasks
from time import sleep
from src.error import CantidateNotFoundError


class Install:
    def __init__(self,args) -> None:
        self.Database = Database()
        self.download =[]
        asyncio.run(self.run(args))

    async def run(self,args):
        tasks = [self.start(i)  for i in args]      
        await asyncio.gather(*tasks)


    def conflit_arised(self,data:list):
        _print()

    async def start(self,value):
        result = await asyncio.gather(self.Database.search(value))
        if not result[0]:
            raise CantidateNotFoundError(value)
        elif len(result[0]) > 1:
            result = self.conflit_arised(result[0])
        else:
            result = result[0]
            