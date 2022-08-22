from os import geteuid


def needroot(Function):
    def wrapper(*args, **kwargs):
        if geteuid() != 0:
            print("You need to be root to run this command")
            exit(1)
        return Function(*args, **kwargs)
    return wrapper