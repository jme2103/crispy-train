import numpy as np #type:ignore
import pandas as pd #type:ignore
import json
import sys
import networkx as nx #type:ignore
from gerrychain import Graph #type:ignore
import networkx as nx #type:ignore

#method to add adjacent nodes to graph
def add_adjacent(num, graph, size):
    #north
    if not num < size:
        graph.add_edge(num, num - size)
    #south
    if not num >= size * size - size:
        graph.add_edge(num, num + size)
    #east
    if not (num + 1) % size == 0:
        graph.add_edge(num, num + 1)
    #west
    if not num % size == 0:
        graph.add_edge(num, num - 1)

# command line arguments
#file to be worked on from
target_filename = sys.argv[1]
#new file to be created, name plus json
new_filename = sys.argv[2] + ".json"
# size of the grid
size = int(sys.argv[3])

# read the CSV file into a DataFrame
#only need the total population column
df = pd.read_csv(target_filename, usecols=["Total"])

#iterate over the DataFrame to create nodes
G = Graph()
for i in range(size * size):
    #add node to graph
    G.add_node(i, district=str(i % size), TOTPOP=df["Total"][i], x=i % size, y=int(np.floor(i / size)))


#add adjacent nodes to graph
for i in range(size * size):    
    add_adjacent(i, G, size)


graph_string = nx.adjacency_data(G)

#output the graph to a JSON file
with open(new_filename, "w") as outfile:
    json.dump(graph_string, outfile, indent=3, sort_keys=False)