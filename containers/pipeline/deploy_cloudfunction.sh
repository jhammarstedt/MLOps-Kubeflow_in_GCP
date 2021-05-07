#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: ./deploy_cloudfunction.sh pipelines_host"
    echo "  eg:  ./deploy_cloudfunction.sh 447cdd24f70c9541-dot-us-central1.notebooks.googleusercontent.com"
    exit
fi


PROJECT=$(gcloud config get-value project)
BUCKET="${PROJECT}-data-bucket"
REGION=us-central1
PIPELINES_HOST=$1

# The function must exist in the main.py file
gcloud functions deploy handle_newfile --runtime python37 \
 --set-env-vars PROJECT=${PROJECT},BUCKET=${BUCKET},PIPELINES_HOST=${PIPELINES_HOST} \
 --trigger-resource="${BUCKET}"  \
 --trigger-event=google.storage.object.finalize
