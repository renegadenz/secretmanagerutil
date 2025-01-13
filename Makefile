# Variables
APP_NAME := secrets-manager-ui
DOCKER_IMAGE := $(APP_NAME)
DOCKER_CONTAINER := $(APP_NAME)-container
PORT := 5000
AWS_CONFIG := ~/.aws
AWS_SSO_CACHE := ~/.aws/sso/cache
AWS_REGION := ap-southeast-2  # Set the region here

# Build Docker image
.PHONY: docker-build
docker-build:
	docker build -t $(DOCKER_IMAGE) .

# Run the application in Docker
.PHONY: docker-run
docker-run:
	docker run --name $(DOCKER_CONTAINER) \
		-p $(PORT):$(PORT) \
		-v $(AWS_CONFIG):/root/.aws:ro \
		-v $(AWS_SSO_CACHE):/root/.aws/sso/cache:ro \
		-e AWS_REGION=$(AWS_REGION) \
		-d $(DOCKER_IMAGE)

# Stop and remove the Docker container
.PHONY: docker-stop
docker-stop:
	docker stop $(DOCKER_CONTAINER) || true
	docker rm $(DOCKER_CONTAINER) || true

# Rebuild and run the application
.PHONY: run
run: docker-stop docker-build docker-run
	@echo "Application is running at http://localhost:$(PORT)"
