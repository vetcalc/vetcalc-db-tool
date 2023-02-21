import subprocess as sp
import config as h


db = h.config["db"]

def login_database():
    command = ['podman', 'exec', '-it', f"{db['name']}", 'psql', '-U', 'postgres']
    sp.run(command)

if __name__ == "__main__":
    login_database()
