from oauth2client.client import GoogleCredentials
import requests
import json


def make_prediction(new_data):
    """Function for making predictions using our deployed model"""

    MODEL_NAME = "test_model1" 
    MODEL_VERSION = "MLOPS-demo"
    PROJECT = "ml-pipeline-309409"


    token = GoogleCredentials.get_application_default().get_access_token().access_token
    api = 'https://ml.googleapis.com/v1/projects/{}/models/{}/versions/{}:predict'.format(PROJECT, MODEL_NAME, MODEL_VERSION)
    headers = {'Authorization': 'Bearer ' + token }
    new_data = 
    {
        'instances':
        {
            'variable1': new_data[0]
            'variable2': new_data[1]
            'variable3': new_data[2]
        }
    }
    response = requests.post(api,json=data,headers=headers)
    print("Prediction: ",response.content)

if __name__ == "__main__":
    print("You're supposed to make a prediction now!")
    #data = [1,2,3]
    #make_prediction(data)
    