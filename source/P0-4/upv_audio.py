
import numpy as np
from scipy.io import wavfile

import os

def read(f):
    filename,extension = os.path.splitext(f)
    if extension=='.wav' or extension=='.WAV':
        return readwav(f)

    else:
        print('Invalid file type: ',extension)
        return

def write(f,sr,x):
    filename,extension = os.path.splitext(f)
    if np.max(np.abs(x)) >=1:
        print('Warning: Clipping signal. Samples >=1 are present.')
        xx = x.copy()
        xx[xx>=1] = (2**15-1 )/2**15
        xx[xx<-1]=-1
    else:
        xx=x
    if extension=='.wav' or extension=='.WAV':
        return writewav(f,sr,xx)
    else:
        print('Invalid file type: ',extension)
        return





def readwav(f):
    fs1,x1=wavfile.read(f)
    xx1=x1.astype('float64');
    xx1 *= 2**(-15)
    return fs1,xx1

def writewav(f,sr,x):

    xdesn=2**15*x
    xint16=xdesn.astype('int16')
    wavfile.write(f,sr,xint16)
