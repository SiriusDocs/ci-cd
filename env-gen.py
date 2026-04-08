#!/usr/bin/env python3

import string
import secrets

alphabet = string.ascii_letters + string.digits

BACKEND_HOST = "api.certsirius.ru"
BACKEND_PORT = "443"


def generate_secret(l):
    return ''.join(secrets.choice(alphabet) for i in range(l))
    

def constant_password(init_flag, env_name, filename):
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

if input("Init a new postgresql password? [y/N]: ") in ["y", "Y"]:
    init_postgresql = True
    input("Do you really want init? (press Enter or Ctrl-C to exit)")
    print("Init -> YES")
else:
    init_postgresql = False 
    print("Init -> NO")
     

env_file = open(".env", "w")

# .env header
env_file.write("# This file generated AUTOMATICALLY. DONT'T CHANGE THIS!\n")
env_file.write("# If you want to add/remove/change any strings, you should rewrite env-gen.py!\n")

# .env data
env_file.write("POSTGRES_USER=postgres\n")
env_file.write("POSTGRES_DB=postgres\n")
env_file.write("POSTGRES_HOST=db\n")

constant_password(init_postgresql, "POSTGRES_PASSWORD", "postgres")

print("Setting up frontend.env ...", end="")
frontend_file = open("frontend.env", "w")
# backend link for frontend
frontend_file.write("VITE_API_URL=https://{}:{}".format(BACKEND_HOST, BACKEND_PORT))
frontend_file.close()
print("done!")

env_file.close()
print("Env files generated.")
