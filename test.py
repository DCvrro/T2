def leer():
    
    with open('t2_Titan.txt','r+') as file:
        count = 0
        uav = {}
        drones = []
        for lines in file.readlines():
            lines = lines.split(' ')

            ######Correccion de texto ##### 
            if('\n' in lines[-1]):
                if(lines[-1] == '\n'): 
                    lines.pop()
                else:
                    lines[-1] = (lines[-1])[:-1] ## corta los nuemeros o palabras con un \n
            

            ##### Ingreso al diccionario #####
            if count == 0: ### Ingreso datos Cantidad de uavs
                uav['cantidad'] = lines
                count = 1
                continue

                ### Ingreso informacion de tiempos
            if count == 1 and len(lines) == 3:
                uav['botTime'] = lines[0]
                uav['midTime'] = lines[1]
                uav['topTime'] = lines[-1]
                count = 2
                continue
                
                ###Ingreso los tiempos asociados a la cantidad y de cada uav.
            if(count == 2 ):
                if 'times' in uav: ## Reviso si ya existe la seccion de registros de tiempos en el diccionario
                    if len(uav['times']) < int((uav.get('cantidad'))[0]): #Los voy ingresando si es que no cumplen con la cantidad dedatos dichos.
                        for datos in lines: 
                            uav['times'].append(datos)
                    else:
                        count = 1  
                        drones.append(uav)
                        del uav['botTime']
                        del uav['midTime']
                        del uav['topTime']
                        del uav['times']   
                else: # en caso contrario los creo y empieza a ingresar dentro del diccionario
                    for datos in lines:
                        if 'times' in uav: 
                            uav['times'].append(datos)
                        else:
                            uav['times'] = [datos]
    print((drones[0]).get('cantidad'))
    for drone in drones: 
        print('botTime:',(drone.get('botTime')))  
        print('midTime:',(drone.get('midTime')))
        print('topTime:',(drone.get('topTime')))
        print('Tiempos:', drone.get('times')) 
leer()