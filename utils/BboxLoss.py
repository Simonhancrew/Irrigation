import numpy as np
import matplotlib.pyplot as plt

def L1(x):
    res = np.where(x > 0,x,np.abs(x))
    return res

def L2(x):
    return np.square(x)


def smoothL1(x):
    return np.where(np.abs(x) < 1,0.5 * np.square(x),np.abs(x) - 0.5)


def plot(funcs,x):
    fig,ax = plt.subplots()
    ax.set(xlabel='input', ylabel='output')
    ax.set_title('Loss summary')
    ax.grid()
    ax.set(xlim=(-2,2),ylim=(0,4))

    for func in funcs:
        y = func(x)
        ax.plot(x,y,linewidth=2,label=func.__name__)
        # fig.show()
    ax.legend(loc='upper right')
    fig.show()
    fig.savefig('loss_curves.jpg')