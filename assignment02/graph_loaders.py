import os
import json
import networkx as nx

def load_graphs(graphs_folder):
    graphs = {}

    for filename in os.listdir(graphs_folder):
        if filename.endswith('.json'):
            
            filepath = os.path.join(graphs_folder, filename)
            with open(filepath, 'r') as file:
                adjacency_list = json.load(file)
                G = nx.Graph()

                for node, neighbors in adjacency_list.items():
                    node = tuple(map(int, node.strip('()').split(', ')))
                    G.add_node(node)
                
                    for neighbor in neighbors:
                        neighbor = tuple(map(int, neighbor.strip('()').split(', ')))
                        G.add_edge(node, neighbor)
        elif filename.endswith('.txt'):
            pass
        
        graph_id = str.replace(filename, '.json', '').replace('graph_', '')
        graphs[graph_id] = G

    return graphs

def load_wiki_graphs(graphs_folder):
    graphs = {}

    for filename in os.listdir(graphs_folder):
        if filename.endswith('.txt'):
            filepath = os.path.join(graphs_folder, filename)
            G = nx.Graph()

            with open(filepath, 'r') as file:
                for line in file:
                    if line.startswith('#'):
                        continue
                    v1, v2 = line.strip().split()
                    G.add_edge(int(v1), int(v2))

            graph_id = filename.replace('.txt', '')
            graph_id = str(len(G.nodes())) + '_' + str(len(G.edges()))
            graphs[graph_id] = G

    return graphs

def load_twitch_graphs(graphs_folder):
    graphs = {}

    for filename in os.listdir(graphs_folder):
        folder_path = os.path.join(graphs_folder, filename)
        if os.path.isdir(folder_path):
            for graph_file in os.listdir(folder_path):
                if graph_file.endswith('edges.csv'):
                    filepath = os.path.join(folder_path, graph_file)
                    print("Loading", filepath)
                    G = nx.Graph()

                    with open(filepath, 'r') as file:
                        for line in file:
                            if line.startswith("from"):
                                continue
                            v1, v2 = line.strip().split(',')
                            G.add_edge(int(v1), int(v2))

                    graph_id = graph_file.replace('musae_', '').replace('_edges.csv', '')
                    graph_id += "_" + str(len(G.nodes())) + '_' + str(len(G.edges()))
                    graphs[graph_id] = G

    return graphs
