import random

a = [{'id_uav': 3}, {'id_uav': 4}, {'id_uav': 15}, {'id_uav': 6}, {'id_uav': 10}, {'id_uav': 14}, {'id_uav': 2}, {'id_uav': 12}, {'id_uav': 11}, {'id_uav': 5}, {'id_uav': 13}, {'id_uav': 1}, {'id_uav': 8}, {'id_uav': 7}, {'id_uav': 9}]

r = []
n = len(a)

p = random.randint(1,15)
k = random.randint(1,15)

for i in range(1,15,5):
    if i == p-1:
        a[i], a[j] = a[j], a[i]
