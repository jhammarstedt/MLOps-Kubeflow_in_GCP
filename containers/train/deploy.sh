#!/bin/bash
TFVERSION=1.8
REGION="europe-west1"

MODEL_NAME="test_model1"
MODEL_VERSION=1
MODEL_DIR= "projects/ml-pipeline-309409/models/"
#create new model
# Get the name from 
modelname= $(gcloud ai-platform models list | grep -w "$MODEL_NAME") #might give me trouble
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
