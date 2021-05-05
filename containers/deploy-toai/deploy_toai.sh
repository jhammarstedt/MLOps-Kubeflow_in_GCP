#!/bin/bash
#THIS SCRIPT WILL DEPLOY OUR MODEL TO AI PLATFORM


# Creating a version resrouce
# origin: Path to GCS directory where the model file is stored.
# python-version: The python version your code is running onto.
# runtime-version: AI platform runtime version.
# machine-type: Machine type is defined as per the requirement of resources for the model to be deployed.
#    Since we are using our own custom prediction routine, there are two machine types available, 
#    Mls1-c4-m4, mls1-c4-m2.
# package-uris: Used for the installation of packages.
# prediction-class: Used to provide custom prediction class names.

MODEL_NAME='test_iris'
MODEL_VERSION='v1'
RUNTIME_VERSION='1.15'
MODEL_CLASS='model.PyTorchIrisClassifier'
PYTORCH_PACKAGE='gs://ml-pipeline-309409_bucket/packages/torch-1.8.1+cpu-cp37-cp37m-linux_x86_64.whl'
DIST_PACKAGE='gs://ml-pipeline-309409_bucket/models/Test_model-0.1.tar.gz'
BUCKET_NAME='ml-pipeline-309409_bucket'
GCS_MODEL_DIR='models/'

# Creating model on AI platform
gcloud alpha ai-platform models create $MODEL_NAME — regions europe-west1 — enable-logging — enable-console-logging

gcloud beta ai-platform versions create {MODEL_VERSION} --model={MODEL_NAME} \
    --origin=gs://${BUCKET_NAME}/${GCS_MODEL_DIR} \
    --python-version=3.7 \
    --runtime-version=${RUNTIME_VERSION} \
    --machine-type=mls1-c4-m4 \
    --package-uris=${DIST_PACKAGE},${PYTORCH_PACKAGE} \
    --prediction-class=${MODEL_CLASS}
