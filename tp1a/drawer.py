import sys
import fileinput
from sets import Set

import matplotlib.pyplot as plt
from matplotlib import rcParams
import pydot

requesters = {}
requesters_links = {}
requested = {}
repliers = {}
replied = {}

#
# File processing
#

for line in fileinput.input():
    hwsrc, psrc, pdst, op = line.split()
    if op == 'who-has':
        requesters[psrc] = requesters.get(psrc, 0.0) + 1.0

        if psrc not in requesters_links:
            requesters_links[psrc] = Set([pdst])
        else:
            requesters_links[psrc].add(pdst)
            
        requested[pdst] = requested.get(pdst, 0.0) + 1.0
    elif op == 'is-at':
        repliers[psrc] = repliers.get(psrc, 0.0) + 1.0
        replied[pdst] = replied.get(pdst, 0.0) + 1.0
#
# Drawings
#

# Graph

graph = pydot.Dot(graph_type='digraph')
nodes = {}

for psrc, pdsts in requesters_links.iteritems():
    if psrc not in nodes:
        nodes[psrc] = pydot.Node(psrc)
        graph.add_node(nodes[psrc])

    for pdst in pdsts:
        if pdst not in nodes:
            nodes[pdst] = pydot.Node(pdst)
            graph.add_node(nodes[pdst])

        edge = pydot.Edge(nodes[psrc], nodes[pdst])
        graph.add_edge(edge)

for psrc, n in requesters.iteritems():
    nodes[psrc].set_width(str(n/9.0))
    nodes[psrc].set_height(str(n/9.0))

graph.write_png('test.png')

# Bars

# Necessary in order to make labels fit
rcParams.update({'figure.autolayout': True})

def draw_IPs_barh(ips_dict, title, label):
    pos = range(len(ips_dict))
    plt.barh(pos, ips_dict.values(), align='center', alpha=0.4)
    plt.yticks(pos, ips_dict.keys())
    plt.xlabel(label)
    plt.title(title)

draw_IPs_barh(requesters, 'IPs que hicieron request', 'pedidos')
plt.savefig('requesters.png')
plt.clf()

draw_IPs_barh(requested, 'IPs por las que se hizo request', 'pedidos')
plt.savefig('requested.png')
plt.clf()

draw_IPs_barh(repliers, 'IPs que respondieron a un request', 'respuestas')
plt.savefig('repliers.png')
plt.clf()

draw_IPs_barh(replied, 'IPs a las que se les respondio un request',
    'respuestas')
plt.savefig('replied.png')
plt.clf()
