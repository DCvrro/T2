def leer():
    uav = {}
    with open('t2_Titan.txt','r+') as file:
        count = 0
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

        print(uav) 
        
leer() 