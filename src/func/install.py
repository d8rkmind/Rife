from re import search
from subprocess import call
from shutil import which

from src.db.database import Database
from src.console.print import input as _input
from src.error import CantidateNotFoundError
from os import devnull

DEVNULL = open(devnull, 'w')


class Install:

    def __init__(self, args) -> None:
        self.database = Database()
        self.args = args
        self.packages = []
        self.not_found = []
        self.dependency = []
        self.search()
        self.dependency_calculate()
        print(self.packages)

    def is_installed(self, package):
        a = call(["dpkg", "-s", package], stdout=DEVNULL, stderr=DEVNULL) == 0
        b = which(package) is not None
        return a or b

    def conflit(self, data):
        message = "Conflict : {} : ".format(data[0][0])
        for index, i in enumerate(data):
            message += f"({index+1}) V{i[2]} {i[1]}  "
        return data[int(_input(message))-1]

    # def depl2(self):
    #     for package in self.packages:
    #         depends = []
    #         repo = package["Repository"].split(" ")[0].strip()
    #         for dependency in package["Depends"].split(","):
    #             dependency = dependency.split(':')[0]
    #             dependency = dependency.split('|')[0].strip()
    #             if dependency not in depends and not self.is_installed(dependency):
    #                 depends.append(dependency.strip())
    #                 data = self.database.search_by_dep(dependency, repo)
    #                 if len(data) == 0:
    #                     raise CantidateNotFoundError(dependency)
    #                 else:
    #                     data = data[0]
    #                 self.dependency.append({
    #                     "Package": data[0],
    #                     "Version": data[1],
    #                     "Repository": data[2],
    #                     "Depends": data[3],
    #                     "Size": data[4],
    #                     "SHA256": data[5],
    #                     "MD5sum": data[6],
    #                     "url": data[7]
    #                 })
    #                 for i in data[3].split(","):
    #                     i = i.split(':')[0]
    #                     i = i.split('|')[0].strip()
    #                     if i not in depends and not self.is_installed(i):
    #                         depends.append(i)
    #                         data2 = self.database.search_by_dep(i, repo)
    #                         if len(data2) == 0:
    #                             raise CantidateNotFoundError(i)
    #                         else:
    #                             data2 = data2[0]
    #                         self.dependency.append({
    #                             "Package": data2[0],
    #                             "Version": data2[1],
    #                             "Repository": data2[2],
    #                             "Depends": data2[3],
    #                             "Size": data2[4],
    #                             "SHA256": data2[5],
    #                             "MD5sum": data2[6],
    #                             "url": data2[7]
    #                         })

    def dependency_calculate(self):
        for package in self.packages:
            depends = []
            repo = package["Repository"].split(" ")[0].strip()
            # self.check_key(repo)
            for dependency in package["Depends"].split(","):
                # These are temporary solutions and needed to be changed (issue found : wpscan)
                dependency = dependency.split(':')[0]
                # These are temporary solutions and needed to be changed (issue found : wpscan)
                dependency = dependency.split('|')[0].strip()
                if dependency not in depends and not self.is_installed(dependency) and dependency not in self.dependency:
                    depends.append(dependency.strip())
                    self.dependency.append(dependency.strip())

            for dependency in depends:
                self.search_d(dependency, repo)

    def search_d(self, package, repo):
        data = self.database.search(package)
        if len(data) == 0:
            self.not_found.append(package)
            return
        elif len(data) > 1:
            data = data[0]
        else:
            data = data[0]
        self.packages.append({
            "Package": data[0],
            "Version": data[1],
            "Repository": data[2],
            "Depends": data[3],
            "Size": data[4],
            "SHA256": data[5],
            "MD5sum": data[6],
            "url": data[7]
        })

    def search(self):
        for package in self.args:
            if not self.is_installed(package):
                data = self.database.search(package)
                if len(data) == 0:
                    raise CantidateNotFoundError(package)
                elif len(data) > 1:
                    data = self.conflit(data)
                else:
                    data = data[0]
                self.packages.append({
                    "Package": data[0],
                    "Version": data[1],
                    "Repository": data[2],
                    "Depends": data[3],
                    "Size": data[4],
                    "SHA256": data[5],
                    "MD5sum": data[6],
                    "url": data[7]
                })
