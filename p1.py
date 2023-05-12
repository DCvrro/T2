

def leerArchivo(): 
    count = 0
    uavs = {}
    with open('t2_Deimos.txt','r+') as _file:
        file = _file.readlines()
        for linea in file:
            linea = linea.split(' ')
            if('\n' in linea[-1]):
                if(linea[-1] == '\n'): 
                    linea.pop()
                else:
                    linea[-1] = (linea[-1])[:-1]
            if count == 0:
                cant_uav = linea
                uavs['cant'] = cant_uav
                count = count + 1
            elif count == 1:
                bestTime = linea[0]  ## Mejor Timepo
                uavs['bestTime'] = bestTime

                prefTime = linea[1]
                uavs['prefTime'] = prefTime

                slowTime = linea[-1]
                uavs['slowTime'] = slowTime
                


        print(uavs)
leerArchivo()

## Cantidad UAVS

#1 UAVSi
## Mejor tiempo | tiempo preferente | mayor tiempro
## tiempos
