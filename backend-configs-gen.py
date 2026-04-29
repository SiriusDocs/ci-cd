#!/usr/bin/env python3

import string
import secrets

alphabet = string.ascii_letters + string.digits

BACKEND_HOST = "api.certsirius.ru"
FRONTEND_HOST = "certsirius.ru"

def generate_secret(l):
    return ''.join(secrets.choice(alphabet) for i in range(l))


# read templates
api_gateway_template_file = open("templates/backend/api_gateway.yaml", "r")
api_gateway_template = "".join(api_gateway_template_file.readlines())
api_gateway_template_file.close()

auth_service_template_file = open("templates/backend/auth_service.yaml", "r")
auth_service_template =  "".join(auth_service_template_file.readlines())
auth_service_template_file.close()

template_service_template_file = open("templates/backend/template_service.yaml", "r")
template_service_template =  "".join(template_service_template_file.readlines())
template_service_template_file.close()


if input("Are you developer? (Y[y]/N[n]) ") in ["Y", "y"]:
    dev_flag = True
else:
    dev_flag = False

if dev_flag:
    backend_host = "localhost"
    frontend_host = "localhost"
    print("Developer mode!")
else:
    backend_host = BACKEND_HOST
    frontend_host = FRONTEND_HOST
    print("Production mode!")

print(f"backend_host: {backend_host}")
print(f"frontend_host: {frontend_host}")

input("Press Enter for writing (or Ctrl-C for exit) ")

print("Writing yaml/api_gateway.yaml ... ", end="")
api_gateway_file = open("yaml/api_gateway.yaml", "w")
api_gateway_file.write(api_gateway_template.format(
    backend_host,
    frontend_host,
    frontend_host,
    frontend_host
))
api_gateway_file.write("\n")
api_gateway_file.close()
print("done!")

print("Writing yaml/auth_service.yaml ... ", end="")
auth_service_file = open("yaml/auth_service.yaml", "w")
auth_service_file.write(auth_service_template)
auth_service_file.write("\n")
auth_service_file.close()
print("done!")

print("Writing yaml/template_service.yaml ... ", end="")
template_service_file = open("yaml/template_service.yaml", "w")
template_service_file.write(template_service_template)
template_service_file.write("\n")
template_service_file.close()
print("done!")

print("Yaml configs generated!")