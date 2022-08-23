
from subprocess import call
from shutil import ExecError, which
from src.utils.summary import Summary
from src.db.database import Database
from src.console.print import input as _input
from src.error import CantidateNotFoundError
from os import devnull
from rich.live import Live
from rich.panel import Panel
from rich.progress import (Progress, SpinnerColumn,TimeElapsedColumn,)
DEVNULL = open(devnull, 'w')
progress = Progress(
    SpinnerColumn(style="bold"),
    "{task.description} : ",
    TimeElapsedColumn(),
)
panel = Panel(progress)
progress.add_task(description="Calculating dependencies",)


class Install:

    def __init__(self, args) -> None:
        self.database = Database()
        self.args = args
        self.packages = []
        self.not_found = []
        self.dependency = []
        self.search()
        with Live(panel, refresh_per_second=10):
            self.dependency_calculate()
            self.database.__exit__()
        self.sum = Summary(self.packages)
        ask,sum = self.sum.ask()
        if not ask:
            raise ExecError("Installation aborted")

    def is_installed(self, package):
        a = call(["dpkg", "-s", package], stdout=DEVNULL, stderr=DEVNULL) == 0
        b = which(package) is not None
        return a or b

    def conflit(self, data):
        message = "Conflict : {} : ".format(data[0][0])
        for index, i in enumerate(data):
            message += f"({index+1}) {i[2]} V {i[1]}  "
        return data[int(_input(message))-1]

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
        self.write_value(data)

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
                self.write_value(data)

    def write_value(self, data):
        value = {
            "Package": data[0],
            "Version": data[1],
            "Repository": data[2],
            "Depends": data[3],
            "Size": data[4],
            "SHA256": data[5],
            "MD5sum": data[6],
            "url": data[7]
        }

        if value not in self.packages:
            self.packages.append(value)
