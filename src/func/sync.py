from __future__ import annotations
from src.utils.Downloader import Downloader
from src.utils.Extractor import Extractor
import os
from src.constants import (
    CONFIG_PATH,
    PKG_GZ_DOWNLOAD_PATH,
    SOURCE_LIST
)
from subprocess import check_output


def arch():
    return check_output('dpkg --print-architecture', shell=True).decode('utf-8').strip()


class Sync():
    def __init__(self) -> None:
        self.updatelist = []
        self.arch = arch()

        with open(CONFIG_PATH + SOURCE_LIST, "r") as f:
            lines = f.readlines()
        for i in lines:
            _list = i.split()
            # type = _list.pop(0) for future work
            folders = _list[-3:]
            url = _list[1:-3]
            for item in folders:
                self.updatelist.append({
                    'url': '{base}/dists/{repo}/{folder}/binary-{arch}/Packages.gz'.format(base=url[0], repo=url[1], folder=item, arch=self.arch),
                    'filename': '{repo}_{folder}_Package.gz'.format(repo=url[1], folder=item),
                    'displayname': str('{repo} {folder}'.format(repo=url[1], folder=item)).capitalize(),
                    'url_path': url[0],
                    'repo': "{} {}".format(url[1], item)
                })
        Downloader(self.updatelist, "Downloading Packages Files from Sources")
        Extractor(self.updatelist)