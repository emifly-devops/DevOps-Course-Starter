import os
import json

required_vars = ["resource_group_name", "storage_account_name", "container_name"]

try:
    # Attempt to load config vars from file
    with open("backend.tfvars.json") as tfvars_file:
        tfvars = json.load(tfvars_file)
except IOError:
    # If loading from file failed, load config vars from environment
    tfvars = {var: os.environ.get(var.upper()) for var in required_vars}

with open("azurerm.tfbackend.template") as template:
    content = template.read()
    for var in required_vars:
        content = content.replace(f"${var}", tfvars.get(var))
    print(content)
