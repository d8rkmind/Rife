import os
import click
from subprocess import call
from src.constants import CONFIG_PATH, SOURCE_LIST
from src.utils.needroot import needroot
from src.func.sync import Sync
from src.func.install import Install


@click.group()
def __main__():
    pass


@__main__.command("edit", help="Edit the sources.list")
@needroot
def edit():
    call(['nano', CONFIG_PATH+SOURCE_LIST])


@__main__.command("sync", help="Updates list of available repositories")
@needroot
def sync():
    Sync()

@__main__.command("install", help="Install a package")
@click.argument('args', nargs=-1)
@needroot
def install(args):
    if len(args) > 0:
        Install(args)