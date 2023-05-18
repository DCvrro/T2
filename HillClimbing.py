import random
import copy

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
    return uav_result, cost

def evaluate_state(neighbor):
    cost = 0
    uavs = neighbor.copy()
    #print(uavs)
    for index, uav in enumerate(uavs):
        if index == 0: #Primer UAV en aterrizar asumiendo que cae en su tiempo preferente
            uav['tiempo_aterrizaje'] = uav['midTime']
            #print(uav)
            uav_ant = uav
            #print(uav_ant)
        else:
            #print(uav_ant)
            tiempo_aterrizaje = uav_ant['tiempo_aterrizaje'] + uav['times'][uav_ant['id_uav']-1]      #uav['midTime'] + uavs_orden[index-1]['times']
            if tiempo_aterrizaje <= uav['topTime'] and tiempo_aterrizaje >= uav['botTime']: #Los uavs no pueden caer mas allá del tiempo máximo de aterrizaje
                uav['tiempo_aterrizaje'] = tiempo_aterrizaje
                cost = cost + abs(tiempo_aterrizaje - uav['midTime'])
                
            elif tiempo_aterrizaje > uav['topTime'] or tiempo_aterrizaje < uav['botTime']:
                tiempo_aterrizaje =  abs(uav_ant['tiempo_aterrizaje'] + uav['times'][uav_ant['id_uav']-1] - uav['midTime'])
                uav['tiempo_aterrizaje'] = uav['botTime']
                cost = cost + tiempo_aterrizaje
                #uav_ant = uav
            #print(uav,cost)
            uav_ant = uav
        #print(index)
    return cost, uavs

def generate_neighbors(current_state, premium):
    if premium == 0:
        while True:
            p = random.randint(0,len(current_state)-1)
            k = random.randint(0,len(current_state)-1)
            if p != k:
                current_state[p] , current_state[k] = current_state[k], current_state[p]
                break
    else:
        while True:
            p = random.randint(1,14)
            k = random.randint(1,14)
            if p != k:
                current_state[p] , current_state[k] = current_state[k], current_state[p]
                break
    return current_state

def Hill_Climbing_alguna_mejora(sol_inicial, costo_inicial, max_iter):
    sol_inicial_aux = copy.deepcopy(sol_inicial)
    neighbor_ant = sol_inicial
    best_score = copy.deepcopy(costo_inicial)
    best_neighbor = [sol_inicial]
    for nei in neighbor_ant:
        if 'tiempo_aterrizaje' in nei:
            del nei['tiempo_aterrizaje']
    neighbor_actual = sol_inicial
    neighbor_score_actual = costo_inicial
    a = 0
    igual_score = 0
    distinta = 0

    while True:
        if neighbor_score_actual < best_score: #Como se alguna-mejora, la primera solución que mejore la solución actual
            best_score = copy.deepcopy(neighbor_score_actual)
            best_neighbor.pop()
            best_neighbor.append(copy.deepcopy(neighbor_actual))
            print('\n Solución Mejor del Alguna-Mejora encontrada con costo: ', best_score )
            print(best_neighbor)
            neighbor_ant = neighbor_actual
            neighbor_actual = None
            distinta = distinta + 1
        elif neighbor_score_actual == best_score and neighbor_actual != best_neighbor:
            igual_score = igual_score + 1 
        else:
            neighbor_actual = neighbor_ant
            for nei in neighbor_actual:
                if 'tiempo_aterriza' in nei:
                    del nei['tiempo_aterrizaje']
        if neighbor_actual != neighbor_ant:
            for nei in neighbor_ant:
                if 'tiempo_aterriza' in nei:
                    del nei['tiempo_aterrizaje']

        if neighbor_ant[0]['botTime'] == 0 and neighbor_ant[0]['midTime'] == 0 and neighbor_ant[0]['topTime'] == 0:
            neighbor_actual = generate_neighbors(neighbor_ant,1)
            neighbor_score_actual, neighbor_actual = evaluate_state(neighbor_actual)
        else:
            neighbor_actual = generate_neighbors(neighbor_ant,0)
            neighbor_score_actual, neighbor_actual = evaluate_state(neighbor_actual)

        if max_iter-1 == a and igual_score != 0 and distinta == 0:
            print('Sol inicial ya que ninguna fue mejor, pero otras daban lo mismo')
            return sol_inicial_aux, costo_inicial
        elif max_iter-1 == a and distinta != 0:
            print('Sol mejor distinta')
            return best_neighbor, best_score
        a = a + 1

def Hill_Climbing_mejor_mejora(sol_inicial, costo_inicial):
    neighbor_score = costo_inicial
    neighbor = sol_inicial 
    best_score = costo_inicial
    a = 0
    best_neighbor = sol_inicial
    neighbor_visitados = []

    while True:

        #print('\n Solución Mejor-Mejora: ', neighbor, 'con costo: ', neighbor_score)

        if a != 0:
            for nei in neighbor:
                if 'tiempo_aterriza' in nei:
                    del nei['tiempo_aterrizaje']
        if a == 0:
            neighbor_visitados.append(neighbor.copy())

        if neighbor[0]['botTime'] == 0 and neighbor[0]['midTime'] == 0 and neighbor[0]['topTime'] == 0:
            while len(neighbor_visitados) == 1000:
                neighbor = generate_neighbors(neighbor,0)
                neighbor_visitados.append(neighbor.copy())
                #if neighbor not in neighbor_visitados:
                neighbor_score, neighbor = evaluate_state(neighbor)
                if neighbor_score < best_score: #Como se alguna-mejora, la primera solución que mejore la solución actual
                    best_score = neighbor_score
                    best_neighbor = neighbor
            break
        else:
            while len(neighbor_visitados) == 1000:
                neighbor = generate_neighbors(neighbor,0)
                neighbor_visitados.append(neighbor.copy())
                if neighbor not in neighbor_visitados:
                    neighbor_score, neighbor = evaluate_state(neighbor)
                    if neighbor_score < best_score: #Como se alguna-mejora, la primera solución que mejore la solución actual
                        best_score = neighbor_score
                        best_neighbor = neighbor
                        print('\n Solución Mejor-Mejora: ', neighbor, 'con costo: ', neighbor_score)
            break

        #if len(neighbor_visitados) == 1000:
        #    break

        a = a + 1
    return best_neighbor, best_score

if __name__ == '__main__':
    print('Leer archivo \n 1.- t2_Deimos.txt \n 2.- t2_Europa.txt \n 3.- t2_Titan.txt')
    choose = input()
    match choose:
        case '1': #En este caso encuentra una solución mejor a la pasada por el greedy determinista.
            archivo = 't2_Deimos.txt'
            print('Aplicar \n 1.- Hill Climbing Alguna-Mejora con Greedy Determinista'+
                  '\n 2.- Hill Climbing Alguna-Mejora con Greedy Estocástico \n 3.- Hill Climbing Mejor-Mejora con Greedy Determinista ' + 
                  '\n 4.- Hill Climbing Mejor-Mejora con Greedy Estocástico')
            choose2 = input()
            match choose2:
                case '1':
                    uavs = leer(archivo)
                    uavs_original = uavs.copy()
                    b, costo_inicial = gDeterminista(uavs)
                    sol_inicial_indexs = []
                    sol_inicial_data = []
                    for i in b:
                        sol_inicial_indexs.append(i['id_uav'])
                    for a in sol_inicial_indexs:
                        for c in uavs_original:
                            if a == c['id_uav']:
                                sol_inicial_data.append(c)
                    print(costo_inicial)
                    #print('Hola ', sol_inicial_data)
                    mejor_sol, mejor_costo = Hill_Climbing_alguna_mejora(sol_inicial_data, costo_inicial, max_iter = 100) #Envía los ids de los uavs resultados del greedy.
                    print('\n Mejor solución :',mejor_sol,' con costo: ',mejor_costo)
                case '2':
                    for d in range(5):
                        uavs = leer(archivo)
                        uavs_original = uavs.copy()
                        b,costo_inicial = gEstocastico(uavs)
                        sol_inicial_indexs = []
                        sol_inicial_data = []
                        for i in b:
                            sol_inicial_indexs.append(i['id_uav'])
                        for a in sol_inicial_indexs:
                            for c in uavs_original:
                                if a == c['id_uav']:
                                    sol_inicial_data.append(c)
                        mejor_sol, mejor_costo = Hill_Climbing_alguna_mejora(sol_inicial_data, costo_inicial) #Envía los ids de los uavs resultados del greedy.
                        print('\n Mejor solución :',mejor_sol,' con costo: ',mejor_costo)
                case '3':
                    #MEJOR MEJORA DETERMINISTA
                    print('Falta')
                case '4':
                    #MEJOR MEJORA ESTOCÁSTICO
                    print('Falta')
        case '2':
            archivo = 't2_Europa.txt'
            print('Aplicar \n 1.- Hill Climbing Alguna-Mejora con Greedy Determinista'+
                  '\n 2.- Hill Climbing Alguna-Mejora con Greedy Estocástico \n 3.- Hill Climbing Mejor-Mejora con Greedy Determinista' +
                  '\n 4.- Hill Climbing Mejor-Mejora con Greedy Estocástico')
            choose2 = input()
            match choose2:
                case '1':
                    uavs = leer(archivo)
                    uavs_original = uavs.copy()
                    b, costo_inicial = gDeterminista(uavs)
                    sol_inicial_indexs = []
                    sol_inicial_data = []
                    for i in b:
                        sol_inicial_indexs.append(i['id_uav'])
                    for a in sol_inicial_indexs:
                        for c in uavs_original:
                            if a == c['id_uav']:
                                sol_inicial_data.append(c)
                    print(costo_inicial)
                    #print('Hola ', sol_inicial_data)
                    mejor_sol, mejor_costo = Hill_Climbing_alguna_mejora(sol_inicial_data, costo_inicial, max_iter = 100) #Envía los ids de los uavs resultados del greedy.
                    print('\n Mejor solución :',mejor_sol,' con costo: ',mejor_costo)
                case '2':
                    for d in range(5):
                        uavs = leer(archivo)
                        uavs_original = uavs.copy()
                        b,costo_inicial = gEstocastico(uavs)
                        print(b)
                        print(uavs_original)
                        sol_inicial_indexs = []
                        sol_inicial_data = []
                        for i in b:
                            sol_inicial_indexs.append(i['id_uav'])
                        for a in sol_inicial_indexs:
                            for c in uavs_original:
                                if a == c['id_uav']:
                                    sol_inicial_data.append(c)
                        mejor_sol, mejor_costo = Hill_Climbing_alguna_mejora(sol_inicial_data, costo_inicial) #Envía los ids de los uavs resultados del greedy.
                        print('\n Mejor solución :',mejor_sol,' con costo: ',mejor_costo)
                case '3':
                    #MEJOR MEJORA DETERMINISTA
                    print('Falta')
                case '4':
                    #MEJOR MEJORA ESTOCÁSTICO
                    print('Falta')
        case '3': #En este caso la mejor solución es el greedy determinista
            archivo = 't2_Titan.txt'
            print('Aplicar \n 1.- Hill Climbing Alguna-Mejora con Greedy Determinista'+
                  '\n 2.- Hill Climbing Alguna-Mejora con Greedy Estocástico \n 3.- Hill Climbing Mejor-Mejora con Greedy Determinista' +
                  '\n 4.- Hill Climbing Mejor-Mejora con Greedy Estocástico')
            choose2 = input()
            match choose2:
                case '1':
                    uavs = leer(archivo)
                    uavs_original = uavs.copy()
                    b, costo_inicial = gDeterminista(uavs)
                    sol_inicial_indexs = []
                    sol_inicial_data = []
                    for i in b:
                        sol_inicial_indexs.append(i['id_uav'])
                    for a in sol_inicial_indexs:
                        for c in uavs_original:
                            if a == c['id_uav']:
                                sol_inicial_data.append(c)
                    #print(costo_inicial)
                    #print('Hola ', sol_inicial_data)
                    mejor_sol, mejor_costo = Hill_Climbing_alguna_mejora(sol_inicial_data, costo_inicial, max_iter = 50) #Envía los ids de los uavs resultados del greedy.
                    print('\n Mejor solución :',mejor_sol,' con costo: ',mejor_costo)
                case '2':
                    for d in range(5):
                        uavs = leer(archivo)
                        uavs_original = uavs.copy()
                        b,costo_inicial = gEstocastico(uavs)
                        mejor_sol, mejor_costo = Hill_Climbing_alguna_mejora(b, costo_inicial,max_iter=1000) #Envía los ids de los uavs resultados del greedy.
                        print('\n Mejor solución :',mejor_sol,' con costo: ',mejor_costo)
                case '3':
                    #MEJOR MEJORA DETERMINISTA
                    print('Falta')
                case '4':
                    #MEJOR MEJORA ESTOCÁSTICO
                    print('Falta')
