
import os
import pandas as pd
from google.cloud import storage
import torch
from network import Network

class PyTorchIrisClassifier(object):
    def __init__(self, model):
        self._model = model
        self.class_vocab = ['setosa', 'versicolor', 'virginica']
    
    @classmethod
    def from_path(cls, model_dir):
        model_file = os.path.join(model_dir,'model.pth')
        model = Network()
        model.load_state_dict(torch.load(model_file))
        #model = torch.load(model_file)
        return cls(model)
        
    def predict(self, instances, **kwargs):
        data = pd.DataFrame(instances).to_numpy()
        inputs = torch.Tensor(data)
        outputs = self._model(inputs)
        _ , predicted = torch.max(outputs, 1)
        return [self.class_vocab[class_index] for class_index in predicted]
