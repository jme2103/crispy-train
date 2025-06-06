import matplotlib.pyplot as plt
from gerrychain import (Partition, Graph, MarkovChain,
                        updaters, constraints, accept)
from gerrychain.proposals import recom
from gerrychain.constraints import contiguous
from functools import partial
import pandas

import sys


target_file = sys.argv[1]
output_file = sys.argv[2]

# Set the random seed so that the results are reproducible!
import random
random.seed(2024)

#graph = Graph.from_json("./gerrymandria.json")

#change file here
graph = Graph.from_json(target_file)
my_updaters = {
    "population": updaters.Tally("TOTPOP"),
    "cut_edges": updaters.cut_edges
}

initial_partition = Partition(
     graph,
     assignment="district",
     updaters=my_updaters
 )

# This should be 8 since each district has 1 person in it.
# Note that the key "population" corresponds to the population updater
# that we defined above and not with the population column in the json file.
from gerrychain.tree import bipartition_tree

ideal_population = sum(initial_partition["population"].values()) / len(initial_partition)
#problem with the above column???
#ideal population is the average population per district
#so is that the value that we check agaainst with the epsilon?
proposal = partial(
    recom,
    pop_col="TOTPOP",
    pop_target=ideal_population,
    #initial value
    epsilon=.20,
    #epsilon=10,
    node_repeats=10,
    method = partial(
        bipartition_tree,
        max_attempts=10,
        allow_pair_reselection=True  # <-- This is the only change
    )
)

recom_chain = MarkovChain(
    proposal=proposal,
    constraints=[contiguous],
    accept=accept.always_accept,
    initial_state=initial_partition,
    total_steps=1000
)

assignment_list = []

for i, item in enumerate(recom_chain):
    print(f"Finished step {i+1}/{len(recom_chain)}", end="\r")
    assignment_list.append(item.assignment)

import matplotlib.pyplot as plt
import matplotlib.cm as mcm
import networkx as nx
import winsound

assignment_list = []

try:
    for i, item in enumerate(recom_chain):
        print(f"Finished step {i+1}/{len(recom_chain)}", end="\r")
        assignment_list.append(item.assignment)
except Exception as e:
    print(f"\nError at step {i+1}: {e}")
    # draw the graph with the last valid assignment
    if assignment_list:
        last_assignment = assignment_list[-1]
        fig, ax = plt.subplots(figsize=(8,8))
        pos = {node: (data['x'], data['y']) for node, data in graph.nodes(data=True)}
        node_colors = [mcm.tab20(int(last_assignment[node]) % 20) for node in graph.nodes()]
        node_labels = {node: str(last_assignment[node]) for node in graph.nodes()}

        nx.draw_networkx_nodes(graph, pos, node_color=node_colors)
        nx.draw_networkx_edges(graph, pos)
        nx.draw_networkx_labels(graph, pos, labels=node_labels)
        plt.axis('off')
        plt.show()

#make sound when done
duration = 500  # milliseconds
freq = 440  # Hz
winsound.Beep(freq, duration)

import csv
import time

start_time = time.time()

with open(output_file, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["partition", "node", "district"])  # header

    for partition_num, assignment in enumerate(assignment_list):
        for node, district in assignment.items():
            writer.writerow([partition_num, node, district])

print("--- %s seconds ---" % (time.time() - start_time))