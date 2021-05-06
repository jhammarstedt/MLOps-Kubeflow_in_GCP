print("Training model!")

""" ideally we would want to run a training job here, but this is just to get the pipeline working
https://cloud.google.com/ai-platform/training/docs/getting-started-pytorch

"""
import os
import torch
from sklearn.model_selection import train_test_split
from torch import nn
from torch.utils.data import DataLoader, Dataset
from torchvision import datasets, transforms
import pandas as pd
from torch.optim import Adam
import tqdm
from sklearn.preprocessing import LabelEncoder
from torch.autograd import Variable
import numpy as np

class AnyDataset(Dataset):
    def __init__(self,csvpath, mode = 'train'):
        self.mode = mode
        df = pd.read_csv(csvpath,delimiter=',')
        
        self.le = LabelEncoder() 
        df['class'] = self.le.fit_transform(df['class'])
        
        
        self.num_classes = len(df['class'].unique())
        self.num_features = len(df.columns)-1
        self.num_samples = df.shape[0]
        if self.mode == 'train':
            df = df.dropna()
            self.inp = df.iloc[:,:-1].values
            self.oup = df.iloc[:,-1].values.reshape(-1, 1)
        else:
            self.inp = df.values
    def __len__(self):
        return len(self.inp)
    def __getitem__(self, idx):
        return torch.Tensor(self.inp[idx]), torch.Tensor(self.oup[idx])

class Network(nn.Module):
    def __init__(self,input_features,hidden_units,num_classes):
        super(Network,self).__init__()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(input_features, hidden_units),
            nn.ReLU(),
            nn.Linear(hidden_units, hidden_units),
            nn.ReLU(),
            nn.Linear(hidden_units, num_classes),
            nn.Softmax(dim=1)
            )
        
        
    def forward(self,x):
        out = self.linear_relu_stack(x)
        return out


def train_network(data,net):

    loss_fn = torch.nn.CrossEntropyLoss()
    optimizer = Adam(net.parameters(),lr=0.001)

    train_data = DataLoader(dataset=data, batch_size=32)
    EPOCHS  = 20

    loss_list     = np.zeros((EPOCHS,))
    accuracy_list = np.zeros((EPOCHS,))

    for epoch in tqdm.trange(EPOCHS):
        loss_ep = []
        for x_batch, y_batch in train_data:
            # Zero gradients
            optimizer.zero_grad()
            
            y_pred = net(x_batch)
            y_batch = y_batch.reshape(-1,).long()
            loss = loss_fn(y_pred, y_batch)
            loss_ep.append(loss)
            loss_list[epoch] = loss.item()

            loss.backward()
            optimizer.step()
        print(sum(loss_ep) / len(loss_ep))
    return net


if __name__=='__main__':
    print('read data from data bucket')
    data = AnyDataset("gs://ml-pipeline-309409_bucket/data/iris.data")
    device = 'cpu'

    hidden = 50
    network = Network(input_features= data.num_features,
                hidden_units = hidden,
                num_classes = data.num_classes)
    print(network)
    trained_network = train_network(data,net=network)
    print('Saving models to models/model.pt')
    torch.save(trained_network,'models/model.pt') #saving the model locally to then upload it to bucket
    print('model saved')
