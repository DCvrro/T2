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
    return uav_result

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
            else:
                tiempo_aterrizaje =  abs(uav_ant['tiempo_aterrizaje'] + uav['times'][uav_ant['id_uav']-1] - uav['midTime'])
                uav['tiempo_aterrizaje'] = uav['botTime']
                cost = cost + tiempo_aterrizaje
    return cost, neighbor

def generate_neighbors(current_state, premium):
    vecino = []
    if premium == 0:
        while True:
            p = random.randint(0,len(current_state)-1)
            k = random.randint(0,len(current_state)-1)
            if p != k:
                current_state[p] , current_state[k] = current_state[k], current_state[p]
                vecino.append(current_state)
                break
    else:
        while True:
            p = random.randint(1,14)
            k = random.randint(1,14)
            if p != k:
                current_state[p] , current_state[k] = current_state[k], current_state[p]
                vecino.append(current_state)
                break
    return current_state

def generar_vecindario_completo(current_state,premium,limite_vecinos, costo_actual):
    #obtengo una solucion inicial y genero todos los vecinos posibles para luego escoger el que posee menor costo.
    vecinos = []
    for nei in current_state:
        if 'tiempo_aterrizaje' in nei:
            del nei['tiempo_aterrizaje']
    menor_costo = costo_actual
    vecinos.append(current_state) #Guardar vecinos generados a partir de la solución que entra a la función
    count = 0 
    if premium == 0:
        while True:
            tmp = copy.deepcopy(current_state)
            i = random.randint(0,len(tmp)-1)
            j = random.randint(0,len(tmp)-1)
            if i != j:
                tmp[i], tmp[j] = tmp[j], tmp[i]
                sol,mejor_vecino  = evaluate_state(tmp)
                print(mejor_vecino, sol)
                if sol < menor_costo:
                    menor_costo = sol
                    vecinos.append(mejor_vecino)
            if count >= limite_vecinos and costo_actual >= menor_costo:
                break
            else:
                count = count + 1 
    else:
        while True:
            i = random.randint(1,len(current_state)-1)
            j = random.randint(1,len(current_state)-1)
            if i != j:
                current_state[i], current_state[j] = current_state[j], current_state[i]
                sol,mejor_vecino  = evaluate_state(current_state)
                if sol < menor_costo:
                    menor_costo = sol
                    vecinos.append(mejor_vecino)
            if count == limite_vecinos:
                break
            else:
                count = count + 1 

    print('Costo inicial: ', costo_inicial)
    #print('Solucion inicial: ', current_state)
    print('Costo del mejor vecino: ', menor_costo)
    print('Vecinos: ', vecinos)
    print(vecinos[-1] )
    return vecinos[-1] 

def Hill_Climbing_mejor_mejora(sol_inicial):
    #print("Current_State:", sol_inicial)

    costo, caminos = evaluate_state(sol_inicial)
    print("Costo", costo) 
    #generar_vecindario_completo(current_state,0,150)
    return 0 

#ahora haremos un hillclimbingiterativo, el cual se volverá a llamar en cada posicion que uno se encuentre.
def Hill_Climbing_iterativo(sol_inicial,nueva_solucion, costo_inicial,ubicacion_actual,revisados):
    size = len(sol_inicial) # veo por cuantos uavs debo pasar
    if(ubicacion_actual == len(sol_inicial)-1):
        return nueva_solucion
    else:
        nueva_solucion,revisados = mejoro_vecino(nueva_solucion,ubicacion_actual,revisados)
        Hill_Climbing_iterativo(sol_inicial,nueva_solucion,costo_inicial,ubicacion_actual+1,revisados)

def mejoro_vecino(nueva_solucion,ubicacion_actual,revisados):
    mejor_vecino = []
    if ubicacion_actual in revisados:
        return nueva_solucion,revisados


def Hill_Climbing_mejor_mejora(sol_inicial, costo_inicial):
    sol_inicial_aux = copy.deepcopy(sol_inicial)
    neighbor_ant = sol_inicial
    best_score = copy.deepcopy(costo_inicial)
    best_neighbor = [sol_inicial]
    for nei in neighbor_ant:
        if 'tiempo_aterrizaje' in nei:
            del nei['tiempo_aterrizaje']
    sol_inicial_aux_2 = copy.deepcopy(neighbor_ant)
    neighbor_actual = neighbor_ant
    neighbor_score_actual = costo_inicial
    a = 0
    b = 0
    igual_score = 0
    distinta = 0

    while a <= 10:
        for i in range(100):
            tmp = sol_inicial_aux_2
            #print(tmp)
            if neighbor_score_actual < best_score: #Como se alguna-mejora, la primera solución que mejore la solución actual
                best_score = copy.deepcopy(neighbor_score_actual)
                best_neighbor.pop()
                best_neighbor.append(copy.deepcopy(neighbor_actual))
                print('\n Solución Mejor del Alguna-Mejora encontrada con costo: ', best_score )
                print(best_neighbor)
                neighbor_ant = neighbor_actual
                neighbor_actual = None
                distinta = distinta + 1
                break 
            if tmp[0]['botTime'] == 0 and tmp[0]['midTime'] == 0 and tmp[0]['topTime'] == 0:
                neighbor_actual = generate_neighbors(tmp,1)
                neighbor_score_actual, neighbor_actual = evaluate_state(neighbor_actual)
            else:
                neighbor_actual = generate_neighbors(tmp,0)
                neighbor_score_actual, neighbor_actual = evaluate_state(neighbor_actual)
            print(neighbor_actual)
        #print(neighbor_actual, neighbor_score_actual)
        print(igual_score)
        a = a + 1
    if igual_score != 0 and distinta == 0:
        print('Sol inicial ya que ninguna fue mejor, pero otras daban lo mismo')
        #return sol_inicial_aux, costo_inicial
    else:
        print()

if __name__ == '__main__':
    print('Archivo a leer para aplicar HillClimbing en base al resultado del Greedy \n 1.- t2_Deimos.txt \n 2.- t2_Europa.txt \n 3.- t2_Titan.txt')
    choose = input()
    match choose:
        case '1': #En este caso encuentra una solución mejor a la pasada por el greedy determinista.
            archivo = 't2_Deimos.txt'
            uavs = leer(archivo)
            uavs_original = leer(archivo)
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
            Hill_Climbing_mejor_mejora(sol_inicial_data, costo_inicial) #Envía los ids de los uavs resultados del greedy.
            #print('\n Mejor solución :',mejor_sol,' con costo: ',mejor_costo)
        case '2': #En este caso la mejor solución es el greedy determinista
            archivo = 't2_Europa.txt'
            uavs = leer(archivo)
            uavs_original = leer(archivo)
            sol_inicial_data, costo_inicial = gDeterminista(uavs)
            print("Costo Determinista:", costo_inicial) 
            #print("Primera solucion:",sol_inicial_data)
            Hill_Climbing_mejor_mejora(sol_inicial_data,costo_inicial) #Envía los ids de los uavs resultados del greedy.
            #print('\n Mejor solución :',mejor_sol,' con costo: ',mejor_costo)

        case '3': #En este caso la mejor solución es el greedy determinista
            archivo = 't2_Titan.txt'
            uavs = leer(archivo)
            uavs_original = leer(archivo)
            sol_inicial_data, costo_inicial = gDeterminista(uavs)
            print("Costo Determinista:", costo_inicial) 
            #print("Primera solucion:",sol_inicial_data)
            mejor_sol, mejor_costo = Hill_Climbing_mejor_mejora(sol_inicial_data,costo_inicial) #Envía los ids de los uavs resultados del greedy.
            #print('\n Mejor solución :',mejor_sol,' con costo: ',mejor_costo)
