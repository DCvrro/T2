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

def gDeterminista(uavs):
    cost = 0
    uav_ant_id = 0
    uavs_orden = sorted(uavs, key=lambda uavs: uavs['midTime'], reverse=False) #UAVs ordenados de menor a mayor por medio del tiempo preferente
    
    for index, uav in enumerate(uavs_orden):
        if index == 0: #Primer UAV en aterrizar asumiendo que cae en su tiempo preferente
            uav['tiempo_aterrizaje'] = uav['midTime']
            cost = cost + 0
            uav_ant_id = uav['id_uav']
        else:
            tiempo_aterrizaje = uavs[uav_ant_id-1]['tiempo_aterrizaje'] + uav['times'][uav_ant_id-1]      #uav['midTime'] + uavs_orden[index-1]['times'][index]
            if tiempo_aterrizaje <= uav['topTime'] and tiempo_aterrizaje >= uav['botTime']: #Los uavs no pueden caer mas allá del tiempo máximo de aterrizaje
                uav['tiempo_aterrizaje'] = tiempo_aterrizaje
                cost = cost + abs(tiempo_aterrizaje - uav['midTime'])
                uav_ant_id = uav['id_uav']
            else:
                tiempo_aterrizaje =  abs(uavs[uav_ant_id-1]['tiempo_aterrizaje'] + uav['times'][uav_ant_id-1] - uav['midTime']) #uavs[uav_ant_id-1]['tiempo_aterrizaje'] + uav['times'][uav_ant_id-1]
                uav['tiempo_aterrizaje'] = uav['botTime']
                cost = cost + tiempo_aterrizaje
    return uavs_orden, cost

def gEstocastico(uavs):
    ##Vamos a generar una lista con los ids de cada uav para despues acceder de forma aleatoria a ellos mediante el greedy estocastico.
    cost = 0
    cant = len(uavs)
    tmpAterrizaje = 0
    i = 0 
    midTime = []
    midTimeTotal = 0 
    uav_result = []

    for uav in uavs: 
        midTime.append(uav['midTime'])
        midTimeTotal = midTimeTotal + uav['midTime']

    premium = False
    premiumID = 0
    for uav in uavs: 
        if uav['midTime'] == 0 or uav['topTime'] == 0 or uav['botTime'] == 0: 
            premium = True
            premiumID = uav['id_uav']
            break
    while((len(uavs)) != 0):
        if i == 0 and premium == False: # el primer uav me permite darle el tiempo de aterrizaje que yo quiera
            nR = random.randint(0,len(uavs)-1) #Genero un numero aleatorio para acceder a un uav de la lista de uavs ordenados
            this_uav = uavs[nR]
            this_uav['tiempo_aterrizaje'] = this_uav['midTime']
            uav_ant = this_uav
            uav_result.append(this_uav)
            uavs.remove(this_uav)
            i =  1 
            #Calculamos las probabilidades de cada uav segun midtime/ midtimetotal
            probUavs = []
            for uav in uavs:
                probUavs.append(uav['midTime']/midTimeTotal)
            continue
        elif i == 0 and premium == True:
            this_uav = uavs[premiumID-1]
            this_uav['tiempo_aterrizaje'] = this_uav['midTime']
            uav_ant = this_uav
            uav_result.append(this_uav)
            uavs.remove(this_uav)
            i =  1
            #Calculamos las probabilidades de cada uav segun midtime/ midtimetotal
            probUavs = []
            for uav in uavs:
                probUavs.append(uav['midTime']/midTimeTotal)
            continue
        else:
            nextMidtime= random.choices(uavs,probUavs)[0]
            #ahora teniendo el midtime, sacamos el id del uav a escoger
            for uav in uavs:
                if uav['midTime'] == nextMidtime['midTime']:
                    this_uav = uav
                    break
            tmpAterrizaje = uav_ant['tiempo_aterrizaje'] + this_uav['times'][uav_ant['id_uav']-1]
            if(tmpAterrizaje <= this_uav['topTime'] and tmpAterrizaje >= this_uav['botTime']): # si esta dentro de los rangos, lo uso
                this_uav['tiempo_aterrizaje'] = tmpAterrizaje                
                cost = cost + abs(tmpAterrizaje - this_uav['midTime']) # calculo los costos
                uav_ant = this_uav # Guardo en una temporal la informacion de uav
                uav_result.append(this_uav)
                uavs.remove(this_uav) # Elimino el uav usado para no repetirlo
                probUavs = [] # Reinicio la probabilidad de los uavs.
                for uav in uavs:
                    probUavs.append(uav['midTime']/midTimeTotal)
            else:
                tmpAterrizaje =  abs(uav_ant['tiempo_aterrizaje']-this_uav['midTime'])
                this_uav['tiempo_aterrizaje'] = this_uav['botTime']
                cost = cost + tmpAterrizaje
                uav_ant = this_uav
                uav_result.append(this_uav)
                uavs.remove(this_uav)
                probUavs = [] # Reinicio la probabilidad de los uavs.
                for uav in uavs:
                    probUavs.append(uav['midTime']/midTimeTotal)
            i = i + 1 
        
    print("Se leyeron ",i, " uavs")
    return uav_result

def evaluate_state(neighbor):
    cost_propio = 0
    cost_total = 0
    #av_ant = None
    cost = 0
    uavs = neighbor.copy()
    
    for index, uav in enumerate(neighbor):
        if index == 0: #Primer UAV en aterrizar asumiendo que cae en su tiempo preferente
            uav['tiempo_aterrizaje'] = uav['midTime']
            #print(uav['tiempo_aterrizaje'])
            uav_ant = uav
            #show_uavs_determinista(uav,cost)
            #print(uav)
            #print(neighbor)
            #print(uav_ant)
        else:
            tiempo_aterrizaje = uav_ant['tiempo_aterrizaje'] + uav['times'][uav_ant['id_uav']-1]      #uav['midTime'] + uavs_orden[index-1]['times']
            if tiempo_aterrizaje <= uav['topTime'] and tiempo_aterrizaje >= uav['botTime']: #Los uavs no pueden caer mas allá del tiempo máximo de aterrizaje
                uav['tiempo_aterrizaje'] = tiempo_aterrizaje
                #cost_propio = abs(tiempo_aterrizaje - uav['midTime'])
                #cost_total = cost_total + cost_propio
                cost = cost + abs(tiempo_aterrizaje - uav['midTime'])
                uav_ant_id = uav['id_uav']
            else:
                #tiempo_aterrizaje =  abs(uavs[uav_ant_id-1] + uav['times'][uav_ant['id_uav']-1] - uav['midTime']) #uavs[uav_ant_id-1]['tiempo_aterrizaje'] + uav['times'][uav_ant_id-1]
                tiempo_aterrizaje =  abs(uav_ant['tiempo_aterrizaje'] + uav['times'][uav_ant['id_uav']-1] - uav['midTime'])
                uav['tiempo_aterrizaje'] = uav['botTime']
                #cost_propio = tiempo_aterrizaje
                #cost_total = cost_total + cost_propio
                cost = cost + tiempo_aterrizaje
        #cost_propio = 0
        #print('Hola ',neighbor)
        #print(uav_ant)
    return cost, neighbor

def generate_neighbors(current_state, premium):
    vecino = []
    #n = len(current_state)
    #for i in range(n - 1, 0, -7):
    #    if premium == 0:
    #        j = random.randint(0, i)
    #        current_state[i], current_state[j] = current_state[j], current_state[i]
    #    elif premium == 1:
    #        j = random.randint(1, i)
    #        current_state[i], current_state[j] = current_state[j], current_state[i]
    #for i in range(n):
    #    vecino.append(current_state[i])
    #print('pene')
    if premium == 0:
        while True:
            p = random.randint(0,len(current_state)-1)
            k = random.randint(0,len(current_state)-1)
            #print(p)
            #print(k)
            #print(type(current_state))
            if p != k:
                current_state[p] , current_state[k] = current_state[k], current_state[p]
                vecino.append(current_state)
                break
    else:
        #print('pene3')
        while True:
            p = random.randint(1,14)
            k = random.randint(1,14)
            if p != k:
                current_state[p] , current_state[k] = current_state[k], current_state[p]
                vecino.append(current_state)
                break
    return current_state

def Hill_Climbing_mejor_mejora(sol_inicial):
    neighbor_score, neighbor = evaluate_state(sol_inicial)
    neighbor_inicial_score, neighbor_inicial = evaluate_state(sol_inicial)
    best_score = neighbor_score
    a = 0
    best_neighbor = neighbor
    neighbor_visitados = []
    igual = 0

    while True:
        if neighbor_score < best_score: #Como se alguna-mejora, la primera solución que mejore la solución actual
            best_score = neighbor_score
            best_neighbor = neighbor

        #print('\n Solución: ', neighbor, 'con costo: ', neighbor_score)

        for nei in neighbor:
            del nei['tiempo_aterrizaje']

        neighbor_visitados.extend(neighbor)

        if neighbor[0]['botTime'] == 0 and neighbor[0]['midTime'] == 0 and neighbor[0]['topTime'] == 0:
            neighbor = generate_neighbors(neighbor,1)
            if len(neighbor_visitados) > len(neighbor):
                for a in range(int(len(neighbor_visitados)/len(neighbor))): # 0,2
                    for c in range(len(neighbor)): # 0,15
                        if a > 0:
                            if neighbor[c]['id_uav'] != neighbor_visitados[len(neighbor)*a+c]['id_uav']: # 45 - 45 
                                neighbor_score, neighbor = evaluate_state(neighbor)
                        else:
                            if neighbor[c]['id_uav'] != neighbor_visitados[c]['id_uav']: 
                                neighbor_score, neighbor = evaluate_state(neighbor)
            else:
                for a in range(len(neighbor)):
                    if neighbor[a]['id_uav'] != neighbor_visitados[a]['id_uav']:
                        neighbor_score, neighbor = evaluate_state(neighbor)
                        break
        else:
            neighbor = generate_neighbors(neighbor,0)
            if len(neighbor_visitados) > len(neighbor):
                for a in range(int(len(neighbor_visitados)/len(neighbor))): # 0,2
                    for c in range(len(neighbor)): # 0,15
                        if a > 0:
                            if neighbor[c]['id_uav'] != neighbor_visitados[len(neighbor)*a+c]['id_uav']: # 45 - 45 
                                neighbor_score, neighbor = evaluate_state(neighbor)
                        else:
                            if neighbor[c]['id_uav'] != neighbor_visitados[c]['id_uav']: 
                                neighbor_score, neighbor = evaluate_state(neighbor)
            else:
                for a in range(len(neighbor)):
                    if neighbor[a]['id_uav'] != neighbor_visitados[a]['id_uav']:
                        neighbor_score, neighbor = evaluate_state(neighbor)
                        break

        if len(neighbor_visitados) == len(neighbor_inicial)*1:
            if neighbor_inicial_score == best_score:
                for a in range(len(best_neighbor)):
                    if best_neighbor[a]['id_uav'] == neighbor_inicial[a]['id_uav']:
                        igual = igual + 1
            if igual == len(best_neighbor):
                best_neighbor = neighbor_inicial
                best_score = neighbor_inicial_score
                break

    return best_neighbor, best_score

def Hill_Climbing_alguna_mejora(sol_inicial, costo_inicial):
    #print(sol_inicial)
    neighbor_score = costo_inicial
    #neighbor_inicial_score, neighbor_inicial = evaluate_state(sol_inicial)

    neighbor = sol_inicial #Arreglo de dicc

    best_score = costo_inicial
    a = 0
    best_neighbor = sol_inicial
    neighbor_visitados = []
    igual = 0

    while True:
        if neighbor_score < best_score: #Como se alguna-mejora, la primera solución que mejore la solución actual
            best_score = neighbor_score
            best_neighbor = neighbor

        print('\n Solución: ', neighbor, 'con costo: ', neighbor_score)

        if a != 0:
            for nei in neighbor:
                if 'tiempo_aterriza' in nei:
                    del nei['tiempo_aterrizaje']
                    #neighbor_visitados.append(neighbor.copy())
            
        #print(neighbor)
        for index, uav in enumerate(neighbor):
            #print(uav['botTime'])
            if uav['botTime'] == 0 and uav['midTime'] == 0 and uav['topTime'] == 0:
                neighbor = generate_neighbors(neighbor,1)
                if neighbor not in neighbor_visitados:
                    neighbor_score, neighbor = evaluate_state(neighbor)
                    neighbor_visitados.append(neighbor.copy())
                    break
                #if len(neighbor_visitados) > len(neighbor):
                #    for a in range(int(len(neighbor_visitados)/len(neighbor))): # 0,2
                #        for c in range(len(neighbor)): # 0,15
                #            if a > 0:
                #                if neighbor[c]['id_uav'] != neighbor_visitados[len(neighbor)*a+c]['id_uav']: # 45 - 45 
                #                    neighbor_score, neighbor = evaluate_state(neighbor)
                #                    break
                #            else:
                #               if neighbor[c]['id_uav'] != neighbor_visitados[c]['id_uav']: 
                #                    neighbor_score, neighbor = evaluate_state(neighbor)
                #                    break
                #else:
                #    for a in range(len(neighbor)):
                #        if neighbor[a]['id_uav'] != neighbor_visitados[a]['id_uav']:
                #            neighbor_score, neighbor = evaluate_state(neighbor)
                #            break
            else:
                #print('hola')
                neighbor = generate_neighbors(neighbor,0)
                #print(neighbor)
                if neighbor not in neighbor_visitados:
                    #print('hola2')
                    neighbor_score, neighbor = evaluate_state(neighbor)
                    neighbor_visitados.append(neighbor.copy())

                #if len(neighbor_visitados) > len(neighbor):
                #    for a in range(int(len(neighbor_visitados)/len(neighbor))): # 0,2
                #        for c in range(len(neighbor)): # 0,15
                #            if a > 0:
                #                if neighbor[c]['id_uav'] != neighbor_visitados[len(neighbor)*a+c]['id_uav']: # 45 - 45 
                #                    neighbor_score, neighbor = evaluate_state(neighbor)
                #                    break
                #            else:
                #                if neighbor[c]['id_uav'] != neighbor_visitados[c]['id_uav']: 
                #                    neighbor_score, neighbor = evaluate_state(neighbor)
                #                    break
                #else:
                #    for a in range(len(neighbor)):
                #        if neighbor[a]['id_uav'] != neighbor_visitados[a]['id_uav']:
                #            neighbor_score, neighbor = evaluate_state(neighbor)
                #            break
            
        print(len(neighbor_visitados))
        if len(neighbor_visitados) == len(neighbor)*5:
            break
            #if neighbor_inicial_score == best_score:
            #    for a in range(len(best_neighbor)):
            #        if best_neighbor[a]['id_uav'] == neighbor_inicial[a]['id_uav']:
            #            igual = igual + 1
        #if igual == len(best_neighbor):
        #    best_neighbor = neighbor_inicial
        #    best_score = neighbor_inicial_score
        #    break
        a = a + 1
    return best_neighbor, best_score

if __name__ == '__main__':
    print('Archivo a leer para aplicar HillClimbing en base al resultado del Greedy \n 1.- t2_Deimos.txt \n 2.- t2_Europa.txt \n 3.- t2_Titan.txt')
    choose = input()
    match choose:
        case '1': #En este caso encuentra una solución mejor a la pasada por el greedy determinista.
            archivo = 't2_Deimos.txt'
            uavs = leer(archivo)
            uavs_original = leer(archivo)
            b, costo_inicial = gDeterminista(uavs)
            #print(b)
            #print(costo)
            #for d in range(5):
                #uavs = leer(archivo)
                #uavs_original = leer(archivo)
                #b = gEstocastico(uavs)
            sol_inicial_indexs = []
            sol_inicial_data = []
            for i in b:
                sol_inicial_indexs.append(i['id_uav'])
            for a in sol_inicial_indexs:
                for c in uavs_original:
                    if a == c['id_uav']:
                        sol_inicial_data.append(c)
            #print(costo_inicial)
            mejor_sol, mejor_costo = Hill_Climbing_alguna_mejora(sol_inicial_data, costo_inicial) #Envía los ids de los uavs resultados del greedy.
            print('\n Mejor solución :',mejor_sol,' con costo: ',mejor_costo)
        case '2': #En este caso la mejor solución es el greedy determinista
            archivo = 't2_Europa.txt'
            uavs = leer(archivo)
            uavs_original = leer(archivo)
            b, costo_inicial = gDeterminista(uavs)
            #print(b)
            #print(costo)
            #for d in range(5):
                #uavs = leer(archivo)
                #uavs_original = leer(archivo)
                #b = gEstocastico(uavs)
            sol_inicial_indexs = []
            sol_inicial_data = []
            for i in b:
                sol_inicial_indexs.append(i['id_uav'])
            for a in sol_inicial_indexs:
                for c in uavs_original:
                    if a == c['id_uav']:
                        sol_inicial_data.append(c)
            #print(costo_inicial)
            mejor_sol, mejor_costo = Hill_Climbing_alguna_mejora(sol_inicial_data, costo_inicial) #Envía los ids de los uavs resultados del greedy.
            print('\n Mejor solución :',mejor_sol,' con costo: ',mejor_costo)
        case '3': #En este caso la mejor solución es el greedy determinista
            archivo = 't2_Titan.txt'
            uavs = leer(archivo)
            uavs_original = leer(archivo)
            b, costo_inicial = gDeterminista(uavs)
            #print(b)
            #print(costo)
            #for d in range(5):
                #uavs = leer(archivo)
                #uavs_original = leer(archivo)
                #b = gEstocastico(uavs)
            sol_inicial_indexs = []
            sol_inicial_data = []
            for i in b:
                sol_inicial_indexs.append(i['id_uav'])
            for a in sol_inicial_indexs:
                for c in uavs_original:
                    if a == c['id_uav']:
                        sol_inicial_data.append(c)
            #print(costo_inicial)
            mejor_sol, mejor_costo = Hill_Climbing_alguna_mejora(sol_inicial_data, costo_inicial) #Envía los ids de los uavs resultados del greedy.
            print('\n Mejor solución :',mejor_sol,' con costo: ',mejor_costo)
