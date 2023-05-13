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

def gDeterminista(uavs):
    cost = 0
    uav_ant_id = 0
    uavs_orden = sorted(uavs, key=lambda uavs: uavs['midTime'], reverse=False) #UAVs ordenados de menor a mayor por medio del tiempo preferente
    print('\n Uavs ordenados por tiempo preferente')
    print('\n')
    
    for index, uav in enumerate(uavs_orden):
        if index == 0: #Primer UAV en aterrizar asumiendo que cae en su tiempo preferente
            uav['tiempo_aterrizaje'] = uav['midTime']
            cost = cost + 0
            uav_ant_id = uav['id_uav']
            show_uavs_determinista(uav,cost)
        else:
            tiempo_aterrizaje = uavs[uav_ant_id-1]['tiempo_aterrizaje'] + uav['times'][uav_ant_id-1]      #uav['midTime'] + uavs_orden[index-1]['times'][index]
            if tiempo_aterrizaje <= uav['topTime'] and tiempo_aterrizaje >= uav['botTime']: #Los uavs no pueden caer mas allá del tiempo máximo de aterrizaje
                uav['tiempo_aterrizaje'] = tiempo_aterrizaje
                cost = cost + abs(tiempo_aterrizaje - uav['midTime'])
                uav_ant_id = uav['id_uav']
            else:
                print('\n UAV ',uav['id_uav'],' no puede aterrizar en un principio.')
                print('......')
                print('Se extiende su tiempo de aterrizaje para que pueda aterrizar.')
                tiempo_aterrizaje =  abs(uavs[uav_ant_id-1]['tiempo_aterrizaje'] - uav['botTime']) #uavs[uav_ant_id-1]['tiempo_aterrizaje'] + uav['times'][uav_ant_id-1]
                uav['tiempo_aterrizaje'] = uav['botTime']
                cost = cost + tiempo_aterrizaje
            show_uavs_determinista(uav,cost)
    print('Costo Total: ',cost)
 
def show_uavs_determinista(uav,cost): 
    print(' ID :',uav.get('id_uav')," | Tiempo de aterrizaje: ", uav.get('tiempo_aterrizaje'), ' | Costo actual: ', cost)


#Mostrar uavs, me dio paja copiar y pegar todo el rato el for para imprimirlos.
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

if __name__ == '__main__':
    print('Archivo a leer para aplicar Greedy Determinista \n 1.- t2_Deimos.txt \n 2.- t2_Europa.txt \n 3.- t2_Titan.txt')
    choose = input()
    match choose:
        case '1':
            archivo = 't2_Deimos.txt'
            uavs = leer(archivo) 
            gDeterminista(uavs)
        case '2':
            archivo = 't2_Europa.txt'
            uavs = leer(archivo) 
            gDeterminista(uavs)
        case '3':
            archivo = 't2_Titan.txt'
            uavs = leer(archivo) 
            gDeterminista(uavs)