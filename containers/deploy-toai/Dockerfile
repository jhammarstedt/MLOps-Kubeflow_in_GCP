# Get an already prebuilt gcloud image that will be usefull running gcloud comands
FROM google/cloud-sdk:latest

#Create a subdirectory, enter it and clone our github repo to get the code for the trainer
RUN mkdir -p /demo1/src && cd /demo1/src && git clone https://github.com/jhammarstedt/gcloud_MLOPS_demo.git 

#Copy the deploy script from /containers/$current_container 
COPY test.py ./
COPY predict.py ./

RUN cat test.py

#using bash we run the deploy script we just copied in here
ENTRYPOINT ["python3"," test.py"]

#running our prediction script
RUN python predict.py 
