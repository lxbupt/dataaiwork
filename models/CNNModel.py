import torch.nn as nn


# 1.定义CNN神经网络结构  5层的神经网络结构
class CNN(nn.Module):

    def __init__(self, in_channels, num_outinputs):
        super(CNN, self).__init__()
        # 定义网络层 3*32*32
        self.conv1 = nn.Conv2d(in_channels=in_channels, out_channels=32, kernel_size=(5, 5), padding=2)  # 32*32*32
        self.maxpool1 = nn.MaxPool2d(kernel_size=(2, 2))  # 32*16*16
        self.relu1 = nn.ReLU()
        self.conv2 = nn.Conv2d(in_channels=32, out_channels=16, kernel_size=(3, 3), padding=1)  # 16*16*16
        self.relu2 = nn.ReLU()
        self.flatten = nn.Flatten()  # 16*14*14 拉成一维的  3136
        self.linear3 = nn.Linear(4096, 256)
        self.relu3 = nn.ReLU()
        self.linear4 = nn.Linear(256, num_outinputs)
        pass

    def forward(self, inputs):
        outputs = self.conv1(inputs)
        outputs = self.maxpool1(outputs)
        outputs = self.relu1(outputs)
        outputs = self.conv2(outputs)
        outputs = self.relu2(outputs)
        outputs = self.flatten(outputs)  # Flatten
        outputs = self.linear3(outputs)
        outputs = self.relu3(outputs)
        outputs = self.linear4(outputs)
        return outputs
        pass

    pass
