#!/bin/bash

CONTAINER_NAME="minio-container"

docker run \
    -p 9000:9000 \
    -p 9001:9001 \
    -e "MINIO_ROOT_USER=AKIAIOSFODNN7EXAMPLE" \
    -e "MINIO_ROOT_PASSWORD=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY" \
    quay.io/minio/minio server /data --console-address ":9001" \
    --name "${CONTAINER_NAME}"

sleep 10 # Wait for queue to start
docker logs "${CONTAINER_NAME}"

python "$(git rev-parse --show-toplevel)/test/minio_engine/test.py"

sleep 10

# Stop container
docker stop "${CONTAINER_NAME}"
# and delete it
docker rm "${CONTAINER_NAME}"