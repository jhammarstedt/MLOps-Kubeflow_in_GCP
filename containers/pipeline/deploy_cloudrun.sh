#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Usage: ./1_deploy_cloudrun.sh pipelines_host"
    echo "  eg:  ./1_deploy_cloudrun.sh 447cdd24f70c9541-dot-us-central1.notebooks.googleusercontent.com"
    exit
fi


PROJECT=$(gcloud config get-value project)
BUCKET="${PROJECT}_bucket"
REGION=us-central1
PIPELINES_HOST=$1

# build the container for Cloud Run
../build_container.sh

# deploy Cloud Run
gcloud run deploy kfpdemo \
   --platform=managed --region=${REGION} \
   --image gcr.io/${PROJECT}/babyweight-pipeline-pipeline \
   --set-env-vars PROJECT=${PROJECT},BUCKET=${BUCKET},PIPELINES_HOST=${PIPELINES_HOST}
