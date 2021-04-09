# Demo on MLOPS with google cloud (WIP)
This demo was created as a part of an assignment for a DevOps course given at KTH spring 2021
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
4. Each subfolder (which will be a container should include)
  * A cloudbuild.yaml file which will tell Cloud Build to create a dockercontainer by running the included dockerfile (No need to create- will be regenerated at each run)
  * A DockerFile that mainly creates a subdirectory and runs the task script (e.g deploy.sh)
  * A task script that tells the Docker container what to do (e.g deploy the trained model to the AI-platform)
5. To test the container manually run

`docker run -t gcr.io/{YOUR_PROJECT}/{IMAGE}:latest --project {YOUR_PROJECT} --bucket {YOUR_BUCKET} local`

to run the container that deploys the model to AI platform I would run:

`docker run -t gcr.io/ml-pipeline-309409/deploytoai:latest --project ml-pipeline-309409 --bucket ml-pipeline-309409_cloudbuild local`

6. Create a pipeline in python using the kubeflow API
7. Now we can either run the pipeline manually at the pipeline dashbord from 1. or run it as a script.
### CI
8. To set up CI and rebuild at every PR:
  * Connect gcloud to github, either using setup_trigger.sh or in the [Trigger UI](https://console.cloud.google.com/cloud-build/triggers?project=ml-pipeline-309409&folder=&organizationId=)
  * This trigger will run everytime a PR happens and thus rebuild the affected Docker Image
### CD (TBD)
CD can be necessary when we want to retrain/finetune the model give that we get new data, not every time we update a component. 
So we will have a Cloud function that will trigger a training pipeline when we upload new data to the Cloud Storage (in AWS this would be a lambda connected to the S3 storage)
