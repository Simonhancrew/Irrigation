import torch
import torch.nn as nn

def batch_norm(training,x,gamma,beta,moving_mean,moving_var,eps = 1e-5,momentum=0.9):
    # 训练的话就需要戴着两个参数一起运动了
    if training:
        # 使用二维卷积层的情况，计算通道维上（axis=1）的均值和方差。这里我们需要保持
        # x的形状以便后面可以做广播运算
        mean = x.mean(dim=0, keepdim=True).mean(dim=2, keepdim=True).mean(dim=3, keepdim=True)
        var = ((x - mean) ** 2).mean(dim=0, keepdim=True).mean(dim=2, keepdim=True).mean(dim=3, keepdim=True)
        # 训练模式下用当前的均值和方差做标准化
        x_hat = (x - mean) / torch.sqrt(var + eps)
        # 更新移动平均的均值和方差
        moving_mean = momentum * moving_mean + (1.0 - momentum) * mean
        moving_var = momentum * moving_var + (1.0 - momentum) * var
    else:
        x_hat = (x - moving_mean) / torch.sqrt(moving_var + eps)
    Y = gamma * x_hat + beta
    return Y,moving_mean, moving_var

'''
1 不需要计算梯度和参与梯度更新的参数，可以用self.register_buffer直接注册就可以了；注册的变量同样使用；
2 被包成nn.Parameter的参数，需要求梯度，但是不能加cuda（），否则会报错。 如果想在gpu上运算，可以将整个类的实例加.cuda（）。例如 bn = BatchNorm（**param），bn=bn.cuda().
'''
class BatchNorm2d(nn.Module):
    def __init__(self, num_features):
        super().__init__()
        shape = (1, num_features, 1, 1)
        # 参与求梯度和迭代的拉伸和偏移参数，分别初始化成0和1
        self.gamma = nn.Parameter(torch.ones(shape))
        self.beta = nn.Parameter(torch.zeros(shape))
        # 不参与求梯度和迭代的变量，全初始化成0
        self.register_buffer('moving_mean', torch.zeros(shape))
        self.register_buffer('moving_var', torch.ones(shape))

    def forward(self, x):
        # 如果X不在内存上，将moving_mean和moving_var复制到X所在显存上
        if self.moving_mean.device != x.device:
            self.moving_mean = self.moving_mean.to(x.device)
            self.moving_var = self.moving_var.to(x.device)

        '''
            训练的时候加model.train()
            推理的时候model.eval()
        '''
        # 保存更新过的moving_mean和moving_var, Module实例的traning属性默认为true, 调用.eval()后设成false
        y, self.moving_mean, self.moving_var = batch_norm(self.training,
                                                          x, self.gamma, self.beta, self.moving_mean,
                                                          self.moving_var, eps=1e-5, momentum=0.9)
        return y

