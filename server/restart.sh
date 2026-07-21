#!/bin/bash

set -e

CONTAINER_NAME="image-server"

echo "Stopping ${CONTAINER_NAME}..."
docker stop "${CONTAINER_NAME}" 2>/dev/null || true

echo "Removing ${CONTAINER_NAME}..."
docker rm "${CONTAINER_NAME}" 2>/dev/null || true

echo "Building image..."
docker compose build image-server

echo "Starting ${CONTAINER_NAME}..."
docker compose up -d image-server

echo
echo "Container status:"
docker ps --filter "name=${CONTAINER_NAME}"

echo
echo "Last logs:"
docker logs --tail 30 "${CONTAINER_NAME}"