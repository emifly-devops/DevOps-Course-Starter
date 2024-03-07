import os
import json

from jinja2 import Environment, PackageLoader

env = Environment(
    loader=PackageLoader(__name__)
)

try:
    # Attempt to load config vars from file
    with open("terraform.tfvars.json") as tfvars_file:
        tfvars = json.load(tfvars_file)
except IOError:
    # If loading from file failed, load config vars from environment
    required_vars = ["resource_group_name", "storage_account_name", "container_name"]
    tfvars = {
        var: os.environ.get(var.upper()) for var in required_vars
    }

template = env.get_template("azurerm.tfbackend.j2")
print(template.render(
    resource_group_name=tfvars.get("resource_group_name"),
    storage_account_name=tfvars.get("storage_account_name"),
    container_name=tfvars.get("container_name"),
))
