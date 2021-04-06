#!/bin/bash -e
for container in */; do
  cd $container
  echo "Building Docker container in $container"

  cd ..
done
