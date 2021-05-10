import argparse
import datetime
import logging
import os
import mnist
import pandas as pd
from io import StringIO #to avoid creating temp csv file

from google.cloud import storage

# credentials_dict = {
#     'type': 'service_account',
#     'client_id': os.environ['BACKUP_CLIENT_ID'],
#     'client_email': os.environ['BACKUP_CLIENT_EMAIL'],
#     'private_key_id': os.environ['BACKUP_PRIVATE_KEY_ID'],
#     'private_key': os.environ['BACKUP_PRIVATE_KEY'],
# }

def preprocess(PROJECT, BUCKET):
    
    OUTPUT_DIR = 'gs://{0}/data/'.format(BUCKET)

    storage_client = storage.Client(project=PROJECT)

    buckets = storage_client.list_buckets()
    # blob = bucket.blob('/mnist/')
    my_bucket = storage_client.get_bucket("${PROJECT}_bucket")
    
    print("loading data from data bucket")
    data = pd.read_csv("gs://${PROJECT}-data-bucket/iris.data",delimiter=',')
    print(buckets)
    
    print('preprocessing data')
    data['class'] = data['class'].str.lower()
    print(data.head())

    filename= 'iris_preproc.csv'
    
    data.to_csv(filename,index=False)
    blob = my_bucket.blob(f'data/{filename}')
    print("Saving preproc data to project bucket")
    blob.upload_from_filename(filename,content_type='csv')
    os.system("rm iris_preproc.csv")
    with open("/output.txt", "w") as output_file:
        output_file.write(BUCKET)
        print("Done")
        

if __name__ == '__main__':
  logging.getLogger().setLevel(logging.INFO)
  parser = argparse.ArgumentParser()
  parser.add_argument('--project',
                      type=str,
                      required=True,
                      help='The GCP project to run the dataflow job.')
  parser.add_argument('--bucket',
                      type=str,
                      required=True,
                      help='Bucket to store outputs.')
  parser.add_argument('--mode',
                      choices=['local', 'cloud'],
                      help='whether to run the job locally or in Cloud Dataflow.')

  args = parser.parse_args()

  preprocess(args.project, args.bucket)
