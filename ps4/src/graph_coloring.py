import sys,os
import numpy as np

import networkx as nx
import networkx.classes.function as nxf
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
    adj_list = generate_adj_list(n)

    for i in range(n):
        for j in range(i+1,n):
            if (adj_list[i,j] > 0):
                G.add_node(i)
                G.add_node(j)
                G.add_edge(i,j)
    return G

def generate_adj_list(n, prob_th=0.80):
    adj_list = np.zeros((n,n))

    for i in range(n):
        for j in range(i+1,n):
            rand = np.random.rand()
            if (rand > prob_th):
                adj_list[i,j] = 1.0
    return adj_list

def random_node_coloring(G, color_list):
    nodes = G.nodes()
    for node in nodes:
        color = np.random.choice(color_list, 1)[0]
        nx.set_node_attributes(G, {node: color}, name="color")

def n_plus_1_coloring(G, color_list):
    print("Coloring graph with {} colors".format(color_list))
    nodes = G.nodes()
    
    # get highest degree node
    max_d = 0
    start_node = ""
    for node,d in G.degree:
        if d > max_d:
            max_d = d
            start_node = node

    node_queue = [start_node]

    while(len(node_queue) > 0):
        # get next node to color
        curr_node = node_queue.pop(0)
        neighbors = nxf.neighbors(G,curr_node)
        node_colors = nx.get_node_attributes(G, "color")

        # check neighbors for coloring
        neighbor_colors = set()
        for n in neighbors:
            try:
                neighbor_colors.append(node_colors[n])
            except:
                node_queue.append(n)

        # select node coloring from color_list without using any neighbor_colors




        
        #nx.set_node_attributes(G, {node: color}, name="color")

def get_degree(G):
    degree_sequence = [ d for n, d in G.degree() ]
    degree_sequence = sorted(degree_sequence, reverse=True)
    return min(degree_sequence),max(degree_sequence)


# build graph
n=10
color_list = ["green","orange","blue","red","purple","cyan","black","brown","magenta"]
graph_type="random"
G = generate_graph(n, graph_type)

# compute degree
min_degree, max_degree = get_degree(G)
print("Minimum degree:", min_degree, "Maximum degree:", max_degree)

# color graph
#random_node_coloring(G, color_list)
n_plus_1_coloring(G, set(color_list[:max_degree+1]))

# visualize
visualize(G)
