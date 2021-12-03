import torch
import torch.nn as nn
from torchvision.models.utils import load_state_dict_from_url
from torchsummary import summary

model_url = {
    'vgg16': 'https://download.pytorch.org/models/vgg16-397923af.pth',
}

cfg = {
    'D': [64, 64, 'M', 128, 128, 'M', 256, 256, 256, 'M', 512, 512, 512, 'M', 512, 512, 512, 'M'],
}

class VGG(nn.Module):
    def __init__(self,features,num_classes=1000,init_weight=True):
        super().__init__()
        self.feartures = features
        # 返回一个自适应的（batch,chanel,7,7）的特征图
        self.avgpool = nn.AdaptiveAvgPool2d((7,7))
        # 最后的输出分类器
        self.classifier = nn.Sequential(
            nn.Linear(512*7*7,4096),
            nn.ReLU(True),
            nn.Dropout(),
            nn.Linear(4096,4096),
            nn.ReLU(True),
            nn.Dropout(),
            nn.Linear(4096,num_classes),
        )
        if init_weight:
            self.initialize_weights()

    # 前向传递
    def forward(self,x):
        x = self.feartures(x)
        x = self.avgpool(x)
        x = torch.flatten(x,1) # flatten成一维
        x = self.classifier(x)
        return x

    def initialize_weights(self):
        for m in self.modules():
            if isinstance(m,nn.Conv2d):
                # todo kaiming_init
                nn.init.kaiming_normal_(m.weight,mode='fan_out',nonlinearity='relu')
                if m.bias is not None:
                    nn.init.constant_(m.bias,0)
            elif isinstance(m,nn.BatchNorm2d):
                nn.init.constant_(m.weight,1)
                nn.init.constant_(m.bias,0)
            elif isinstance(m,nn.Linear):
                nn.init.normal_(m.weight,0,0.01)
                nn.init.constant_(m.bias,0)

    # 训练冻结主干和解冻
    def freeze_backbone(self):
        for param in self.feartures.parameters():
            param.require_grad = False

    def unfreeze_backbone(self):
        for param in self.feartures.parameters():
            param.require_grad = True

#  cfg中网络结构主结构实现，VGG中的features
def make_layers(cfg,batch_norm=False):
    layers = []
    in_chanels = 3
    for v in cfg:
        if v == 'M':
            layers += [nn.MaxPool2d(kernel_size=2,stride=2)]
        else:
            conv2d = nn.Conv2d(in_chanels,v,kernel_size=3,padding=1)
            if batch_norm:
                layers += [conv2d,nn.BatchNorm2d(v),nn.ReLU(inplace=True)]
            else:
                layers += [conv2d,nn.ReLU(inplace=True)]
            in_chanels = v
    return nn.Sequential(*layers)

def vgg16(pretrained=False,progress=True,num_classes=1000):
    model = VGG(make_layers(cfg['D']))
    if pretrained:
        state_dict = load_state_dict_from_url(model_url['vgg16'],model_dir='./model_data',progress=progress)
        model.load_state_dict(state_dict,strict=False)
    if num_classes != 1000:
        model.classifier = nn.Sequential(
            nn.Linear(512 * 7 * 7,496),
            nn.ReLU(True),
            nn.Dropout(),
            nn.Linear(4096,4096),
            nn.ReLU(True),
            nn.Dropout(),
            nn.Linear(4096,num_classes),
        )
    return model

if __name__=='__main__':
    model = vgg16().train().cuda()
    summary(model,(3,224,224))