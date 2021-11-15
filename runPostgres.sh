#!/bin/bash

CONTAINER_NAME=postgres
docker run -d \
    -p 5432:5432 \
    --name ${CONTAINER_NAME} \
    --env-file $PWD/$CONTAINER_NAME}/${CONTAINER_NAME}.env/
    -v $PWD/${CONTAINER_NAME}/data:/var/lib/postgresql/data \
    postgres
