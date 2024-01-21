import matplotlib.pyplot as plt
import numpy as np
import json
import math

with open('dataset.json', 'r') as json_file:
    dataset = json.load(json_file)

mass_list = []
# 0 index: rock, 1 index: crystal, 2 index: metal
type_list = []
for dictionary in dataset:
    mass_list.append(dictionary['mass'])
    type_list.append(dictionary['type'])
    # match t:
    #     case 'rock':
    #         type_list[0] += 1
    #     case 'crystal':
    #         type_list[1] += 1
    #     case 'metal':
    #         type_list[2] += 1

x1 = np.array(type_list)
x = np.array(mass_list)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
b = int(math.log(len(x)))
n, bn, _ =ax1.hist(x,log=True , bins=b)
ax1.set_xlabel("mass")
ax1.set_ylabel("quantity")
print(b, n, bn)


ax2.hist(x1, bins=3)

plt.show()
