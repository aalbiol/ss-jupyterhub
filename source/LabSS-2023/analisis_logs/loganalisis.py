import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

def getLines(fichero):
    f = open(fichero, "r")
    lineas=f.readlines()

    lineas=[l.strip() for l in lineas]
    return lineas

####################################################################################################
def parseLine(linea):
    out={}
    if "Starting logger" in linea:
        out['starting']=True
    else:
        out['starting']=False
    
    if "Cerrando logger" in linea:
        out['closing']=True
    else:
        out['closing']=False

    campos=linea.split('*')
   # print(campos)
    dt_format='%Y-%m-%d %H:%M:%S'
    out['datetime']=datetime.strptime(campos[2].split('.')[0], dt_format)

    if out['starting'] or out['closing']:
        out['notebook'] = campos[3]
    else:
        out['notebook'] = campos[1]
    
    accion=campos[-1]

    out['Testing'] = False
    out['Success'] = False
    out['action'] = ''

    if "Testing" in accion and "Success" not in accion:
        palabras=accion.split(' ')
        palabras=palabras[1:]     
        out['action']=' '.join(palabras)
        out['Testing'] = True
    elif "Success"  in accion:
        palabras=accion.split(' ')
        palabras=palabras[2:]     
        out['action']=' '.join(palabras)
        out['Success'] = True
    elif not out['starting'] and not out['closing']:
        out['action']=accion
    
    return out


####################################################################################################
def parseLines(entrada):
    if isinstance(entrada,str):
        lineas = getLines(entrada)
    else:
        lineas = entrada
    out=[]
    for l in lineas:
        out.append(parseLine(l))
    return out

####################################################################################################
def setNotebooks(info):
    n = []
    for l in info:
        n.append(l['notebook'])
    return list(set(n))

####################################################################################################
def horasEnCuaderno(info,cuaderno):
    horas=[]
    for l in info:
        if l['notebook'] == cuaderno:
            horas.append(l['datetime'])
    horas.sort()
    return horas
    

####################################################################################################
def analisisHoras(horas,gap_min=60):
    ''' horas: lista de datetimes
        gap_min: cantidad de minutos entre dos entradas para no considerar pausa
        Devuelve: lista de intervalos de trabajo [(inicio,duracion_minutos)]
        '''
    inicios=[horas[0]]
    finales=[]
    for k in range(1,len(horas)):
        d = horas[k] - horas[k-1]
        minutos= d.days * 24* 60 + d.seconds /60
        if minutos > gap_min:
            finales.append(horas[k-1])
            inicios.append(horas[k])
    finales.append(horas[-1])
    intervalos=[]
    for ini,fin in zip(inicios,finales):
        d = fin - ini
        minutos = int(d.days * 24* 60 + d.seconds /60)
        intervalos.append((ini,minutos))
    return intervalos



####################################################################################################
def tiempoTrabajoCuaderno(info,cuaderno,gap_min = 60):
    ''' Suma los minutos empleados trabajando en el cuaderno
        También devuelve el número de intervalos trabajados
    '''
    
    intervalos = analisisHoras(horasEnCuaderno(info,cuaderno),gap_min)
    nintervalos = len(intervalos)
    minutos_totales = 0
    for i in intervalos:
        minutos_totales += i[1]
    return {'num_sesiones':nintervalos, 'min_totales':minutos_totales}


####################################################################################################
def testingsSuccesses(info,cuaderno):
    ''' Cuenta la cantidad de lineas testing y Success de un cuaderno '''
    ntesting = 0
    nsuccess = 0
    for i in info:
        if i['notebook'] != cuaderno:
            continue
        if i['Success']:
            nsuccess += 1
        if i['Testing']:
            ntesting += 1
    return {'ntesting':ntesting, 'nsuccess': nsuccess}

####################################################################################################
def resumen(fichero):
    ''' Devuelve un diccionarios con tantas entradas como cuadernos

        Los values de cada entrada son:
        num_sesiones: numero de veces que ha estado trabajando
        min_totales: de trabajo real con un gap < 60 min
        cantidad de testings y successes'''
    
    info = parseLines(fichero)
    cuadernos = setNotebooks(info)
    out={}
    for c in cuadernos:
        out[c]=tiempoTrabajoCuaderno(info,c)
        out[c].update(testingsSuccesses(info,c))
    return out

def asistencia(fichero,dias,horario):
    '''
    Devuelve para cada día del calendario la cantidad de entradas en los logs en cualquier cuaderno
    '''
    info = parseLines(fichero)

    out={}
    for dia in dias:
        out[dia.date()]=0
        
    for l in info:
        dia = l['datetime'].date()
        hora = l['datetime'].hour
        if dia not in out:
            continue
        if hora >= horario[0] and hora <horario[1]:
            out [dia] +=1
    return out      