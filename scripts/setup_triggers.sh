#!/bin/bash -e
# Continuous integration: recreate image anytime any file
# in the directory that this script is run from is commited into GitHub using Cloud Build triggers
# Run this only once per directory
# In order to try this out, fork this repo into your personal GitHub account
# Then, change the repo-owner to be your GitHub id

REPO_NAME=gcloud_MLOPS_demo
REPO_OWNER=jhammarstedt

#for trigger_name in trigger-000 trigger-001 trigger-002 trigger-003; do
#  gcloud beta builds triggers delete --quiet $trigger_name
#done

#Here a trigger is created
create_github_trigger() {
	
	DIR_IN_REPO=$(pwd | sed "s%${REPO_NAME}/% %g" | awk '{print $2}')

	#Create a github trigger from gcloud
	gcloud beta builds triggers create github --build-config="${DIR_IN_REPO}/cloudbuild.yaml" \
      		--included-files="${DIR_IN_REPO}/**" --branch-pattern="^master$" --repo-name=${REPO_NAME} --repo-owner=${REPO_OWNER} 
}
cd containers/
for container in $(ls -d */| sed 's%/%%g');do
    cd $container
    echo "Container $container"
    create_github_trigger  
    cd ..
done
cd ..