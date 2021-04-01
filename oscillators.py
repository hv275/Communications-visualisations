import numpy as np

def sinosc(f,end):
    t = np.arange(0,end,0.001)
    return t, np.sin(f*2*np.pi*t)
    