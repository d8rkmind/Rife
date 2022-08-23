import asyncio
import os
import sys
from src.constants import PKG_DOWNLOAD_PATH, PKG_GZ_DOWNLOAD_PATH
import aiohttp
from rich.live import Live
from rich.panel import Panel
from rich.progress import (BarColumn, DownloadColumn, Progress, SpinnerColumn,
                           TextColumn, TimeRemainingColumn, TransferSpeedColumn)
from rich.style import Style
from rich.table import Table

bar_front = Style(color="cyan")
bar_back = Style(color="red1")


class Downloader:
    def __init__(self, dictlist: dict, title: str) -> None:
        self.download_progress = Progress(
            SpinnerColumn(),
            "{task.description}",
            BarColumn(bar_width=None, style=bar_back,
                      complete_style=bar_front, finished_style=bar_front),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            "•",
            TimeRemainingColumn(),
            "•",
            DownloadColumn(),
            "•",
            TransferSpeedColumn(),
        )
        self.download_progress_table = Table.grid(expand=True)
        self.download_progress_table.add_row(
            Panel(self.download_progress,
                  title=f"[b white]{title}", title_align='left', border_style="green", padding=(1, 2)),
        )
        self.url = dictlist
        self.path = PKG_GZ_DOWNLOAD_PATH
        os.makedirs(self.path, exist_ok=True)
        try:
            asyncio.run(self.__init__download())
        except Exception:
            sys.exit(1)

    async def __init__download(self):
        with Live(self.download_progress_table, refresh_per_second=10):
            async with aiohttp.ClientSession() as session:
                task = []
                for i in self.url:
                    task.append(asyncio.ensure_future(
                        self.__download_file(session, i)))
                await asyncio.gather(*task)

    async def __download_file(self, session, urls):
        async with session.get(urls["url"]) as resp:
            if resp.status == 200:
                job = self.download_progress.add_task(
                    f"{urls['displayname']}", total=resp.content_length)
                with open(os.path.join(self.path, urls["filename"]), "wb") as f:
                    async for data in resp.content.iter_chunked(1024):
                        f.write(data)
                        self.download_progress.advance(job, advance=len(data))


class DownloaderPackage:
    def __init__(self,list:dict):
        self.list = list
        self.path = PKG_DOWNLOAD_PATH
        os.makedirs(self.path, exist_ok=True)
        

    def __init__download(self):
        for i in self.list:
            self.__download_file(i)