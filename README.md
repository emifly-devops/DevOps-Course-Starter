# DevOps Apprenticeship: Project Exercise

## System Requirements

## Python and Poetry

The project uses Poetry for Python to create an isolated environment and manage package dependencies.
To prepare your system, ensure you have an official distribution of Python (at least version 3.8) and install Poetry using the following command:

```bash
curl -sSL https://install.python-poetry.org | python -
```

### MongoDB

MongoDB is used as the project database. To install the Community Edition locally, follow the instructions on the [MongoDB website](https://www.mongodb.com/docs/manual/administration/install-community/).

## Optional Installations

### Node and NPM

If you wish to run the end-to-end tests associated with the app, you will also need to have Node installed - follow the [installation steps on the website](https://nodejs.org/).
It should come with the package manager NPM, which is also required.

### Vagrant

A production configuration has been provided for Vagrant if you wish to run the app in a virtual machine.
Again, follow the [installation steps on the website](https://www.vagrantup.com) if this is of interest.
You will need a hypervisor available if you choose to take this route. If in doubt, [VirtualBox](https://www.virtualbox.org) is a good option.

### Ansible

A production configuration has been provided for Ansible if you wish to run the app on a managed node.
To install Ansible, simply run the following in the terminal of the machine you wish to use as the control node:

```bash
pip install ansible
```

### Docker

Various configurations have been provided for Docker if you wish to run the app or its associated tests in a container.
To install Docker Desktop, follow the [installation steps on the website](https://www.docker.com/products/docker-desktop/).
Ensure that it is running locally before attempting any of the Docker-specific instructions below.

### Terraform

Terraform can be used to automate the creation of Azure resources.
To install Terraform, follow the [instructions on the website](https://developer.hashicorp.com/terraform/install).

## Dependencies

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
poetry install
```

For the end-to-end tests, you will need to install the dependencies in the `package.json` file using the following command:

```bash
npm install
```

You'll also need to copy a new `.env` file from the `.env.template` to store local configuration options. This is a one-time operation on first setup:

```bash
cp .env.template .env  # (first time only)
```

There are five values that need to be set:

```dotenv
OAUTH_CLIENT_ID=oauth-client-id
OAUTH_CLIENT_SECRET=oauth-client-secret
CYPRESS_OAUTH_USERNAME=cypress-oauth-username
CYPRESS_OAUTH_PASSWORD=cypress-oauth-password
CYPRESS_OAUTH_OTP_SECRET=cypress-oauth-otp-secret
```

The `OAUTH_CLIENT_ID` and `OAUTH_CLIENT_SECRET` settings are used to provide the client details for the **non-production** GitHub app being used for authentication. (See details in the section immediately below.)

The `CYPRESS_OAUTH_USERNAME` and `CYPRESS_OAUTH_PASSWORD` settings are used to store a valid GitHub username-password combination to be used to log in to the app for testing purposes.

If the GitHub account associated with the username and password above uses two-factor authentication, the `CYPRESS_OAUTH_OTP_SECRET` setting should be used to store the account's two-factor secret.
This can be obtained by following the setup key link in the Authenticator App section of the account's Password and Authentication settings.

## Authentication

The project uses OAuth via GitHub for authentication of users.

To get this working, you will first need to set up an OAuth app for non-production environments on GitHub by following the [documentation](https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/creating-an-oauth-app).

For the homepage URL field, enter the address for accessing the website locally ([`http://localhost:5000/`]() unless configured otherwise; see the development configuration section immediately below).

For the callback URL field, enter [`http://localhost:5000/login/github/authorized`]().

Note that you will need a second app for your production environment, where your URLs will be different.
When creating the app, simply swap out the [`http://localhost:5000/`]() domain in each URL above for your live domain.
If you follow the [Azure deployment instructions](#Deployment-with-Docker-and-Azure) below, this live domain will be [https://$WEBAPP_NAME.azurewebsites.net/](), where `$WEBAPP_NAME` should be swapped out for your web app name as configured in Azure.

## Running the App with a Development Configuration

Once the all dependencies have been installed, start the Flask app in development mode within the Poetry environment by running:

```bash
poetry run flask run
```

Alternatively, if you have chosen to install Node, you can simply run the following command:

```bash
npm start
```

In each case, visit [`http://localhost:5000/`]() in your web browser to view the app.

## Running the App with a Production Configuration

If you have chosen to install Vagrant, run the following command from the `vagrant` folder to try out a production configuration locally:

```bash
vagrant up
```

With this option, visit [`http://localhost:5000/`]() in your web browser to view the app, as before.

If you have chosen to install Ansible, change the contents of the `inventory.ini` file to reflect your managed node's IP address and run the following from your control node:

```bash
ansible-playbook ansible/playbook.yml -i ansible/inventory.ini
```

You will be prompted to enter two secrets: your Flask secret key and your Mongo URI. You should use the same values that you have stored in your `.env` file.
With this option, visit the IP address of your managed node in your browser to view the app.

If you have chosen to install Docker, navigate into the `docker` directory and run the following to try out a production configuration locally:

```bash
docker compose --file docker-compose.local.yml up production --build
```

With this option, visit [`http://localhost:5000/`]() in your web browser to view the app, as before.

## Running the Tests

### Unit and Integration Tests with Pytest

Use the following command to run the unit and integration tests associated with the app:

```bash
poetry run pytest
```

Alternatively, if you have chosen to install Node, you may run the following instead:

```bash
npm run test:pytest
```

To run these tests in a container using Docker, navigate into the `docker` directory and use the following command instead:

```bash
docker compose --file docker-compose.pytest.yml up pytest --build
```

### End-to-end Tests with Cypress

This project uses Cypress for some basic end-to-end testing. To run these tests, you will need to first start the app, and then use the following command:

```bash
npm run test:cypress
```

To run these tests in a container using Docker, navigate into the `docker` directory and use the following command instead:

```bash
docker compose --file docker-compose.cypress.yml --env-file ../.env up cypress --build --abort-on-container-exit
```

In this case, there is no need to manually start the app - Docker will take care of this as well as automatically tearing it down when the tests are complete.

## Deployment with Docker and Azure

### Common Steps

If you wish to host your app's container images using the Docker Hub, you will need to [set up a Docker Hub account](https://hub.docker.com/signup).
Once you have done so, create a public repository called `todo-app`.

To build and push your production Docker image to the Docker Hub manually, you will need to first navigate into the `docker` directory and then run the following commands, using the Docker Hub username you created previously:

```bash
EXPORT DOCKERHUB_USERNAME=...
docker login
docker compose build production
docker compose push production
```

To set up an Azure account, first ensure you have a Microsoft account, and then visit the [Azure Portal](https://portal.azure.com) and use this Microsoft account to register.
Once you have done this, you will also need to create a subscription - this is achieved by clicking the Subscriptions blade under Azure services and then clicking Add.
Next, within this subscription, create a resource group by choosing the Resource groups blade, again under Azure services, and then clicking Create.

For Azure, if you wish to set up resources within your new account locally, you first need to log in.
For this, run the following command and follow the ensuing steps:

```bash
az login
```

### Option 1: Manual Steps

To manually create Azure App Service and Azure CosmosDB resources for your app, you will need to run the following commands from a Bash shell, setting the environment variables to appropriate values:

```bash
export RESOURCE_GROUP_NAME=...
export APPSERVICE_PLAN_NAME=...
export WEBAPP_NAME=...
export DOCKERHUB_USERNAME=...
export COSMOS_ACCOUNT_NAME=...
az appservice plan create -g $RESOURCE_GROUP_NAME -n $APPSERVICE_PLAN_NAME --sku F1 --is-linux
az webapp create -g $RESOURCE_GROUP_NAME -p $APPSERVICE_PLAN_NAME -n $WEBAPP_NAME --deployment-container-image-name docker.io/$DOCKERHUB_USERNAME/todo-app:latest
az webapp config appsettings set -g $RESOURCE_GROUP_NAME -n $WEBAPP_NAME --settings `cat .env | grep -v '^#' | tr '\n' ' '`
az cosmosdb create --name $COSMOS_ACCOUNT_NAME --resource-group $RESOURCE_GROUP_NAME --kind MongoDB --capabilities EnableServerless --server-version 4.2
az cosmosdb mongodb database create --account-name $COSMOS_ACCOUNT_NAME --name todo_app --resource-group $RESOURCE_GROUP_NAME
```

Note that you should use the resource group name and Docker Hub username you created previously, but you will need to choose your app service plan name, web app name and CosmosDB account name, with the web app name needing to be globally unique within Azure.

Once you have done this, retrieve the primary connection string for your CosmosDB account by running the following command, ensuring that your environment variables from the previous set of commands are still set:

```bash
az cosmosdb keys list --type connection-strings --name $COSMOS_ACCOUNT_NAME --resource-group $RESOURCE_GROUP_NAME
```

Finally, run the following commands to set environment variables for your app:

```bash
export SECRET_KEY=...
export MONGO_URI=...
export OAUTH_CLIENT_ID=...
export OAUTH_CLIENT_SECRET=...
az webapp config appsettings set --name $WEBAPP_NAME --resource-group $RESOURCE_GROUP_NAME --settings SECRET_KEY=$SECRET_KEY MONGO_URI=$MONGO_URI OAUTH_CLIENT_ID=$OAUTH_CLIENT_ID OAUTH_CLIENT_SECRET=$OAUTH_CLIENT_SECRET
```

The `SECRET_KEY` setting is used to secure the Flask session. You should generate a random sequence of characters to use for this setting.

The `MONGO_URI` setting should contain the primary connection string you retrieved above.

For `OAUTH_CLIENT_ID` and `OAUTH_CLIENT_SECRET`, you should **not** use the same values that you saved in your `.env` file (as these will be the **non-production** values). Instead, you should use the values for the **production** OAuth app you set up in the [Authentication](#Authentication) section above.

Your deployed web app will be available at [https://$WEBAPP_NAME.azurewebsites.net/]() in due course.

### Option 2: Automated Steps using Terraform

As preparation, you should manually create an Azure storage account to contain your Terraform configuration. Use the following commands, setting the environment variables to appropriate values:

```bash
export RESOURCE_GROUP_NAME=...
export STORAGE_ACCOUNT_NAME=...
export CONTAINER_NAME=...
az storage account create --resource-group $RESOURCE_GROUP_NAME --name $STORAGE_ACCOUNT_NAME --sku Standard_LRS --encryption-services blob
az storage container create --name $CONTAINER_NAME --account-name $STORAGE_ACCOUNT_NAME
```

You should use the resource group name that you created previously, but you will need to choose your storage account name and container name.

Once this is done, navigate into the `terraform` directory.
Then, create the following two files containing the specified config variables:

`backend.tfvars.json`
```json
{
  "resource_group_name": "resource-group-name",
  "storage_account_name": "storage-account-name",
  "container_name": "container-name"
}
```

Replace the dummy values with the same values you used in the storage account creation step above.

`terraform.tfvars.json`
```json
{
  "resource_group_name": "resource-group-name",
  "cosmos_account_name": "cosmos-account-name",
  "appservice_plan_name": "appservice-plan-name",
  "webapp_name": "webapp-name",
  "dockerhub_username": "dockerhub-username",
  "secret_key": "secret-key",
  "oauth_client_id": "oauth-client-id",
  "oauth_client_secret": "oauth-client-secret"
}
```

Check the [Option 1](#Option-1-Manual-Steps) section above for instructions for swapping out the dummy values for real ones.
The requirements for each value are identical to those in that section.

Once these two files are set up, run the following commands to initialise your Terraform backend and resources:

```bash
terraform init -backend-config=<(python -m generate_backend_config)
terraform apply
```

Your deployed web app will be available at [https://prod-$WEBAPP_NAME.azurewebsites.net/]() by default, unless you change the prefix variable away from "prod".
Note that your `OAUTH_CLIENT_ID` and `OAUTH_CLIENT_SECRET` must be for a GitHub OAuth app set up with this as the domain for the homepage and redirect URLs (see the [Authentication](#Authentication) section above) .

### Refreshing the Web App

To manually refresh your app when you push a new version of your image to the Docker Hub, send a post request to your web app's CD webhook URL.
One way of doing this is to install the cURL utility and run the following command, filling in your webhook URL:

```bash
curl -f -X POST '...'  # (Single quotation marks important here)
```

If you set up your infrastructure manually, you should use the same webhook URL you obtained in the previous section.
If you used Terraform to set up your infrastructure, you can obtain your webhook URL by running the following command:

```bash
terraform output -raw webapp_cd_webhook_url
```

## Pipelines

### GitHub Actions

A workflow file called `ci-cd-pipeline.yml` has been set up in order to validate any non-documentation changes upon new pushes or pull requests to the project's GitHub repository.
Upon successful validation of the changes, it is also configured to build and push a Docker image to the Docker Hub, and use this new image as the basis for an Azure web app.
In order to get this working with a fork of the repository, it should be necessary to create the following GitHub Actions secrets:

```dotenv
ARM_CLIENT_ID
ARM_CLIENT_SECRET
ARM_SUBSCRIPTION_ID
ARM_TENANT_SECRET
```

These values will be used to authenticate with Azure using a service principal as part of the pipeline.
To set one up, first obtain your Azure subscription ID using the following command:

```bash
az account list
```

From here, pick out the subscription ID that corresponds with the subscription that contains your resource group.
Once you have this, run the following commands to create the service principal:

```bash
export SUBSCRIPTION_ID=...
export RESOURCE_GROUP_NAME=...
export SERVICE_PRINCIPAL_NAME=...
az ad sp create-for-rbac --name $SERVICE_PRINCIPAL_NAME --role Contributor --scopes "/subscriptions/$SUBSCRIPION_ID/resourceGroups/$RESOURCE_GROUP_NAME"
```

You should use the subscription ID you obtained in the previous step and the same resource group name you have used in earlier steps.
You should choose a name for the service principal at this point.
The last command should output some data in JSON format if all is successful. The values for our GitHub Actions secrets should correspond to each piece of data as follows:

```text
appId -> ARM_CLIENT_ID
password -> ARM_CLIENT_SECRET
tenant -> ARM_TENANT_SECRET
```

Finally, the `ARM_SUBSCRIPTION_ID` should be set to the subscription ID we used throughout this process.

```dotenv
DOCKERHUB_USERNAME
DOCKERHUB_TOKEN
```

Your Docker Hub username should be the username you used to create your Docker Hub account.
Your Docker Hub token should be obtained via the settings page of your Docker Hub account.

```dotenv
OAUTH_CLIENT_ID
OAUTH_CLIENT_SECRET
CYPRESS_OAUTH_USERNAME
CYPRESS_OAUTH_PASSWORD
CYPRESS_OAUTH_OTP_SECRET
```

The values of these settings should be the same as the values in your `.env` file.

```dotenv
RESOURCE_GROUP_NAME
STORAGE_ACCOUNT_NAME
CONTAINER_NAME
```

The values of these settings should be the same as those at the start of the [Option 2](#Option-2-Automated-Steps-using-Terraform) section of the deployment instructions above.

```dotenv
TF_VAR_DOCKERHUB_USERNAME
TF_VAR_RESOURCE_GROUP_NAME
TF_VAR_COSMOS_ACCOUNT_NAME
TF_VAR_APPSERVICE_PLAN_NAME
TF_VAR_WEBAPP_NAME
TF_VAR_OAUTH_CLIENT_ID
TF_VAR_OAUTH_CLIENT_SECRET
TF_VAR_SECRET_KEY
```

The values of these settings should be the same as those in the [Option 1](#Option-1-Manual-Steps)/[Option 2](#Option-2-Automated-Steps-using-Terraform) sections of the deployment instructions above.
