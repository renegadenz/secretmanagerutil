# Variables
APP_NAME := secrets-manager-ui
PYTHON := python3
DOCKER_IMAGE := $(APP_NAME)
DOCKER_CONTAINER := $(APP_NAME)-container
PORT := 5000

# Default target
.PHONY: help
help:
	@echo "Available commands:"
	@echo "  make install       Install Python dependencies"
	@echo "  make run           Run the Flask application locally"
	@echo "  make docker-build  Build the Docker image"
	@echo "  make docker-run    Run the application in a Docker container"
	@echo "  make docker-stop   Stop the running Docker container"
	@echo "  make test          Run tests using pytest"
	@echo "  make clean         Clean up temporary files"

# Install Python dependencies
.PHONY: install
install:
	pip install -r requirements.txt

# Run Flask app locally
.PHONY: run
run:
	FLASK_APP=app/app.py FLASK_ENV=development $(PYTHON) -m flask run --host=0.0.0.0 --port=$(PORT)

# Build Docker image
.PHONY: docker-build
docker-build:
	docker build -t $(DOCKER_IMAGE) .

# Run the application in Docker
.PHONY: docker-run
docker-run:
	docker run --name $(DOCKER_CONTAINER) -p $(PORT):$(PORT) -d $(DOCKER_IMAGE)

# Stop the Docker container
.PHONY: docker-stop
docker-stop:
	docker stop $(DOCKER_CONTAINER) || true
	docker rm $(DOCKER_CONTAINER) || true

# Run tests
.PHONY: test
test:
	pytest tests/

# Clean up temporary files
.PHONY: clean
clean:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -exec rm -rf {} +
	rm -rf .pytest_cache
	docker system prune -f

