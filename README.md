# Demo on MLOPS with google cloud (WIP)
This repo will demonstrate how to take the first step towards MLOps by setting up and deploying an ML CI/CD pipeline using Google Clouds AI Platform, Kubeflow and Docker.

This demo was created as a part of an assignment for a DevOps course given at KTH spring 2021 and a video demo will also be added shortly.
## Members
* Johan Hammarstedt, [jhammarstedt](https://github.com/jhammarstedt)
* Matej Sestak, [Sestys](https://github.com/sestys)

## Steps to set up the pipeline CI/CD workflow
### Initial steps to set up a pipeline
1. Create a [kubeflow pipeline](https://console.cloud.google.com/ai-platform/pipelines/clusters?project=ml-pipeline-309409)
2. Run the set_auth.sh script in google cloud shell (might wanna change the SA_NAME), this gives us the roles we need to run the pipeline
3. Create a docker container for each step (each of the folders in the containers repo representes a different step)
 * Do this by running:
 `gcloud_MLOPS_demo/containers ./build_containers.sh `
 This will run "build_single_container.sh in each directory"
4. Each subfolder (which will be a container will include)
  * A cloudbuild.yaml file (created in build_single_repo.sh) which will let Cloud Build create a docker container by running the included Dockerfile.
  * The DockerFile that mainly runs the task script (e.g deploy.sh)
  * A task script that tells the Docker container what to do (e.g deploy the trained model to the AI-platform)
5. To test the container manually run

`docker run -t gcr.io/{YOUR_PROJECT}/{IMAGE}:latest --project {YOUR_PROJECT} --bucket {YOUR_BUCKET} local`

e.g to run the container that deploys the model to AI platform I would run:

`docker run -t gcr.io/ml-pipeline-309409/ml-demo-deploy-toai `

6. Create a pipeline in python using the kubeflow API (currently a notebook in AI platform)
7. Now we can either run the pipeline manually at the pipeline dashbord from 1. or run it as a script.
### CI (To be added) ##
8. To set up CI and rebuild at every PR:
  * Connect gcloud to github, either using setup_trigger.sh or in the [Trigger UI](https://console.cloud.google.com/cloud-build/triggers?project=ml-pipeline-309409&folder=&organizationId=)
  * Push the newly created cloudbuilds from GCP into the origin otherwise the trigger won't find them
  * This trigger will run everytime a push to master happens in any of the containers and thus rebuild the affected Docker Image
### CD (To be added) ##
CD can be necessary when we want to retrain/finetune the model give that we get new data, not every time we update a component. 
So we will have a Cloud function that will trigger a training pipeline when we upload new data to the Cloud Storage (in AWS this would be a lambda connected to the S3 storage)

### Planned Pipeline structure 
1. Preproc
2. Training
3. Deploy to AI platform
4. Serving
