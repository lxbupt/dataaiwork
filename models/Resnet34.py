# _*_ coding : utf-8 _*_
# @Time : 2023/12/28 12:17
# @Author : 战斧牛排炖洋芋
# @File : Resnet34
# @Project : dataaiwork
# _*_ coding : utf-8 _*_
# @Time : 2023/12/28 11:37
# @Author : 战斧牛排炖洋芋
# @File : CNNModel04
# @Project : dataaiwork
import torch as t
import torch.nn as nn
import torchvision.models as models

device = t.device("cuda" if t.cuda.is_available() else "cpu")


# 定义新的CNN类，使用ResNet-34作为基础模型
class ResNet34CNN(nn.Module):
    def __init__(self, num_outinputs):
        super(ResNet34CNN, self).__init__()
        # 使用预训练的ResNet-34模型
        self.resnet34 = models.resnet34(pretrained=True)

        # 修改ResNet的全连接层，以适应CIFAR-10的类别数
        in_features = self.resnet34.fc.in_features
        self.resnet34.fc = nn.Linear(in_features, num_outinputs)

    def forward(self, x):
        return self.resnet34(x)

# # 设置参数
# batch_size = 100
# in_channels = 3
# num_classes = 10
# learning_rate = 0.001
# epochs = 10
#
# # 加载CIFAR-10数据集
# trainset = datasets.CIFAR10(
#     root="./cifar10data", train=True, download=True, transform=transforms.ToTensor()
# )
# testset = datasets.CIFAR10(
#     root="./cifar10data", train=False, download=True, transform=transforms.ToTensor()
# )
#
# trainloader = DataLoader(trainset, batch_size=batch_size, shuffle=True, num_workers=0)
# testloader = DataLoader(testset, batch_size=batch_size, shuffle=False, num_workers=0)
#
# # 创建ResNet34CNN模型
# model = ResNet34CNN(num_classes).to(device)
#
# # 修改优化器和学习率
# optimizer = t.optim.Adam(model.parameters(), lr=learning_rate)
#
# # 定义交叉熵损失
# criterion = nn.CrossEntropyLoss()

# 训练循环，使用tqdm包装迭代器
# for epoch in range(epochs):
#     print("Epoch %d/%d:" % (epoch + 1, epochs))
#     for i, (batchX, labels) in enumerate(tqdm(trainloader)):
#         batchX = batchX.to(device)
#         labels = labels.to(device)
#
#         # 清零梯度
#         optimizer.zero_grad()
#
#         # 前向传播
#         py = model(batchX)
#
#         # 计算损失
#         loss = criterion(py, labels)
#
#         # 反向传播和优化
#         loss.backward()
#         optimizer.step()
#
#         # 计算批次的准确率
#         p_labels = t.argmax(py, dim=1).flatten()
#         correct = (p_labels == labels).sum()
#         acc = correct / batchX.shape[0]
#
#         print("Loss: %.10f, Accuracy: %.2f%%" % (loss.item(), acc * 100))

# 保存模型
# savePath = "test.pth"
# t.save(model.state_dict(), savePath)
# print("模型保存到了:", savePath)
#
# # 模型评估
# correct = t.tensor(0).to(device)
# total = 0
#
# with t.no_grad():
#     for images, labels in testloader:
#         images = images.to(device)
#         labels = labels.to(device)
#         outputs = model(images)
#         predicted = t.argmax(outputs.data, 1)
#         total += labels.size(0)
#         correct += (predicted == labels).sum()
#
# print("模型在测试集上的准确性: %.2f%%" % (correct.item() / total * 100))
