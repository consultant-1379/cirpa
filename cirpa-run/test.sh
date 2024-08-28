#!/bin/bash
set -e
docker build -t "$USER/cirpa" -f Dockerfile.test . &> /dev/null
docker run --rm -it "$USER/cirpa" "$@"
