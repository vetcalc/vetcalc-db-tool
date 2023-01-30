import subprocess as sp
import container_config as h

db = h.db

def login_database():
    command = ['podman', 'exec', '-it', f"{db['name']}", 'psql', '-U', 'postgres']
    sp.run(command)

if __name__ == "__main__":
    login_database()
