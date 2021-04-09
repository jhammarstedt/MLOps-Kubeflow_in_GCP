#!bin/bash -e
echo "Current dir $(pwd) "
CONTAINER_NAME= "ml-demo-$(basename $(pwd))" #gets the last folder which is our name
PROJECT_ID= "$(gcloud config config-helper --format "value(configuration.properties.core.project)")"

echo "Creating ${CONTAINER_NAME}:latest from Dockerfile:"
cat ${CONTAINER_NAME}/Dockerfile

#check if the cloudbuild file already exists
#if [-f cloudbuild.yaml];
#      echo "Cloudbuild existed, removing and creating a new"
#      rm cloudbuild.yaml
#fi

#So in each dir we will create a cloudbuild file that tells Cloud Build to run the Dockerfile
cat <<EOM> cloudbuild.yaml
steps:
      - name: 'gcr.io/cloud-builders/docker'  
        # dir: '/containers/$CONTAINER_NAME' #enable this when we run the github triggers
        #Use cloudbuild to build and use -t to exit after running this command
        #path is gcr.io/PROJECT_ID/IMAGE_NAME
        args: ['build','-t','gcr.io/${PROJECT_ID}/${CONTAINER_NAME}:latest','.']
        
        #Create and store an image in the container registry
images: ['gcr.io/${PROJECT_ID}/${CONTAINER_NAME}:latest']
EOM
echo "cloudbuild file created: "
cat cloudbuild.yaml

echo "Build the container using Cloud Build"
gcloud builds submit . --config cloudbuild.yaml
