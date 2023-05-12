

def leerArchivo(): 
    count = 0
    numUAV = []
    uav = {}
    with open('t2_Titan.txt','r+') as _file:
        file = _file.readlines()
        print(file)
        for linea in file:
            linea = linea.split(' ')
            if('\n' in linea[-1]):
                if(linea[-1] == '\n'): 
                    linea.pop()
                else:
                    linea[-1] = (linea[-1])[:-1] ## corta los nuemeros o palabras con un \n
            if count == 0:
                cant_uav = linea[-1]
                uav['cant'] = cant_uav
                count = count + 1
                continue
            elif count == 1:
                print("entre")

        print(uav)
leerArchivo()

## Cantidad UAVS

#1 UAVSi
## Mejor tiempo | tiempo preferente | mayor tiempro
## tiempos
