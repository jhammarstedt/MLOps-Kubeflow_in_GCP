#! /bin/bash
#Getting the project id 
echo "Enter project id: "
read PROJECT_ID 

gcloud config set project $PROJECT_ID

#ENABLE SERVICES
gcloud services enable \
compute.googleapis.com \
container.googleapis.com \
cloudbuild.googleapis.com

#entering our lab workspace
cd
mkdir lab-workspace
cd lab-workspace

#Requirements
Echo "Create requirements file with the following components:"
cat > requirements.txt << EOF
pandas<1.0.0
click==7.0
tfx==0.21.4
kfp==0.5.1
EOF

cat requirements.txt
#####################

echo "Creating dockerfile"
cat > Dockerfile << EOF
FROM gcr.io/deeplearning-platform-release/base-cpu:m42
RUN apt-get update -y && apt-get -y install kubectl
RUN curl -Lo skaffold https://storage.googleapis.com/skaffold/releases/latest/skaffold-linux-amd64 \
&& chmod +x skaffold \
&& mv skaffold /usr/local/bin
COPY requirements.txt .
RUN python -m pip install -U -r requirements.txt --ignore-installed PyYAML==5.3.1
EOF
####################
echo "Enter Image name: "
read IMAGE_NAME
TAG="latest"
IMAGE_URI="gcr.io/${PROJECT_ID}/${IMAGE_NAME}:${TAG}"
echo "#### STARTING CLOUD BUILD #####"
gcloud builds submit --timeout 15m --tag ${IMAGE_URI} .

####################

echo "Setting up AI Platform notebook instance"
ZONE="europe-west4-a"

echo "Enter instance name: "
read INSTANCE_NAME

IMAGE_FAMILY="common-container"
IMAGE_PROJECT="deeplearning-platform-release"
INSTANCE_TYPE="n1-standard-4"
METADATA="proxy-mode=service_account,container=$IMAGE_URI"

gcloud compute instances create $INSTANCE_NAME\
    --zone=$ZONE \
    --image-family=$IMAGE_FAMILY \
    --machine-type=$INSTANCE_TYPE \
    --image-project=$IMAGE_PROJECT \
    --maintenance-policy=TERMINATE \
    --boot-disk-device-name=${INSTANCE_NAME}-disk \
    --boot-disk-size=100GB \
    --boot-disk-type=pd-ssd \
    --scopes=cloud-platform,userinfo-email \
    --metadata=$METADATA






sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 8B57C5C2836F4BEB
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys FEEA9169307EA071
gcloud builds submit --timeout 15m --tag gcr.io/ml-pipeline-309409/mlops-dev:latest