# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/engine/reference/builder/

ARG PYTHON_VERSION=3.12.4
FROM python:${PYTHON_VERSION}-slim as base

ARG AGE_DETECT

ENV AGE_DETECT_ENV=${AGE_DETECT} \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # Poetry's configuration:
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    POETRY_HOME='/usr/local' \
    POETRY_VERSION=1.7.1

# System deps:
RUN curl -sSL https://install.python-poetry.org | python3 -


WORKDIR /app
COPY poetry.lock pyproject.toml /app/

# Project initialization:
RUN poetry install $(test "$AGE_DETECT_ENV" == pre-production && echo "--only=main") --no-interaction --no-ansi


# Copy the source code into the container.
COPY ./app ./app

# Expose the port that the application listens on.
EXPOSE 8000

ENV PORT 8000

# Run the application.
COPY entrypoint.sh /entrypoint.sh
RUN chmod a+x /entrypoint.sh
CMD ["/entrypoint.sh"]
