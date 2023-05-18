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
    for index, uav in enumerate(neighbor):
        if index == 0: #Primer UAV en aterrizar asumiendo que cae en su tiempo preferente
            uav['tiempo_aterrizaje'] = uav['midTime']
            uav_ant = uav
        else:
            tiempo_aterrizaje = uav_ant['tiempo_aterrizaje'] + uav['times'][uav_ant['id_uav']-1]      #uav['midTime'] + uavs_orden[index-1]['times']
            if tiempo_aterrizaje <= uav['topTime'] and tiempo_aterrizaje >= uav['botTime']: #Los uavs no pueden caer mas allá del tiempo máximo de aterrizaje
                uav['tiempo_aterrizaje'] = tiempo_aterrizaje
                cost = cost + abs(tiempo_aterrizaje - uav['midTime'])
                
            elif tiempo_aterrizaje > uav['topTime'] or tiempo_aterrizaje < uav['botTime']:
                tiempo_aterrizaje =  abs(uav_ant['tiempo_aterrizaje'] + uav['times'][uav_ant['id_uav']-1] - uav['midTime'])
                uav['tiempo_aterrizaje'] = uav['botTime']
                cost = cost + tiempo_aterrizaje
            uav_ant = uav
    return cost, neighbor

def generate_neighbor(current_state, premium):
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

def generar_todos_los_vecinos(camino, premium):
    vecinos = []
    if premium == 0:
        for i in range(1,len(camino)):
            for j in range(i + 1, len(camino)):
                vecino = copy.deepcopy(camino)
                vecino[i], vecino[j] = vecino[j], vecino[i]
                vecinos.append(vecino)
    else:
        for i in range(len(camino)):
            for j in range(i + 1, len(camino)):
                vecino = copy.deepcopy(camino)
                vecino[i], vecino[j] = vecino[j], vecino[i]
                vecinos.append(vecino)
    return vecinos

def calcular_costo(camino):
    cost = 0
    uav_ant = None
    for index, uav in enumerate(camino):
        if index == 0:
            uav['tiempo_aterrizaje'] = uav['midTime']
            cost = cost + 0
            uav_ant = uav
        else:
            tiempo_aterrizaje = uav_ant['tiempo_aterrizaje'] + uav['times'][uav_ant['id_uav']-1]
            if tiempo_aterrizaje <= uav['topTime'] and tiempo_aterrizaje >= uav['botTime']:
                uav['tiempo_aterrizaje'] = tiempo_aterrizaje
                cost = cost + abs(tiempo_aterrizaje - uav['midTime'])
                uav_ant_id = uav['id_uav']
            else:
                tiempo_aterrizaje = abs(uav_ant['tiempo_aterrizaje'] + uav['times'][uav_ant['id_uav']-1] - uav['midTime'])
                uav['tiempo_aterrizaje'] = uav['botTime']
                cost = cost + tiempo_aterrizaje
            uav_ant = uav
    return cost, camino

def tabu_search(initial_solution, initial_cost, tabu_list_size, num_iterations):
    best_solution = copy.deepcopy(initial_solution)
    current_solution = copy.deepcopy(initial_solution)
    best_neighbor_score = initial_cost
    lista_tabu = []

    for i in range(num_iterations):
        neighbors = []
        for nei in current_solution: #SE LIMPIA AL IGUAL QUE EN LOS DEMÁS ALGORITMOS LA LISTA DE UAVS A ATERRIZAR PARA PODER REALIZAR EL CALCULO DE ATERRIZAJE Y COSTO DE FORMA CORRECTA
            if 'tiempo_aterrizaje' in nei:
                del nei['tiempo_aterrizaje']
        if current_solution[0]['botTime'] == 0 and current_solution[0]['midTime'] == 0 and current_solution[0]['topTime'] == 0: #CASO ESPECÍFICO QUE SE ESTÉ TRABAJANDO CON EL ARHCHIVO 2.
            neighbor = generate_neighbor(current_solution, 0)
        else: 
            neighbor = generate_neighbor(current_solution, 1)
        
        neighbour_score, best_neighbor = evaluate_state(neighbor)
        neighbors.append(neighbor)
        if neighbor not in lista_tabu:
            current_solution = neighbor
            if len(lista_tabu) > tabu_list_size:
                print('Se llenó ', lista_tabu.pop(0))
            lista_tabu.append(current_solution)
            break

        current_solution_score, best_neighbor = evaluate_state(current_solution)
        
        if current_solution_score < best_neighbor:
            best_solution = current_solution
            best_neighbor_score = current_solution_score
            
    return best_solution, best_neighbor_score

def generar_todos_los_vecinos(camino, premium, count_neighbor): 
    vecinos = []    #LISTA QUE ALMACENARÁ EL VECINDARIO DE UNA SOLUCIÓN.
    a = 0
    if premium == 0:    #EN CASO EXCEPCIONAL QUE SE ESTÉ TRABAJANDO CON EL ARCHIVO 2. YA QUE EN ESTE EL PRIMER UAV EMPIEZA EN EL TIEMPO 0.
        while a < count_neighbor:
            vecino = copy.deepcopy(camino)
            p = random.randint(0,len(camino)-1)
            k = random.randint(0,len(camino)-1)
            if p != k:
                vecino[p] , vecino[k] = vecino[k], vecino[p]
                vecinos.append(vecino)
                a = a + 1
    else:   #LO MISMO QUE EN EL IF, SOLO QUE ACÁ ES CUANDO SE ESTÉ TRABAJANDO CON OTROS ARCHIVOS QUE NO SEAN EL 2.
        while a < count_neighbor:
            vecino = copy.deepcopy(camino)
            p = random.randint(0,len(camino)-1)
            k = random.randint(0,len(camino)-1)
            if p != k:
                vecino[p] , vecino[k] = vecino[k], vecino[p]
                vecinos.append(vecino)
                a = a + 1
    return vecinos


def Tabu_Search(sol_inicial, costo_inicial, tabu_list_size, num_iterations, count_neighbors):
    lista_tabu = []
    best_neighbor = [sol_inicial]
    best_score = costo_inicial
    for nei in sol_inicial:
            if 'tiempo_aterriza' in nei:
                del nei['tiempo_aterrizaje']
    neighbor_actual = sol_inicial
    neighbor_score_actual = costo_inicial
    lista_tabu.append(neighbor_actual)
    a = 0
    while a <= num_iterations:
        if neighbor_actual[0]['botTime'] == 0 and neighbor_actual[0]['midTime'] == 0 and neighbor_actual[0]['topTime'] == 0:
            neighbor_actual = generate_neighbor(neighbor_actual,1)
            if neighbor_actual not in lista_tabu:
                neighbor_score_actual, neighbor_actual = evaluate_state(neighbor_actual)
                if len(lista_tabu) == tabu_list_size:
                    lista_tabu.pop()
                    break
            lista_tabu.append(neighbor_actual)
        else:
            for nei in neighbor_actual:
                if 'tiempo_aterriza' in nei:
                    del nei['tiempo_aterrizaje']
            vecinos = generar_todos_los_vecinos(neighbor_actual,0, count_neighbors)  #GENERACIÓN DE VECINOS
            for vecino in vecinos:
                if vecino not in lista_tabu:
                    print('No estoy')
                    neighbor_actual = vecino
                    neighbor_score_actual, neighbor_actual = evaluate_state(neighbor_actual)
                    if len(lista_tabu) == tabu_list_size:
                        lista_tabu.pop()
                    lista_tabu.append(neighbor_actual)
                    print(len(lista_tabu))
                    break
            if neighbor_score_actual < best_score: #Como se alguna-mejora, la primera solución que mejore la solución actual
                best_score = copy.deepcopy(neighbor_score_actual)
                best_neighbor.pop()
                best_neighbor.append(copy.deepcopy(neighbor_actual))
                print('\n Solución Mejor del Tabu encontrada con costo: ', best_score )
                print(best_neighbor)
            
        a = a + 1
    return best_neighbor, best_score

#MAIN DEL PROGRAMA.
if __name__ == '__main__':
    ar  = 't2_Europa.txt'
    uavs = leer(ar)
    caminoDeterminista, costoDeterminista = gDeterminista(uavs)
    print("Costo Determinista:",costoDeterminista)
    mejorCamino, mejorCosto = tabu_search(caminoDeterminista, costoDeterminista, tabu_list_size=100, num_iterations= 10000)# count_neighbors=100)
    print ("Mejor Costo:", mejorCosto) 
    #print('Mejor camino ', mejorCamino)