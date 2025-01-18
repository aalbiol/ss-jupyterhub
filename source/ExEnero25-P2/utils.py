import numpy as np
import matplotlib.pyplot as plt
import math

def dibujaEspectro(espectro):

    amplitudes =np.abs(np.array([c[1] for c in espectro]))
    frecuencias =np.array([c[0] for c in espectro])
    _=plt.stem(frecuencias,np.abs(amplitudes), markerfmt=" ")
    _=plt.title('Espectro de amplitud')
    _=plt.xlabel('frecuencia')
    _=plt.xlim([-0.1*np.max(frecuencias),1.2*np.max(frecuencias)]) 
    _=plt.grid()


def creaComponentes(espectro,t):
    '''
    espectro: lista de tuplas de 3 elementos (frec,ampl,fase)
    t: Instantes de tiempo
    
    Devuelve un array de numpy con tantas columnas como elementos tenga el espectro
    Cada una de ellas es una componente frecuencial
    
    La señal suma se puede obtener haciendo np.sum(out,axis=1)
    '''
    ncomponentes = len(espectro)
    ninstantes = len(t)
    out=np.zeros((ninstantes,ncomponentes))
    for k in range(ncomponentes):
        frecuencia = espectro[k][0]
        amplitud = espectro[k][1]
        fase = espectro[k][2]      
        out [:,k]= amplitud * np.cos(2*math.pi*frecuencia*t + fase)
    return out