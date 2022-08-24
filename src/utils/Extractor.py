import gzip
import os
from src.constants import PKG_GZ_DOWNLOAD_PATH, PACKAGE_DB_PATH
from rich.live import Live
from rich.panel import Panel
from rich.spinner import Spinner
import re
from src.db.connector import Connection
import asyncio


keys = ["Package", "Source", "Version",
        "Depends", 'Description', "Size", "SHA256", "MD5sum","Priority", "Filename"]
spinner = Spinner(
    'dots2', text='[bold] Updating the information to the Database', style="bold")
panel = Panel(spinner)


class Extractor:
    def __init__(self, updatelist):
        try:
            os.remove(PACKAGE_DB_PATH)
        except FileNotFoundError:
            pass
        with Live(panel, refresh_per_second=10):
            self.db = Connection()
            self.db.create_table()
            self.updatelist = updatelist
            asyncio.run(self.init_download())
            self.db.__exit__()

    async def extract(self, package, repo, url_path):
        getpack = {}
        with gzip.open(PKG_GZ_DOWNLOAD_PATH+package, 'rb') as f:
            for line in f:
                key, value = line.decode().strip().partition(':')[::2]
                if key in keys and value:
                    if key == 'Filename':
                        value = "/".join([url_path.strip(), value.strip()])

                    getpack[key] = re.sub(r'\([^)]*\)',
                                          "", value.strip()) if value else None
                elif key == "":
                    getpack['Repository'] = repo
                    self.db.cursor.execute(
                        f"INSERT INTO packages ({ ','.join(getpack.keys())}) VALUES ({ ', '.join('?' * len(getpack.keys()))})", [getpack[i] for i in getpack.keys()])

    async def init_download(self):
        task = []
        for data in self.updatelist:
            task.append(asyncio.ensure_future(self.extract(
                data['filename'], data['repo'], data['url_path'])))
        await asyncio.gather(*task)
