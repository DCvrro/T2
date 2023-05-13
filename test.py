def leer():
    drones = []
    with open('t2_Titan.txt','r+') as file:
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
leer()

def gDeterminista(uavs):
    nTimes = []
    uavs_orden = sorted(uavs, key=lambda uavs: uavs['midTime'], reverse=False)
    print('\n Uavs ordenados por tiempo preferente')
    show_uavs(uavs_orden)
    #print(uavs_orden)

def gEstocastico():
    print("")  

def HillClimbing():
    print("")

#Mostrar uavs, me dio paja copiar y pegar todo el rato el for para imprimirlos.
def show_uavs(uavs):
    b = True
    large = len(uavs) 
    for uav in uavs: 
        if b :
            print("UAVs :", large  ) 
            print(' ID :',uav.get('id_uav')," | ", 'Range :', uav.get('botTime')," | ", uav.get('midTime')," | ",uav.get('topTime'))
            b = False
        else:
            print(' ID :',uav.get('id_uav')," | ", 'Range :', uav.get('botTime')," | ", uav.get('midTime')," | ",uav.get('topTime')) 

if __name__ == '__main__':
    uavs = leer()
    b = True
    large = len(uavs)

    show_uavs(uavs)
    
    gDeterminista(uavs)
    ### Para el primer greedy se recomienda ordenar los uavs sgn el tipo de tiempo que se prefiera, creo que el mejor
    #puede ser ordenar por el tiempo  preferente.
    