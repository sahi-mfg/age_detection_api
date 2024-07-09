# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set environment variables
ENV POETRY_VERSION=1.8.3

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Ensure the Poetry binary is in the PATH
ENV PATH="/root/.local/bin:$PATH"

# Set the working directory in the container
WORKDIR /app

# Copy pyproject.toml and poetry.lock files
COPY pyproject.toml poetry.lock /app/

# Install dependencies
RUN poetry install --no-root

# Copy the rest of the application code
COPY . /app


# Run the application.
COPY entrypoint.sh /entrypoint.sh
RUN chmod a+x /entrypoint.sh
CMD ["/entrypoint.sh"]
