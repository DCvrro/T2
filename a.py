import random

def aleatorizar_array(array):
    n = len(array)
    for i in range(n - 1, 0, -7):
        print('i: ',i)
        j = random.randint(1, i)
        print('j: ',j)
        array[i], array[j] = array[j], array[i]

# Ejemplo de uso
mi_array = [6, 2, 11, 8, 15, 1, 7, 3, 12, 13, 5, 14, 10, 4, 9]
#aleatorizar_array(mi_array)
#print(mi_array)

def vecinas(array,mod):
    for i in range(len(array)):
        if i == mod:
            array[mod+1], array[mod+2] = array[mod+2], array[mod+1]
    print(array)

array = [1,2,3,4,5,6,7,8,9]

a = 0
b = a
while True :
    mod = random.randint(a,b)
    print(mod)
    vecinas(array,mod)
    a = a + 1
    b = a + 1
    