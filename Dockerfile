FROM python:3.10-slim-bullseye AS base

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y curl

ENV POETRY_HOME=/opt/poetry
RUN curl -sSL https://install.python-poetry.org | python -
RUN ln -s $POETRY_HOME/bin/poetry /usr/local/bin/poetry

WORKDIR /opt/todo-app

COPY pyproject.toml poetry.toml poetry.lock ./
RUN poetry install

COPY todo_app todo_app/

# ----- #
FROM base AS production

ENTRYPOINT ["poetry", "run", "gunicorn", "--bind", "0.0.0.0:80", "todo_app.app:create_app()"]
EXPOSE 80

# ----- #
FROM base AS development

ENTRYPOINT ["poetry", "run", "flask", "run", "--host", "0.0.0.0"]
EXPOSE 5000

# ----- #
FROM base AS test

COPY tests tests/

ENTRYPOINT ["poetry", "run", "pytest"]
