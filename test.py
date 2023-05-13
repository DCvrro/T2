def leer():
    drones = []
    with open('t2_Europa.txt','r+') as file:
        count = 0
        uav = {}
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
                    'botTime':0,
                    'midTime':0,
                    'topTime':0,
                    'times':[]
                }
                times = []
                uav['botTime'] = int(lines[0])
                uav['midTime'] = int(lines[1])
                uav['topTime'] = int(lines[-1])
                uav['times'] = times
                
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
                            #print('todos los tiempos')
                            count = 1  
                            uav['times'] = times
                            print(uav)
                            drones.append(uav)
                            #times.clear()
        #print(drones) 
    #print((drones[0]).get('cantidad'))
    #for drone in drones: 
        #print('botTime:',(drone.get('botTime')))  
        #print('midTime:',(drone.get('midTime')))
        #print('topTime:',(drone.get('topTime')))
        #print('Tiempos:', drone.get('times')) 
    return drones
leer()

if __name__ == '__main__':
    a = leer()
    print(a)