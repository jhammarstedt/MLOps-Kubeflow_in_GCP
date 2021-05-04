#!/bin/bash

echo "Running traning model.py"
python train_test.py


#This file creates a local package with all our pytorch requirements and then copies it to our bucket
echo "SETTING UP MODEL"
python setup.py sdist
DIST_PACKAGE_BUCKET='gs://ml-pipeline-309409_bucket/models/Test_model-0.1.tar.gz'
LOCAL_PACKAGE='dist/Test_model-0.1.tar.gz'

gsutil cp $LOCAL_PACKAGE $DIST_PACKAGE_BUCKET
#gsutil cp dist/Test_model-0.1.tar.gz gs://ml-pipeline-309409_bucket/models/Test_model-0.1.tar.gz
