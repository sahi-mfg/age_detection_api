# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Install uv
RUN pip install uv

# Set the working directory in the container
WORKDIR /app

# Copy requirements files
COPY requirements.txt requirements-dev.txt requirements-test.txt /app/

# Install dependencies
RUN uv pip install -r requirements.txt -r requirements-dev.txt -r requirements-test.txt

# Copy the rest of the application code
COPY . /app

# Expose the port the app runs on
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
