import config as h

pod = h.config["pod"]
db = h.config["db"]

def start_database():
    # start the pod
    command = ['podman', 'pod', 'create', 
               '--name', pod['name'], 
               '-p', db['port_map']]
    h.do(command)

    # add the database to the pod
    command = ['podman', 'run', 
               f"--pod={pod['name']}", 
               '--name', db["name"], 
               '-e', f"POSTGRES_PASSWORD={db['superuser_password']}", 
               '-v', "./data:/var/lib/postgresql/data", 
               '-d', 
               db['registry_image']]
    h.do(command)


if __name__ == "__main__":
    start_database()
