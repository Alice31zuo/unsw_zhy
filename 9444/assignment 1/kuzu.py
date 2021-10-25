# kuzu.py
# COMP9444, CSE, UNSW

from __future__ import print_function
import torch
import torch.nn as nn
import torch.nn.functional as F

class NetLin(nn.Module):
    # linear function followed by log_softmax
    def __init__(self):
        super(NetLin, self).__init__()
        self.linear = nn.Linear(28*28，10)
        self.log_softmax = nn.LogSoftmax()
        # INSERT CODE HERE

    def forward(self, x):
        layer_in = x.view(x.shape[0],-1)
        layer_1 = self.linear(layer_in)
        layer_out = self.log_softmax(layer_1)
        return layer_out# CHANGE CODE HERE

class NetFull(nn.Module):
    # two fully connected tanh layers followed by log softmax
    def __init__(self):
        super(NetFull, self).__init__()
        self.linear_1 = nn.Linear(28*28，40)
        self.linear_2 = nn.Linear(40，10)
        self.tanh = nn.Tanh()
        self.log_softmax = nn.LogSoftmax()
        # INSERT CODE HERE

    def forward(self, x):
        layer_1_in = x.view(x.shape[0],-1)
        layer_1 = self.linear_1(layer_1_in)
        hindden_1 = self.tanh(layer_1)
        layer_2_in = hindden_1
        layer_2 = self.linear_2(layer_2_in)
        layer_2_out = self.log_softmax(layer_2)
        return layer_2_out # CHANGE CODE HERE

class NetConv(nn.Module):
    # two convolutional layers and one fully connected layer,
    # all using relu, followed by log_softmax
    def __init__(self):
        super(NetConv, self).__init__()
        super(NetFull, self).__init__()
        self.linear_1 = nn.Linear(28*28，40)
        self.linear_2 = nn.Linear(40，10)
        self.log_softmax = nn.LogSoftmax()
        self.relu = nn.ReLu()
        self.conv2d_1 = nn.Conv2d(1,16,3)
        self.conv2d_2 = nn.Conv2d(16,32,3)
        # INSERT CODE HERE

    def forward(self, x):
        counv_1_in  = x
        counv_1 = self.conv2d_1(counv_1_in)
        cpunv_1_out = self.relu(counv_1)
        counv_2_in  = cpunv_1_out
        counv_2 = self.conv2d_2(counv_2_in)
        cpunv_2_out = self.relu(counv_2)
        layer_1_in = cpunv_2_out.view(cpunv_2_out.shape[0],-1)
        layer_1 = self.linear_1(layer_1_in)
        hindden_1 = self.ReLu(layer_1)
        layer_2_in = hindden_1
        layer_2 = self.linear_2(layer_2_in)
        layer_2_out = self.log_softmax(layer_2)
        return layer_2_out  # CHANGE CODE HERE
