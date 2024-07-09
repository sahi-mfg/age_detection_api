# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/engine/reference/builder/

ARG PYTHON_VERSION=3.11.4
FROM python:${PYTHON_VERSION}-slim as base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copy the requirements.txt file into the container.
COPY requirements.txt .

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
RUN python -m pip install --no-cache-dir -r requirements.txt && python -m pip install -r requirements-test.txt

USER root
# Copy the source code into the container.
COPY ./app ./app

# Expose the port that the application listens on.
EXPOSE 8000

ENV PORT 8000

# Run the application.
COPY entrypoint.sh /entrypoint.sh
RUN chmod a+x /entrypoint.sh
CMD ["/entrypoint.sh"]
