from rich import print as _print
from rich.table import Table
from rich.box import SIMPLE_HEAD
from hurry.filesize import size,alternative
from src.console.print import input as _input


color = ["cyan", "blue","yellow","green"]

class Summary:
    def __init__(self,list:dict):
        sum=0
        self.grid = Table(expand=True,box=SIMPLE_HEAD,show_footer=True)
        for i in ["Package", "Version", "Repository", "Size"]:
            self.grid.add_column(i,style=color.pop())
        
        for i in list:
            sum+=int(i["Size"])
            self.grid.add_row(i["Package"],i["Version"],i["Repository"].split(" ")[0],size(i["Size"],system=alternative))
        self.grid.add_row(None,None,None,None)
        self.grid.add_row("[white]Total",None,None,f"[white]{size(sum,system=alternative)}")
        
    def ask(self):
        _print(self.grid)
        return _input("[bold] Do you want to install these packages? [ Y/n ] ").lower() == "y" , sum