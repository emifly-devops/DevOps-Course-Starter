# DevOps Apprenticeship: Project Exercise

## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies.
To prepare your system, ensure you have an official distribution of Python version 3.7+ and install Poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

### Poetry installation (Bash)

```bash
$ curl -sSL https://install.python-poetry.org | python -
```

### Poetry installation (PowerShell)

```powershell
PS> (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

If you wish to run the end-to-end tests associated with the app, you will also need to have Node installed - follow the [installation steps on the website](https://nodejs.org/).
It should come with the package manager NPM, which is also required.

Another optional installation is Vagrant, for which a production configuration has been provided if you want to run the app in a virtual machine.
Again, follow the [installation steps on the website](https://www.vagrantup.com) if this is of interest.
You will need a hypervisor available if you choose to take this route. If in doubt, [VirtualBox](https://www.virtualbox.org) is a good option.

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
There are also some Trello variables that need to be set, which are detailed below.

## Trello

You will need to [set up a Trello account](https://trello.com/signup) and create a new board in order to run this project. Once you have done so, there are three Trello variables that need to be set in your `.env` file.
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

## Running the App

Once the all dependencies have been installed, start the Flask app in development mode within the Poetry environment by running:

```bash
$ poetry run flask run
```

Alternatively, if you have chosen to install Node, you can simply run the following command:

```bash
$ npm start
```

As another alternative, if you have chosen to install Vagrant, you can run the following:

```bash
$ vagrant up
```

In each case, visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

## Running the Tests

Use the following command to run the unit and integration tests associated with the app:

```bash
$ poetry run pytest
```

Alternatively, if you have chosen to install Node, you may run the following instead:

```bash
$ npm run test:pytest
```

This project uses Cypress for some basic end-to-end testing. To run these tests, you will need to first start the app, and then use the following command:

```bash
$ npm run test:cypress
```
