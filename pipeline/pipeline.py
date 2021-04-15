import kfp
import os

from kfp.gcp import use_gcp_secret
import kfp.dsl as dsl


@dsl.pipeline(
    name='ml-demo',
)
def test(
        project='ml-demo',
        bucket='ml-pipeline-309409-kubeflowpipelines-default',
):
    train = dsl.ContainerOp(
        name='training',
        # image needs to be a compile-time string
        image='gcr.io/ml-pipeline-309409/ml-demo-train:latest',
        # file_outputs = {'bucket':'models/output.txt'} something like this
    ).apply(use_gcp_secret('user-gcp-sa'))

    test = dsl.ContainerOp(
        name='test',
        # image needs to be a compile-time string
        image='gcr.io/ml-pipeline-309409/ml-demo-deploy-toai:latest',
        # arguments = [train.outputs['bucket']]
        # file_outputs= {} foo foo
    ).apply(use_gcp_secret('user-gcp-sa'))


if __name__ == '__main__':
    PIPELINES_HOST = os.environ['PIPELINE_HOST']
    client = kfp.Client(host=PIPELINES_HOST)
    pipeline = client.create_run_from_pipeline_func(test, {})
