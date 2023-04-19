import sys,os
import numpy as np

import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network

def visualize(G):
    net = Network(height="1000px", notebook=True, cdn_resources="remote")
    net.from_nx(G)
    net.write_html("graph.html")

def generate_graph(n, graph_type):
    if (graph_type=="random"):
        G = random_graph(n)
    elif (graph_type=="ladder"):
        G = nx.generators.classic.ladder_graph(n)
    elif (graph_type=="complete"):
        G = nx.generators.classic.complete_graph(n)
    elif (graph_type=="balanced_multipartite"):
        G = nx.generators.classic.complete_multipartite_graph(n,n)
    elif (graph_type=="cycle"):
        G = nx.generators.classic.cycle_graph(n)
    else:
        print("Unsupported graph type {}.".format(graph_type))
        sys.exit()

    return G

def random_graph(n):
    G = nx.Graph()
    color_list = ["green","orange","blue","red","purple","cyan","black","brown","magenta"]
    adj_list = generate_adj_list(n)
    node_colors = random_node_colors(adj_list, color_list)

    for i in range(n):
        if (np.any(adj_list[i,:] > 0)):
            G.add_nodes_from([(str(i), {"color": node_colors[i]})])

        for j in range(i+1,n):
            if (adj_list[i,j] > 0):
                G.add_edge(str(i),str(j))
    return G

def generate_adj_list(n, prob_th=0.90):
    adj_list = np.zeros((n,n))

    for i in range(n):
        for j in range(i+1,n):
            rand = np.random.rand()
            if (rand > prob_th):
                adj_list[i,j] = 1.0
    return adj_list

def random_node_colors(adj_list, color_list):
    n = adj_list.shape[0]
    return np.random.choice(color_list, n, replace=True)

def n_plus_1_graph_coloring(adj_list, color_list):
    pass

def get_max_degree(G):
    degree_sequence = [ d for n, d in G.degree() ]
    degree_sequence = sorted(degree_sequence, reverse=True)
    return min(degree_sequence),max(degree_sequence)


# build graph
n=25
graph_type="random"
G = generate_graph(n, graph_type)

# compute degree
min_degree, max_degree = get_max_degree(G)
print("Minimum degree:", min_degree, "Maximum degree:", max_degree)

# visualize
visualize(G)
