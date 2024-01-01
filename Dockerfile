FROM ubuntu:22.04


WORKDIR /app

# Install Python
RUN apt-get -y update && \
    apt-get install -y python3-pip

# Install project dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . /app/

CMD ["uvicorn","main:app", "--port","5001", "--host","0.0.0.0"]
