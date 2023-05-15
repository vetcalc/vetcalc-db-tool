import config as h

pod = h.config["pod"]

def delete_database():
    # stop then remove the pod from system
    command = ['podman', 'pod', 'stop', f"{pod['name']}"]
    h.do(command)

    command = ['podman', 'pod', 'rm', f"{pod['name']}"]
    h.do(command)

if __name__ == "__main__":
    delete_database()