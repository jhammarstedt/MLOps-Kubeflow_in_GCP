#!/bin/bash -e
for container in */; do
  cd $container
  echo "Building Docker container in $container"
  # Going into the container and building it with the general build_container.sh script
  bash ../build_single_container.sh $container 
  cd .. #Go back to the root container repository to start building the next one
done
