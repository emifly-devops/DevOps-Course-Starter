# DevOps Apprenticeship: Project Exercise

## System Requirements

## Python and Poetry

The project uses Poetry for Python to create an isolated environment and manage package dependencies.
To prepare your system, ensure you have an official distribution of Python version 3.7+ and install Poetry using the following command:

```bash
$ curl -sSL https://install.python-poetry.org | python -
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
$ pip install ansible
```

### Docker

Various configurations have been provided for Docker if you wish to run the app or its associated tests in a container.
To install Docker Desktop, follow the [installation steps on the website](https://www.docker.com/products/docker-desktop/).
Ensure that it is running locally before attempting any of the Docker-specific instructions below.

## Dependencies

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
$ poetry install
```

For the end-to-end tests, you will need to install the dependencies in the `package.json` file using the following command:

```bash
$ npm install
```

You'll also need to clone a new `.env` file from the `.env.template` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

There are two values that need to be set:

```dotenv
SECRET_KEY=secret-key
MONGO_URI=mongo-uri
```

The `SECRET_KEY` setting is used to secure the Flask session. You should generate a random sequence of characters to use for this setting.

The `MONGO_URI` setting is used to provide connection details for the MongoDB instance being used in production. This should be set to the primary connection string of a suitable Azure CosmosDB account. (See instructions for setting this up in the [Deployment with Docker and Azure](#Deployment-with-Docker-and-Azure) section below.)

## Running the App with a Development Configuration

Once the all dependencies have been installed, start the Flask app in development mode within the Poetry environment by running:

```bash
$ poetry run flask run
```

Alternatively, if you have chosen to install Node, you can simply run the following command:

```bash
$ npm start
```

In each case, visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

## Running the App with a Production Configuration

If you have chosen to install Vagrant, run the following to try out a production configuration locally:

```bash
$ vagrant up
```

With this option, visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app, as before.

If you have chosen to install Ansible, change the contents of the `inventory.ini` file to reflect your managed node's IP address and run the following from your control node:

```bash
$ ansible-playbook ansible/playbook.yml -i ansible/inventory.ini
```

You will be prompted to enter two secrets: your Flask secret key and your Mongo URI. You should use the same values that you have stored in your `.env` file.
With this option, visit the IP address of your managed node in your browser to view the app.

If you have chosen to install Docker, run the following to try out a production configuration locally:

```bash
$ docker compose up production --build
```

With this option, visit [`http://localhost:8080/`](http://localhost:8080/) in your web browser to view the app.

## Running the Tests

### Unit and Integration Tests with Pytest

Use the following command to run the unit and integration tests associated with the app:

```bash
$ poetry run pytest
```

Alternatively, if you have chosen to install Node, you may run the following instead:

```bash
$ npm run test:pytest
```

To run these tests in a container using Docker, use the following command instead:

```bash
$ docker compose --file docker-compose.pytest.yml up pytest --build
```

### End-to-end Tests with Cypress

This project uses Cypress for some basic end-to-end testing. To run these tests, you will need to first start the app, and then use the following command:

```bash
$ npm run test:cypress
```

To run these tests in a container using Docker, use the following command instead:

```bash
$ docker compose --file docker-compose.cypress.yml up cypress --build --abort-on-container-exit
```

In this case, there is no need to manually start the app - Docker will take care of this for us as well as automatically tearing it down when the tests are complete.

## Deployment with Docker and Azure

If you wish to host your app's container images using the Docker Hub, you will need to [set up a Docker Hub account](https://hub.docker.com/signup).
Once you have done so, create a public repository called `todo-app`.

To build and push your production Docker image to the Docker Hub, you will need to run the following commands from your terminal, using the Docker Hub username you created previously:

```bash
$ EXPORT DOCKERHUB_USERNAME=...
$ docker login
$ docker compose build production
$ docker compose push production
```

To set up an Azure account, first ensure you have a Microsoft account, and then visit the [Azure Portal](https://portal.azure.com) and use this Microsoft account to register.
Once you have done this, you will also need to create a subscription - this is achieved by clicking the Subscriptions blade under Azure services and then clicking Add.
Next, within this subscription, create a resource group by choosing the Resource groups blade, again under Azure services, and then clicking Create.
Finally, to log in to your new account locally, run the following command and follow the ensuing steps:

```bash
$ az login
```

To create Azure App Service and Azure CosmosDB resources for your app, you will need to run the following commands from a Bash shell, setting the environment variables to appropriate values:

```bash
$ export RESOURCE_GROUP_NAME=...
$ export APPSERVICE_PLAN_NAME=...
$ export WEBAPP_NAME=...
$ export DOCKERHUB_USERNAME=...
$ export COSMOS_ACCOUNT_NAME=...
$ az appservice plan create -g $RESOURCE_GROUP_NAME -n $APPSERVICE_PLAN_NAME --sku F1 --is-linux
$ az webapp create -g $RESOURCE_GROUP_NAME -p $APPSERVICE_PLAN_NAME -n $WEBAPP_NAME --deployment-container-image-name docker.io/$DOCKERHUB_USERNAME/todo-app:latest
$ az webapp config appsettings set -g $RESOURCE_GROUP_NAME -n $WEBAPP_NAME --settings `cat .env | grep -v '^#' | tr '\n' ' '`
$ az cosmosdb create --name $COSMOS_ACCOUNT_NAME --resource-group $RESOURCE_GROUP_NAME --kind MongoDB --capabilities EnableServerless --server-version 4.2
$ az cosmosdb mongodb database create --account-name $COSMOS_ACCOUNT_NAME --name todo_app --resource-group $RESOURCE_GROUP_NAME
```

Note that you should use the resource group name and Docker Hub username you created previously, but you will need to choose your app service plan name, web app name and CosmosDB account name, with the web app name needing to be globally unique within Azure.

Once you have done this, retrieve the primary connection string for your CosmosDB account by running the following command, ensuring that your environment variables from the previous set of commands are still set:

```bash
$ az cosmosdb keys list --type connection-strings --name $COSMOS_ACCOUNT_NAME --resource-group $RESOURCE_GROUP_NAME
```

Copy the primary connection string into your `.env` file, using it as the value for the `MONGO_URI` setting.

Finally, run the following commands to set environment variables for your app:

```bash
$ export SECRET_KEY=...
$ export MONGO_URI=...
$ az webapp config appsettings set --name $WEBAPP_NAME --resource-group $RESOURCE_GROUP_NAME --settings SECRET_KEY=$SECRET_KEY MONGO_URI=$MONGO_URI
```

You should use the same values for `SECRET_KEY` and `MONGO_URI` that you saved in your `.env` file.

Your deployed web app will be at [https://$WEBAPP_NAME.azurewebsites.net/]() in due course.

To refresh your app when you push a new version of your image to the Docker Hub manually, send a post request to your app's webhook URL, which you can find by looking in the Deployment Center blade of your resource in the Azure portal.
One way of doing this is to install the cURL utility and run the following command, filling in your webhook URL:

```bash
$ curl -f -X POST '...'  # (Single quotation marks important here)
```

## Pipelines

### GitHub Actions

A workflow file called `ci-cd-pipeline.yml` has been set up in order to validate any non-documentation changes upon new pushes or pull requests to the project's GitHub repository.
Upon successful validation of the changes, it is also configured to build and push a Docker image to the Docker Hub, and use this new image as the basis for an Azure web app.
In order to get this working with a fork of the repository, it should be necessary to create the following GitHub Actions secrets:

```dotenv
DOCKERHUB_USERNAME
```

This should be the username you used to create your Docker Hub account.

```dotenv
DOCKERHUB_TOKEN
```

This token should be obtained via the settings page of your Docker Hub account.

```dotenv
AZURE_APP_WEBHOOK_URL
```

This is the webhook URL from the Deployment Center blade of your web app resource in the Azure portal.
