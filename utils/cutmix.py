import numpy as np
import torch

'''
    input:x
    target:y
'''
def cutmix(x,y,beta = 1.0):
    # 和mixup非常类似
    # 服从beta分布，默认服从(0,1)的均匀分布
    lam = np.random.beta(beta, beta)
    rand_index = torch.randperm(x.size()[0]).cuda()
    # 随便选一个裁剪区域
    target_a = y
    target_b = y[rand_index]
    bbx1, bby1, bbx2, bby2 = rand_bbox(x.size(), lam)
    # exchange
    x[:, :, bbx1:bbx2, bby1:bby2] = x[rand_index, :, bbx1:bbx2, bby1:bby2]
    # 裁剪的区域，调整lam的值
    lam = 1 - ((bbx2 - bbx1) * (bby2 - bby1) / (x.size()[-1] * x.size()[-2]))
    # 训练的时候就需要重新按lam的权值分配loss了
    return input,target_a,target_b,lam



def rand_bbox(size, lam):
    W = size[2]
    H = size[3]
    cut_rat = np.sqrt(1. - lam)
    cut_w = np.int(W * cut_rat)
    cut_h = np.int(H * cut_rat)

    # uniform
    cx = np.random.randint(W)
    cy = np.random.randint(H)

    bbx1 = np.clip(cx - cut_w // 2, 0, W)
    bby1 = np.clip(cy - cut_h // 2, 0, H)
    bbx2 = np.clip(cx + cut_w // 2, 0, W)
    bby2 = np.clip(cy + cut_h // 2, 0, H)

    return bbx1, bby1, bbx2, bby2

'''
usage:
    criterion = nn.CrossEntropyLoss().to(device)    
    input,target_a,target_b,lam = cutmix(input,target)
    model = Network()
    model = model.to(device)
    output = model(input)
    loss = criterion(output, target_a) * lam + criterion(output, target_b) * (1. - lam)
'''