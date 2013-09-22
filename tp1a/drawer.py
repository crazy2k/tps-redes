import sys
import fileinput

import matplotlib.pyplot as plt
from matplotlib import rcParams

requesters = {}
requested = {}
repliers = {}
replied = {}

# File processing

for line in fileinput.input():
    hwsrc, psrc, pdst, op = line.split()
    if op == 'who-has':
        requesters[psrc] = requesters.get(psrc, 0.0) + 1.0
        requested[pdst] = requested.get(pdst, 0.0) + 1.0
    elif op == 'is-at':
        repliers[psrc] = repliers.get(psrc, 0.0) + 1.0
        replied[pdst] = replied.get(pdst, 0.0) + 1.0
            
# Drawings

# Necessary in order to make labels fit
rcParams.update({'figure.autolayout': True})

def draw_IPs_barh(ips_dict, title, label):
    pos = range(len(ips_dict))
    plt.barh(pos, ips_dict.values(), align='center', alpha=0.4)
    plt.yticks(pos, ips_dict.keys())
    plt.xlabel(label)
    plt.title(title)

draw_IPs_barh(requesters, 'IPs que hicieron request', 'pedidos')

plt.show()
