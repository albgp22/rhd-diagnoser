#!/bin/bash

conda activate Rabbit

CONTAINER_NAME="some-rabbit"

# Run a mock rabbitmq queue
docker run -d --rm --hostname my-rabbit --name "${CONTAINER_NAME}" -p 15672:15672 -p 5672:5672 rabbitmq:3-management

sleep 10 # Wait for queue to start
docker logs "${CONTAINER_NAME}"

python "$(git rev-parse --show-toplevel)/test/queue_engine/send.py" &
python "$(git rev-parse --show-toplevel)/test/queue_engine/rcv.py"

sleep 10

# Stop container
docker stop "${CONTAINER_NAME}"
# and delete it
docker rm "${CONTAINER_NAME}"