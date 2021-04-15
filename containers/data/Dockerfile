FROM python:3.8

COPY . .

RUN pip install -r requirements.txt

#using bash we run the deploy script we just copied in here
ENTRYPOINT ["python", "load_data.py"]