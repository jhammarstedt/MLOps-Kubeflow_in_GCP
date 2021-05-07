print("Training model!")

""" ideally we would want to run a training job here, but this is just to get the pipeline working
https://cloud.google.com/ai-platform/training/docs/getting-started-pytorch

"""
import os
import torch
import argparse
import configparser
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

from models.network import Network

CONFIG = configparser.ConfigParser()
CONFIG.read("models/config.txt")

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

# class Network(nn.Module):
#     def __init__(self,input_features=4,hidden_units=50,num_classes=3):
#         super(Network,self).__init__()
#         self.linear_relu_stack = nn.Sequential(
#             nn.Linear(input_features, hidden_units),
#             nn.ReLU(),
#             nn.Linear(hidden_units, hidden_units),
#             nn.ReLU(),
#             nn.Linear(hidden_units, num_classes),
#             nn.Softmax(dim=1)
#             )


#     def forward(self,x):
#         out = self.linear_relu_stack(x)
#         return out


def train_network(data,net):

    EPOCHS = int(CONFIG.get("training","epochs"))
    batch_size = int(CONFIG.get("training","batch_size"))
    LR = float(CONFIG.get("training","lr"))

    loss_fn = torch.nn.CrossEntropyLoss()
    optimizer = Adam(net.parameters(),lr=LR)

    train_data = DataLoader(dataset=data, batch_size=batch_size)

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
    parser = argparse.ArgumentParser()
    parser.add_argument('--datasetPath',
                        type=str,
                        required=True,
                        help='Bucket to store outputs.')

    args = parser.parse_args()
    print('read data from data bucket')
    data_path = CONFIG.get("data","path")
    
    data = AnyDataset(data_path)
    
    device = CONFIG.get("data",'device')

    MODEL_SAVE_PATH = 'models/model.pth'
    hidden = int(CONFIG.get("model","Hidden_layers"))
    N_classes = int(CONFIG.get("model","num_classes"))
    Inp_features  = int(CONFIG.get("model","input_features"))
    network = Network(input_features= Inp_features,
                hidden_units = hidden,
                num_classes = N_classes)
    
    print(network)
    trained_network = train_network(data,net=network)
    print('Saving models to {}'.format(MODEL_SAVE_PATH))
    #torch.save(trained_network, MODEL_SAVE_PATH) #saving the model locally to then upload it to bucket
    
    torch.save(trained_network.state_dict(),MODEL_SAVE_PATH)

    print('model saved')
    with open("/modelOutput.txt", "w") as output_file:
        output_file.write(MODEL_SAVE_PATH)
        print("Done!")
