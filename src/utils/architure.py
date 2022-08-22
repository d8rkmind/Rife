from subprocess import check_output

def arch():
    return check_output('dpkg --print-architecture', shell=True).decode('utf-8').strip()
