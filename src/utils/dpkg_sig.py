from pydpkg import Dpkg
from src.constants import PKG_DOWNLOAD_PATH
import os 


def signature(package):
    for i in package:
        dp = Dpkg(os.path.join(PKG_DOWNLOAD_PATH, str(i['url'].split('/')[-1]).strip()))
        if not (dp.sha256 == i['SHA256'] and dp.md5 == i['MD5sum']):
            raise Exception(f"{i['Package']} Package signature is not valid")