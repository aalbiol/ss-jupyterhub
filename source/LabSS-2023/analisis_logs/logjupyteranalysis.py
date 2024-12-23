from tqdm import tqdm
import pandas as pd


def analisis_linea(linea):

    if "GET" not in linea:
        return
    if "workspaces"  not in linea:
        return
    campos=linea.split(" ")
    if len(campos) < 3:
        return
    #print(campos)
    campo_fecha=campos[1]
    campo_hora=campos[2]
    campo_ip=None
    for c in campos[3:]:
        if "@" in c:
            campo_ip=c


    if campo_ip is None:            
        return
    #print(campo_ip)
    campo_ip=campo_ip[1:-1]
    campos_ip=campo_ip.split("@")
    usuario=campos_ip[0]
    dir_ip=campos_ip[-1].split(":")[-1]
    if len(usuario) < 2:
        return
    if usuario =="profesor":
        return
    #print(campo_fecha,campo_hora,usuario,dir_ip)
    #time.sleep(.1)
    return campo_fecha,campo_hora,usuario,dir_ip

def carga_tabla(ficherologs):
    with open(ficherologs, 'r') as file1:
        lineas = file1.readlines()
    fechas=[]
    horas=[]
    usuarios=[]
    ips=[]
    
    data=[]
    for l in tqdm(lineas):
        res=analisis_linea(l)
        if res is None:
            continue
        fecha,hora,usuario,dir_ip=res
        hora=hora[:5]
        #print(fecha,hora)
        fechas.append(fecha)
        horas.append(hora)
        usuarios.append(usuario)
        ips.append(dir_ip)
        data.append({"fecha":fecha,"hora":hora,"usuario":usuario, "ip":dir_ip})

    df=pd.DataFrame(data)

    df['hora_dt']=pd.to_datetime(df['hora'],format="%H:%M")
    return df

def detecta_usuarios_dobles(ficherologs):

    df=carga_tabla(ficherologs)
############ Solucion con pandas
    #df1=df.groupby(["fecha","ip"]).usuario.unique().tolist()
    #casos_pandas=[c for c in df1 if len(c)>1]
    #print(casos_pandas)
###############################################    
    
    usuarios_por_ip={}
    for k in range(len(df)):
        evento=df.iloc[k]
        usuarios_por_ip[(evento.fecha,evento.ip)]=set()
    for k in range(len(df)):
        evento=df.iloc[k]
        usuarios_por_ip[(evento['fecha'],evento.ip)].add((evento.usuario))   

    casos_interesantes={}
    for k,v in usuarios_por_ip.items():
        if len(v)>1:
            casos_interesantes[k]=v

    for k,v in casos_interesantes.items():
        fecha=k[0]
        ip=k[1]
        usuarios=v
        horas_usuario={}
        for u in usuarios:
            horas_usuario[u]=[]
        for k in range(len(df)):
            evento=df.iloc[k]
            if evento.fecha != fecha :
                continue
            if evento.ip != ip:
                continue
            evento.usuario
            if evento.usuario in usuarios:
                horas_usuario[evento.usuario].append(evento.hora_dt)
        print("=========================")
        for k,v in horas_usuario.items():
            print(k,min(v),max(v))
        
    return casos_interesantes



def detecta_usuarios_dobles_hora(ficherologs):
    with open(ficherologs, 'r') as file1:
        lineas = file1.readlines()
    fechas=[]
    horas=[]
    usuarios=[]
    ips=[]
    
    data=[]
    for l in tqdm(lineas):
        res=analisis_linea(l)
        if res is None:
            continue
        fecha,tiempo,usuario,dir_ip=res
        hora=int(tiempo.split(':')[0])

        fechas.append(fecha)
        horas.append(hora)
        usuarios.append(usuario)
        ips.append(dir_ip)
        data.append({"fecha":fecha,"hora":hora,"usuario":usuario, "ip":dir_ip})

    df=pd.DataFrame(data)
############ Solucion con pandas
    #df1=df.groupby(["fecha","ip"]).usuario.unique().tolist()
    #casos_pandas=[c for c in df1 if len(c)>1]
    #print(casos_pandas)
###############################################    
    
    usuarios_por_ip={}
    for k in range(len(df)):
        evento=df.iloc[k]
        usuarios_por_ip[(evento.fecha,evento.hora,evento.ip)]=set()
    for k in range(len(df)):
        evento=df.iloc[k]
        usuarios_por_ip[(evento['fecha'],evento['hora'],evento.ip)].add(evento.usuario)   

    casos_interesantes={}
    for k,v in usuarios_por_ip.items():
        if len(v)>1:
            casos_interesantes[k]=v
    return casos_interesantes