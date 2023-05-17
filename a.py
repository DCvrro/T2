import random

a = [{'id_uav': 3}, {'id_uav': 4}, {'id_uav': 15}, {'id_uav': 6}, {'id_uav': 10}, {'id_uav': 14}, {'id_uav': 2}, {'id_uav': 12}, {'id_uav': 11}, {'id_uav': 5}, {'id_uav': 13}, {'id_uav': 1}, {'id_uav': 8}, {'id_uav': 7}, {'id_uav': 9}]

r = list()
n = len(a)

r.append(a.copy())
while True:
    p = random.randint(0,14)
    k = random.randint(0,14)
    if p != k:
        print(p)
        print(k)
        print(r)
        a[p] , a[k] = a[k], a[p]
        if a not in r:
            r.append(a.copy())
        else:
            print('Está dentro ',a, ' de ', r)
            print(r.remove(a))
            break
print(r)
print(len(r))