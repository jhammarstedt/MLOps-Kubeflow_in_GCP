from torch import nn
class Network(nn.Module):
    def __init__(self,input_features=4,hidden_units=50,num_classes=3):
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
