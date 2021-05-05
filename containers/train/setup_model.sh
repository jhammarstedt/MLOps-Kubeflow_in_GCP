#!/bin/bash

echo "Running traning model.py"
python train_test.py
echo "Saving the model.pth to bucket: models/model.pth"

LOCAL_MODELPATH='models/model.pth'
BUCKET_MODELPATH='gs://ml-pipeline-309409_bucket/models/model.pth'


gsutil cp $LOCAL_MODELPATH $BUCKET_MODELPATH

#This file creates a local package with all our pytorch requirements and then copies it to our bucket
echo "SETTING UP MODEL"

python models/setup.py sdist

ls

DIST_PACKAGE_BUCKET='gs://ml-pipeline-309409_bucket/models/Test_model-0.1.tar.gz'
LOCAL_PACKAGE='dist/Test_model-0.1.tar.gz'

gsutil cp $LOCAL_PACKAGE $DIST_PACKAGE_BUCKET
echo "cleaning up temp files in container"
rm -r Test_model.egg-info
rm -rf dist/
rm -r models/model.pth
#gsutil cp dist/Test_model-0.1.tar.gz gs://ml-pipeline-309409_bucket/models/Test_model-0.1.tar.gz
