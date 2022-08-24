from subprocess import call
from os import devnull
Devnull = devnull()
from src.constants import PKG_DOWNLOAD_PATH
def install():
    call(["dpkg","-i",f"{PKG_DOWNLOAD_PATH}*"], stdout=Devnull, stderr=Devnull)