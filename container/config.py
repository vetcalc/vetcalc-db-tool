import subprocess as sp
import configparser

config = configparser.ConfigParser()
config.read("example.ini")

def do(command):
    output = sp.run(command, capture_output=True)
    if output.stderr:
        print(bytes.decode(output.stderr))
    else:
        print(bytes.decode(output.stdout))

