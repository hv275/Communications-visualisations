import numpy as np

def sinosc(f,end,mag,fs=1/0.001):
    t = np.arange(0,end,1/fs)
    return t, np.sin(f*2*np.pi*t)*mag


    