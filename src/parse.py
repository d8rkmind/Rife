import os
import click
from subprocess import call
from src.constants import CONFIG_PATH, PACKAGE_PATH, PKG_DOWNLOAD_PATH, PKG_GZ_DOWNLOAD_PATH, SOURCE_LIST, DEFAULT_MIRROR
from src.utils.needroot import needroot
from src.func.sync import Sync
from src.func.install import Install


@click.group()
def __main__():
    pass


@__main__.command("edit", help="Edit the sources.list")
@needroot
def edit():
    check()
    call(['nano', CONFIG_PATH+SOURCE_LIST])


@__main__.command("sync", help="Updates list of available repositories")
@needroot
def sync():
    check()
    Sync()


@__main__.command("install", help="Install a package")
@click.argument('args', nargs=-1)
@needroot
def install(args):
    if len(args) > 0:
        Install(args)

def check():
    for i in [PKG_DOWNLOAD_PATH, PKG_GZ_DOWNLOAD_PATH,CONFIG_PATH,PACKAGE_PATH]:
        os.makedirs(i, exist_ok=True)
    if not os.path.exists(CONFIG_PATH+SOURCE_LIST):
        with open(CONFIG_PATH+SOURCE_LIST, 'w') as f:
            f.write(DEFAULT_MIRROR)
        