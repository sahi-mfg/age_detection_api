FROM ubuntu:22.04


WORKDIR /root/app

# Install Python
RUN apt-get -y update && \
    apt-get install -y python3-pip

# Install project dependencies
COPY requirements.txt .
RUN pip3 install -r requirements.txt

CMD ["uvicorn","main:app", "--port","5001", "--host","0.0.0.0"]
