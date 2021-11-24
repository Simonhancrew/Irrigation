import numpy as np
import matplotlib.pyplot as plt


def sigmoid(x):
    res = 1.0 / (1.0 + np.exp(-x))
    return res

def relu(x):
    res = np.maximum(x.data,0)
    return res

def leaky_relu(x,alpha = 1 / 5.5):
    res = np.maximum(x.data,0) + alpha * np.minimum(x.data,0)
    return res

def elu(x,alpha = 1):
    res = np.maximum(x.data,0) + alpha * (np.exp(np.minimum(x.data,0)) - 1)
    return res

def plot(func,x):
    fig,ax = plt.subplots()
    y = func(x)
    ax.plot(x,y,linewidth=2)
    ax.set(xlabel='input',ylabel='output')
    ax.set_title(func.__name__)
    ax.grid()
    if func.__name__ != 'sigmoid':
        ax.set(xlim=(-100,100),ylim=(-50,100))
    # fig.show()
    fig.savefig('{}.jpg'.format(func.__name__))
    print('plt {} done'.format(func.__name__))

if __name__=='__main__':
    x = np.arange(-100,100,1,dtype = np.float64)
    func = [elu,relu,sigmoid,leaky_relu]
    for acti in func:
        plot(acti,x)