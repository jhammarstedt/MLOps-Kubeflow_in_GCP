FROM python:3.8

RUN git clone https://github.com/jhammarstedt/gcloud_MLOPS_demo.git 

COPY gcloud_MLOPS_demo/data/load_data.py .
COPY gcloud_MLOPS_demo/data/requirements .

RUN pip install -r requirements.txt
ARG project_id='ml-pipeline-309409'
ARG bucket='ml-pipeline-309409_bucket'
#using bash we run the deploy script we just copied in here
ENTRYPOINT ["python", "load_data.py --project ml-pipeline-309409 --bucket ml-pipeline-309409_bucket"]
