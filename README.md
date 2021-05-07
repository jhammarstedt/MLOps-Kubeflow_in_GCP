# MLOPS CI/CD with Kubeflow Pipelines in Google Cloud (WIP)
This repo will demonstrate how to take the first step towards MLOps by setting up and deploying an ML CI/CD pipeline using Google Clouds AI Platform, Kubeflow and Docker.

This demo was created as a part of an assignment for a DevOps course given at KTH spring 2021 and a video demo will also be added shortly.
## Authors
* Johan Hammarstedt, [jhammarstedt](https://github.com/jhammarstedt)
* Matej Sestak, [Sestys](https://github.com/sestys)

## Overview
The following topics will be covered:
1. Building each task as a docker container and running them with cloud build
   * Preprocessing step: Loading data from GC bucket, editing it and storing a new file
   * Training: Creating a pytorch model and build a custom prediction routine (GCP mainly supporst tensorflow, but you can add custom models)
   * Deployment: Deploying your custom model to the AI Platform with version control
2. Creating a Kubeflow pipeline and connecting the above tasks
3. Perform CI by building Github Triggers in Cloud Build that will rebuild container upon a push to repository
4. CD by using Cloud Functions to trigger upon uploading new data to your bucket

## Setting up the pipeline
Here we will go through the process of running the pipeline step by step:

1. Create a gcp project, open the shell (make sure you're in the project), and fork the repository `$ git clone clone jhammarstedt/gcloud_MLOPS_demo.git`
2. Create a [kubeflow pipeline](https://console.cloud.google.com/ai-platform/pipelines)
3. Run the set_auth.sh script in google cloud shell (might wanna change the SA_NAME), this gives us the roles we need to run the pipeline
4. Create a docker container for each step (each of the folders in the containers repo representes a different step)
       * Do this by running: ```$ gcloud_MLOPS_demo/containers ./build_containers.sh ``` from the cloud shell.

      This will run "build_single_container.sh in each directory"
      * If you wish to try and just build one container, enter the directory which you want to build and run:

        `$ bash ../build_single_container.sh {directory name}`

5. Each subfolder (which will be a container) includes:
     * A cloudbuild.yaml file (created in build_single_repo.sh) which will let Cloud Build create a docker container by running the included Dockerfile.
     * The DockerFile that mainly runs the task script (e.g deploy.sh)
     * A task script that tells the Docker container what to do (e.g preproc/train/deploy the trained model to the AI-platform)
6. To test the container manually run

    `docker run -t gcr.io/{YOUR_PROJECT}/{IMAGE}:latest --project {YOUR_PROJECT} --bucket {YOUR_BUCKET} local`

    e.g to run the container that deploys the model to AI platform I would run:

    `docker run -t gcr.io/ml-pipeline-309409/ml-demo-deploy-toai `

7. Create a pipeline in python using the kubeflow API (currently a notebook in AI platform)
8. Now we can either run the pipeline manually at the pipeline dashbord from 1. or run it as a script.

## CI
To set up CI and rebuild at every PR:
  * Connect gcloud to github, either using setup_trigger.sh or in the [Trigger UI](https://console.cloud.google.com/cloud-build/triggers?project=ml-pipeline-309409&folder=&organizationId=)
  * Push the newly created cloudbuilds from GCP into the origin otherwise the trigger won't find them
  * This trigger will run everytime a push to master happens in any of the containers and thus rebuild the affected Docker Image

## CD
CD can be necessary when we want to retrain/finetune the model give that we get new data, not every time we update a component.
So we will have a Cloud function that will trigger a training pipeline when we upload new data to the Cloud Storage.
1. Get the pipeline host url from pipiline settings (looks like this: https://39ddd8e8124976d-dot-us-central1.pipelines.googleusercontent.com, ideally save it as an PIPELINE_HOST environment variable).
2. in pipeline folder, run the deploy script

`./deploy_cloudfunction $PIPELINE_HOST`

3. Now, whenever a new file is added or deleted from the project bucket, it will rerun the pipeline.

## Resources used and further reading
* [Deploy your own custom model on GCP’s AI platform](https://medium.com/searce/deploy-your-own-custom-model-on-gcps-ai-platform-7e42a5721b43)
* [How to carry out CI/CD in Machine Learning (“MLOps”) using Kubeflow ML pipelines](https://medium.com/google-cloud/how-to-carry-out-ci-cd-in-machine-learning-mlops-using-kubeflow-ml-pipelines-part-3-bdaf68082112)
* [GCP documentation on model deployment](https://cloud.google.com/ai-platform/prediction/docs/deploying-models)
