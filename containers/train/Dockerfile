# Get an already prebuilt gcloud image that will be usefull running gcloud comands
FROM gcr.io/deeplearning-platform-release/pytorch-cpu:latest

#Create a subdirectory, enter it and clone our github repo to get the code for the trainer
RUN git clone https://github.com/jhammarstedt/gcloud_MLOPS_demo.git 

#Copy the deploy script from /containers/$current_container 
COPY containers/train/train_test.py ./
COPY containers/train/models/ ./
COPY containers/train/setup_model.sh ./
COPY containers/train/requirements.txt ./


#using bash we run the deploy script we just copied in here
ENTRYPOINT ["python","./train_test.py"]