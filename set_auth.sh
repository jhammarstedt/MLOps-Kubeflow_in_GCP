#!/bin/bash


if [ "$#" -ne 3 ]; then
    echo "Usage: ./set_auth.sh service-account-name zone cluster namespace"
    echo "     Create a new name and get the other values at https://console.cloud.google.com/ai-platform/pipelines/clusters"
    echo "  eg:  ./set_auth.sh ml-demo europe-north1-c cluster-1 default"
    exit
fi

PROJECT_ID=$(gcloud config config-helper --format "value(configuration.properties.core.project)")
SA_NAME=$1 
ZONE=$2
CLUSTER=$3
NAMESPACE="default"



gcloud container clusters get-credentials "$CLUSTER" --zone "$ZONE" --project "$PROJECT_ID"

#create the service account
gcloud iam service-accounts create $SA_NAME \
       --display-name $SA_NAME --project "$PROJECT_ID"

# Grant permissions to the service account by binding roles
# roles/editor is needed to launch a CAIP Notebook.
# The others (storage, bigquery, ml, dataflow) are pretty common for GCP ML pipelines
for ROLE in roles/editor roles/storage.admin roles/bigquery.admin roles/ml.admin roles/dataflow.admin roles/pubsub.admin; do
  gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member=serviceAccount:$SA_NAME@$PROJECT_ID.iam.gserviceaccount.com \
    --role=$ROLE
done

# Create credential for the service account
gcloud iam service-accounts keys create application_default_credentials.json --iam-account $SA_NAME@$PROJECT_ID.iam.gserviceaccount.com

# Attempt to create a k8s secret. If already exists, override.
kubectl create secret generic user-gcp-sa \
  --from-file=user-gcp-sa.json=application_default_credentials.json \
  -n $NAMESPACE --dry-run -o yaml  |  kubectl apply -f -
  
# remove private key file
rm application_default_credentials.json

#Create a txt file with some info about the project to be used as reference
cat <<EOM > project_info.txt
PROJECT_ID=$PROJECT_ID
SA_NAME=$SA_NAME
SA_ADRESS="$SA_NAME@ai-analytics-solutions.iam.gserviceaccount.com"
ZONE=$ZONE
CLUSTER=$CLUSTER
NAMESPACE=default
EOM
