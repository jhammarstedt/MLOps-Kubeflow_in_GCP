#!/bin/bash
TFVERSION=1.8 #specify later
REGION=europe-west1

PROJECT_ID=$(gcloud config config-helper --format "value(configuration.properties.core.project)")
MODEL_NAME="test_model1"
MODEL_VERSION=1
MODEL_DIR=$(gsutil ls gs://ml-pipeline-309409_cloudbuild/models)
#create new model
echo "Setting region to global"
#gcloud config set compute/region global
# Get the name from 
modelname=$(gcloud ai-platform models list --region global| grep -w "$MODEL_NAME") #might give me trouble
echo $modelname

#check if the string is empty, if so we create a new model
if [-z "$modelname"]; then
	echo "Creating model $MODEL_NAME"
	
	gcloud ai-platform models create ${MODEL_NAME} --regions $REGION
else
	echo "The model $MODEL_NAME already exists"
fi

echo "Create version $MODEL_VERSION from $MODEL_DIR"
gcloud ai-platform versions create ${MODEL_VERSION}\
	--model ${MODEL_NAME} --origin ${MODEL_DIR}\
	--runtime-version $TFVERSION
echo $MODEL_NAME >/model.txt
echo $MODEL_VERSION > /version.txt
