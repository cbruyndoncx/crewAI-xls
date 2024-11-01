############################## DOCKER ######################################
# Default Variables
IMAGE_NAME ?= crew-ai-xls
CONTAINER_NAME ?= crew-ai-xls-cntnr
PORT ?= 8000

# Build the Docker image
build:
	docker build -t $(IMAGE_NAME) .

# Run the Docker container
run:
	@if [ "$$(docker ps -q -f name=$(CONTAINER_NAME))" ]; then \
		echo "Stop and remove running container $(CONTAINER_NAME)..."; \
		docker stop $(CONTAINER_NAME); \
		docker rm $(CONTAINER_NAME); \
	fi
	docker run -d --name $(CONTAINER_NAME) -p $(PORT):$(PORT) $(IMAGE_NAME)

# Stop the Docker container
stop:
	docker stop $(CONTAINER_NAME)

# Remove the Docker container
rm:
	docker rm $(CONTAINER_NAME)

# View logs from the running container
logs:
	docker logs -f $(CONTAINER_NAME)

# Rebuild and run the Docker container
rerun: stop rm build run

# Clean up all unused images and containers
clean:
	docker system prune -f

################################### DEVELOPER DEBUG ##################################
CONDA_NAME ?= mypi310
conda:
	conda activate $(CONDA_NAME)
pyrun:
	python -m uvicorn main:app --reload
reqs:
	pipreqs --ignore templates .

