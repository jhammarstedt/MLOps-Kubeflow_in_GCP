FROM python:3.8

COPY . .

RUN pip install -r requirements.txt
ARG project_id='ml-pipeline-309409'
ARG bucket=''ml-pipeline-309409_bucket'
#using bash we run the deploy script we just copied in here
ENTRYPOINT ["python", "load_data.py --project ${project_id} --bucket ${bucket}"]
