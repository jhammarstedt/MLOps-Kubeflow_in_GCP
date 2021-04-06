#!/bin/bash -e
for container in */; do
  cd $container
  ehco "Building Docker container in $container

  cd..
done
