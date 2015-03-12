from file_handler import Enum, readfile, writesoluce
from capacity import getMinCapacity
import pickle

(datacenter, servers, nbgroups) = readfile("input.txt")

# first fit

fitServers = sorted(servers, key=lambda x: (float)(x['size']) / (float)(x['capacity']))

pickle.dump(fitServers, open("tamere", "w"))
pickle.dump(servers, open("tasoeur", "w"))

for (index, server) in enumerate(fitServers):
    match = False
    location = (-1, -1)
    fitDatacenter = sorted(enumerate(datacenter), key=lambda x: sum(1 for i in x[1] if i == Enum.EMPTY))
    for (x, row) in fitDatacenter:
        for (y, space) in enumerate(row):
            if space == Enum.EMPTY:
                match = True
                for j in range(server['size']):
                    if y + j < len(row):
                        if row[y + j] != Enum.EMPTY:
                            match = False
                    else:
                        match = False
                if match:
                    location = (x, y)
                    break
        if match:
            break
    if match:
        servers[server['id']]['used'] = True
        servers[server['id']]['pos'] = location
        for i in range(server['size']):
            datacenter[location[0]][location[1] + i] = server['id']

# groups repartition

sortedServers = sorted(servers, key=lambda x: x['capacity'])

groups = list(0 for i in range(nbgroups))

for row in datacenter:
    for id in set(row):
        if id != Enum.EMPTY and id != Enum.UNUSED:
            _, groupIndex = getMinCapacity(datacenter, servers, nbgroups)
            groups[groupIndex] += servers[id]['capacity']
            servers[id]['group'] = groupIndex

writesoluce("output.txt", servers)

print getMinCapacity(datacenter, servers, nbgroups)
