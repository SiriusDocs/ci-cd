#!/usr/bin/env python3

import string
import secrets

alphabet = string.ascii_letters + string.digits

BACKEND_HOST = "api.certsirius.ru"
BACKEND_PORT = "443"

def constant_secret(init_flag, filename):
    if init_flag:
        secret = generate_secret(64)
        secret_file = open("{}.secret".format(filename), "w")
        secret_file.write("{}".format(secret))
        secret_file.close()
        return secret
    else:
        secret_file = open("{}.secret".format(filename), "r")
        secret = secret_file.readlines()[0]
        secret_file.close()
        return secret
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

api_gateway_template_file = open("templates/backend/api_gateway.env", "r")
api_gateway_template = "".join(api_gateway_template_file.readlines())
api_gateway_template_file.close()

auth_service_template_file = open("templates/backend/auth_service.env", "r")
auth_service_template =  "".join(auth_service_template_file.readlines())
auth_service_template_file.close()

template_service_template_file = open("templates/backend/template_service.env", "r")
template_service_template =  "".join(template_service_template_file.readlines())
template_service_template_file.close()

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

postgres_password = constant_secret(init_postgresql, "postgres")
env_file.write("POSTGRES_PASSWORD={}\n".format(postgres_password))

print("Setting up frontend.env ...", end="")
frontend_file = open("frontend.env", "w")
# backend link for frontend
frontend_file.write("VITE_API_URL=https://{}:{}".format(BACKEND_HOST, BACKEND_PORT))
frontend_file.close()
print("done!")


if input("Are you want to generate backend auth signing key? (Y[y]/N[n]) ") in ["Y", "y"]:
    signing_key_flag = True
else: 
    signing_key_flag  = False
signing_key = constant_secret(signing_key_flag, "auth_signing_key")

if input("Are you want to generate backend auth salt? (Y[y]/N[n]) ") in ["Y", "y"]:
    salt_flag = True
else: 
    salt_flag  = False
salt = constant_secret(salt_flag, "salt")

print("Setting up api_gateway.env ...", end="")
api_gateway_file = open("api_gateway.env", "w")
api_gateway_file.write(api_gateway_template.format(
    signing_key
))
api_gateway_file.write("\n")
api_gateway_file.close()
print("done!")

print("Setting up auth_service.env ...", end="")
auth_service_file = open("auth_service.env", "w")
auth_service_file.write(auth_service_template.format(
    postgres_password,
    signing_key,
    salt
))
auth_service_file.write("\n")
auth_service_file.close()
print("done!")

print("Setting up template_service.env ... ", end="")
template_service_file = open("template_service.env", "w")
template_service_file.write(template_service_template.format(
    postgres_password
))
template_service_file.write("\n")
template_service_file.close()
print("done!")

env_file.close()
print("Env files generated.")
