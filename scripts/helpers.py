import subprocess as sp

def do(command):
    process = sp.Popen(command,stdout=sp.PIPE, 
                       stderr=sp.PIPE)
    stdout, _ = process.communicate()
    return stdout

def show(some_bytes):
    for line in bytes.decode(some_bytes).splitlines():
        print(line)

