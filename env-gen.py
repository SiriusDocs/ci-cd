#!/usr/bin/env python3

import string
import secrets

alphabet = string.ascii_letters + string.digits

def generate_secret(l):
    return ''.join(secrets.choice(alphabet) for i in range(l))

def db_password(init_flag, env_name, filename):
    if init_flag:
        password = generate_secret(64)
        env_file.write("{}={}\n".format(env_name, password))
        db_file = open("{}.env".format(filename), "w")
        db_file.write("{}".format(password))
        db_file.close()
    else:
        db_file = open("{}.env".format(filename), "r")
        password = db_file.readlines()[0]
        db_file.close()
        env_file.write("{}={}\n".format(env_name, password))
    
env_file = open(".env", "w")

if input("Init a new postgresql password? [y/N]: ") in ["y", "Y"]:
    init_postgresql = True
    input("Do you really want init? (press Enter)")
    print("Init -> YES")
else:
    init_postgresql = False 
    print("Init -> NO")
    
# .env header
env_file.write("# This file generated AUTOMATICALLY. DONT'T CHANGE THIS!\n")
env_file.write("# If you want to add/remove/change any strings, you should rewrite env-gen.py!\n")

env_file.write("POSTGRES_USER=postgres\n")
env_file.write("POSTGRES_DB=postgres\n")
env_file.write("POSTGRES_HOST=db\n")

db_password(init_postgresql, "POSTGRES_PASSWORD", "postgres")

env_file.close()
print("Done.")
