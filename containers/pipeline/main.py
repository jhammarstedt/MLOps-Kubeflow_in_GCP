import kfp
import os
from kfp.gcp import use_gcp_secret
import kfp.dsl as dsl
import argparse


@dsl.pipeline(
    name='ml-demo',
)
def preprocess_train_deploy(
        project='ml-pipeline-309409',
        bucket='ml-pipeline-309409_bucket',
):
    # 1 load data
    data = dsl.ContainerOp(
        name='preprocess',
        # image needs to be a compile-time string
        image='gcr.io/ml-pipeline-309409/ml-demo-data:latest',
        arguments=[
            '--project', project,
            '--mode', 'cloud',
            '--bucket', bucket,
          ],
        file_outputs = {'bucket':'/output.txt'}
    ).apply(use_gcp_secret('user-gcp-sa'))
    data.container.set_image_pull_policy('Always')


    # 2 train
    train = dsl.ContainerOp(
      name='train',
      # image needs to be a compile-time string
      image='gcr.io/ml-pipeline-309409/ml-demo-train:latest',
      arguments=[
        data.outputs['bucket']
      ],
      file_outputs={'model': '/modelOutput.txt'}
    ).apply(use_gcp_secret('user-gcp-sa'))
    train.container.set_image_pull_policy('Always')


    # 3 deploy the trained model to Cloud ML Engine
    deploymodel = dsl.ContainerOp(
      name='deploymodel',
      # image needs to be a compile-time string
      image='gcr.io/ml-pipeline-309409/ml-demo-deploy-toai:latest',
      arguments=[
        train.outputs['model'],
      ],
      file_outputs={
        'model': '/model.txt',
        'version': '/version.txt'
      }
    ).apply(use_gcp_secret('user-gcp-sa'))
    deploymodel.execution_options.caching_strategy.max_cache_staleness = "P0D"
    deploymodel.container.set_image_pull_policy('Always')


def handle_newfile(data, context):
    PIPELINES_HOST = os.environ.get('PIPELINES_HOST', "Environment variable PIPELINES_HOST not set")
    PROJECT = os.environ.get('PROJECT', "Environment variable PROJECT not set")
    BUCKET = os.environ.get('BUCKET', "Environment variable BUCKET not set")
    client = kfp.Client(host=PIPELINES_HOST)
    client.create_run_from_pipeline_func(preprocess_train_deploy, {'project': PROJECT, 'bucket': BUCKET})
