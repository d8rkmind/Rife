from rich.console import Console
console = Console()

def print_error(message):
    console.print(message, style="red")

def print_success(message):
    console.print(message, style="green")

def print_info(message):
    console.print(message, style="cyan")

def print_warning(message):
    console.print(message, style="yellow")

def print(message):
    console.print(message)
def input(message):
    return console.input(message)