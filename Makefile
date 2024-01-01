# Variables
IMAGE_NAME = age-detection-api
CONTAINER_NAME = age-detection-api-container
PORT = 5001

# Targets
.PHONY: build run stop clean

build:
	docker build -t $(IMAGE_NAME) .

run:
	docker run -d -p $(PORT):$(PORT) --name $(CONTAINER_NAME) $(IMAGE_NAME)

stop:
	docker stop $(CONTAINER_NAME) && docker rm $(CONTAINER_NAME)

clean: stop
	docker rmi $(IMAGE_NAME)

test:
	pip3 install -r requirements.txt
	python3 -m pytest -v




