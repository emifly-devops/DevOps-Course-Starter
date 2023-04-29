# DevOps Apprenticeship: Project Exercise

## System Requirements

The project uses Poetry for Python to create an isolated environment and manage package dependencies.
To prepare your system, ensure you have an official distribution of Python version 3.7+ and install Poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

### Poetry Installation (Bash)

```bash
$ curl -sSL https://install.python-poetry.org | python -
```

### Poetry Installation (PowerShell)

```powershell
PS> (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

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

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change).
There are also some Trello secrets that need to be set, which are detailed below.

## Trello

You will need to [set up a Trello account](https://trello.com/signup) and create a new board in order to run this project. Once you have done so, there are three Trello secrets that need to be set in your `.env` file.
Here is how each of these can be obtained:

```dotenv
TRELLO_KEY
```

Your personal Trello app key can be found at the top of the [developer API keys page](https://trello.com/app-key) when signed in.

```dotenv
TRELLO_TOKEN
```

On the same page, just below your personal Trello app key, there is a link to manually generate a token. Follow the steps to obtain a token.

```dotenv
TRELLO_BOARD_ID
```

A suitable board ID can be obtained from the URL of the board you created after signing up.
The URL will be of the form `https://trello.com/b/<board ID>/<board name>`.

For example, if your board URL is `https://trello.com/b/12345678/to-do-board`, your board ID will be `12345678`.

## Running the App with a Development Configuration

Once the all dependencies have been installed, start the Flask app in development mode within the Poetry environment by running:

```bash
$ poetry run flask run
```

Alternatively, if you have chosen to install Node, you can simply run the following command:

```bash
$ npm start
```

If you have chosen to install Docker, you can run the following command instead:

```bash
$ docker compose --file docker-compose.development.yml up development --build
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

You will be prompted to enter your Trello secrets.
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
$ docker compose up cypress --build --abort-on-container-exit
```

In this case, there is no need to manually start the app - Docker will take care of this for us as well as automatically tearing it down when the tests are complete.

## Deployment with Docker and Azure

If you wish to host your app's container images using the Docker Hub, you will need to [set up a Docker Hub account](https://hub.docker.com/signup).
Once you have done so, create a public repository called `todo-app`.
There is also a Docker configuration value that needs to be set in your `.env` file:

```dotenv
DOCKERHUB_USERNAME
```

Enter the username you chose when you signed up to the Docker Hub.

To build and push your production Docker image to the Docker Hub, you will need to run the following commands from your terminal:

```bash
docker login
docker compose build production
docker compose push production
```

It is necessary to do this once before configuring your Azure App Service app (detailed below). However, future pushes will be automated.

To set up an Azure account, first ensure you have a Microsoft account, and then visit the [Azure Portal](https://portal.azure.com) and use this Microsoft account to register.
Once you have done this, you will also need to create a subscription - this is achieved by clicking the Subscriptions blade under Azure services and then clicking Add.
Next, within this subscription, create a resource group by choosing the Resource groups blade, again under Azure services, and then clicking Create.

To create an Azure App Service resource for your app, you will need to run the following commands from a Bash shell, setting the environment variables to appropriate values:

```bash
export RESOURCE_GROUP_NAME=...
export APPSERVICE_PLAN_NAME=...
export WEBAPP_NAME=...
export DOCKERHUB_USERNAME=...
az appservice plan create -g $RESOURCE_GROUP_NAME -n $APPSERVICE_PLAN_NAME --sku F1 --is-linux
az webapp create -g $RESOURCE_GROUP_NAME -p $APPSERVICE_PLAN_NAME -n $WEBAPP_NAME --deployment-container-image-name docker.io/$DOCKERHUB_USERNAME/todo-app:latest
az webapp config appsettings set -g $RESOURCE_GROUP_NAME -n $WEBAPP_NAME --settings `cat .env | grep -v '^#' | tr '\n' ' '`
```

Note that you should use the resource group name and Docker Hub username you created previously, but you will need to choose your app service plan name and web app name, with the latter needing to be globally unique within Azure.

You should be able to view your deployed web app at [https://$WEBAPP_NAME.azurewebsites.net/]().

To refresh your app if you ever push a new version of your image to the Docker Hub manually, send a post request to your app's webhook URL, which you can find by looking in the Deployment Center blade of your resource in the Azure portal.
One way of doing this is to install the cURL utility and run the following command, filling in your webhook URL:

```bash
curl -dH -X POST "..."
```

## Pipelines

### GitHub Actions

A workflow file called `ci-cd-pipeline.yml` has been set up in order to validate any non-documentation changes upon new pushes or pull requests to the project's GitHub repository.
Upon successful validation of the changes, it is also configured to build and push a Docker image to the Docker Hub, and use this new image as the basis for an Azure web app.
In order to get this working with a fork of the repository, it should be necessary to create the following GitHub Actions secrets:

```dotenv
TRELLO_KEY
```

This should be the same as the Trello key that you saved in your `.env` file.

```dotenv
TRELLO_TOKEN
```

This should be the same as the Trello token that you saved in your `.env` file.

```dotenv
TRELLO_BOARD_ID
```

This should be the same as the Trello board ID that you saved in your `.env` file.

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
