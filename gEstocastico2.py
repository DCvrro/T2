import random

def leer(archivo):
    drones = []
    with open(archivo,'r+') as file:
        count = 0
        uav = {}
        id = 1 
        tiempos = []
        times = []
        for lines in file.readlines():
            lines = lines.split(' ')

            ######Correccion de texto ##### 
            if('\n' in lines[-1]):
                if(lines[-1] == '\n'): 
                    lines.pop()
                else:
                    lines[-1] = (lines[-1])[:-1] ## corta los números o palabras con un \n
            
            ##### Ingreso al diccionario #####
            if count == 0: ### Ingreso datos Cantidad de uavs
                uav['cantidad'] = int(lines[0])
                limit = int(lines[0])
                count = 1
                continue

                ### Ingreso informacion de tiempos
            if count == 1 and len(lines) == 3:
                uav = {
                    'id_uav': id,
                    'botTime':0,
                    'midTime':0,
                    'topTime':0,
                    'times':[]
                }
                times = []
                uav['id_uav'] = id
                uav['botTime'] = int(lines[0])
                uav['midTime'] = int(lines[1])
                uav['topTime'] = int(lines[-1])
                uav['times'] = times

                id = id + 1
                count = 2
                continue
                
                ###Ingreso los tiempos asociados a la cantidad y de cada uav.
            if(count == 2 ):
                if 'times' in uav: ## Reviso si ya existe la seccion de registros de tiempos en el diccionario
                    if len(times) < limit: #Los voy ingresando si es que no cumplen con la cantidad dedatos dichos.
                        for datos in lines: 
                            tiempos.append(int(datos))
                        times.extend(tiempos)
                        tiempos.clear()
                        if len(times) == limit:
                            count = 1  
                            uav['times'] = times
                            drones.append(uav)
    return drones



def gEstocastico(uavs):
    ##Vamos a generar una lista con los ids de cada uav para despues acceder de forma aleatoria a ellos mediante el greedy estocastico.
    cost = 0
    uav_ant_id = 0
    uavs_orden = sorted(uavs, key=lambda uavs: uavs['midTime'], reverse=False) #Esto podria cambiarse a que tmbn sea aleatorio
    print('\n Uavs ordenados por tiempo preferente')                           #aleatorizar el hecho de trabajar cm por mid o bot time
    print('\n')
    tmpAterrizaje = 0
    i = 0 
    while((len(uavs)) != 0):
        nR  =  random.randint(0,len(uavs_orden)-1) #Genero un numero aleatorio para acceder a un uav de la lista de uavs ordenados
        uav = uavs_orden[nR]
        if i == 0: # el primer uav me permite darle el tiempo de aterrizaje que yo quiera
            uav['tiempo_aterrizaje'] = uav['midTime']
            uav_ant = uav
            show_uavs_info(uav,cost)
            uavs.remove(uav)
            uavs_orden.remove(uav)
            i = i + 1 
            continue
        else:
            tmpAterrizaje = uav_ant['tiempo_aterrizaje'] + uav['times'][uav_ant['id_uav']-1]
            if(tmpAterrizaje <= uav['topTime'] and tmpAterrizaje >= uav['botTime']):
                uav['tiempo_aterrizaje'] = tmpAterrizaje
                show_uavs_info(uav,cost)
                uavs.remove(uav)
                uavs_orden.remove(uav)
                cost = cost + abs(tmpAterrizaje - uav['midTime'])
                uav_ant = uav
                i = i + 1
            if i > 20:
                break
def show_uavs_info(uav,cost): 
    print(' ID :',uav.get('id_uav')," | Tiempo de aterrizaje: ", uav.get('tiempo_aterrizaje'), ' | Costo actual: ', cost)

def show_uavs(uavs):
    b = True
    large = len(uavs) 
    for uav in uavs: 
        if b :
            print("UAVs :", large  ) 
            print(' ID :',uav.get('id_uav')," | ", 'Range :', uav.get('botTime')," | ", uav.get('midTime')," | ",uav.get('topTime'),'|', uav.get('times'))
            b = False
        else:
            print(' ID :',uav.get('id_uav')," | ", 'Range :', uav.get('botTime')," | ", uav.get('midTime')," | ",uav.get('topTime'),'|', uav.get('times')) 



def printUAVs(uavs):
    for uav in uavs:
        print(uav)
        print("")

if __name__ == '__main__':
    print('Archivo a leer para aplicar Greedy Determinista \n 1.- t2_Deimos.txt \n 2.- t2_Europa.txt \n 3.- t2_Titan.txt')
    choose = input()
    match choose:
        case '1':
            archivo = 't2_Deimos.txt'
            uavs = leer(archivo)
            #printUAVs(uavs)
            gEstocastico(uavs)
        case '2':
            archivo = 't2_Europa.txt'
            uavs = leer(archivo) 
            #printUAVs(uavs)
            gEstocastico(uavs)
        case '3':
            archivo = 't2_Titan.txt'
            uavs = leer(archivo) 
            #printUAVs(uavs)
            gEstocastico(uavs)