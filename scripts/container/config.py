import subprocess as sp

def do(command):
    output = sp.run(command, capture_output=True)
    if output.stderr:
        print(bytes.decode(output.stderr))
    else:
        print(bytes.decode(output.stdout))

pod = {
    'name' : 'vaddb'
}

db = {
    'name' : 'vaddb_pg',
    'port_map' : '33333:5432',
    'registry_image' : 'docker.io/library/postgres',
    'superuser_password' : 'mysecretpassword'
}


