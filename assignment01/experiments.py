import time
import signal

import os
import json
import sys

import networkx as nx
import matplotlib.pyplot as plt

from algorithm_exhaustive import exhaustive_search_independent_set
from algorithm_greedy import greedy_heuristic_independent_set

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
        
        graph_id = str.replace(filename, '.json', '').replace('graph_', '')
        graphs[graph_id] = G

    print(sorted(graphs.keys())[1], '-', sorted(graphs.keys())[-1])

    return graphs

def run(graphs, algo, runs=1, timeout=60):
    results = {}

    def handler(signum, frame):
        raise TimeoutError("Timed out!")

    signal.signal(signal.SIGALRM, handler)

    for graph_id in sorted(graphs.keys()):
        results[graph_id] = {
            "times": [],
            "operation_count": -1,
            "set_size": -1
        }

        try:
            for i in range(runs):
                print(f"Running {graph_id}, {i}")
                signal.alarm(timeout)
                start_time = time.perf_counter()
                max_set, count = algo(graphs[graph_id])
                end_time = time.perf_counter()
                signal.alarm(0)

                total_time = end_time - start_time
                results[graph_id]["times"].append(total_time)
                results[graph_id]["operation_count"] = count
                results[graph_id]["set_size"] = len(max_set)
        except TimeoutError as e:
            print(f"Timed out on graph {graph_id}")
            break

    return results

if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in ['run', 'plot']: 
        print("Usage: run_experiments.py [run | plot]")
        sys.exit(1)
    
    if sys.argv[1] == 'run':
        graphs = load_graphs('graphs')
        graphs = {graph_id: graphs[graph_id] for graph_id in sorted(graphs.keys())}
        
        results = {'exhaustive': {}, 'greedy': {}}

        # exhaustive_results = run(graphs, exhaustive_search_independent_set, runs=1, timeout=60)
        # for graph_id in exhaustive_results.keys():
        #     if len(exhaustive_results[graph_id]["times"]) != 0:
        #         exhaustive_results[graph_id]["avg_time"] = sum(exhaustive_results[graph_id]["times"]) / len(exhaustive_results[graph_id]["times"])
        # for graph_id in exhaustive_results.keys():
        #     vertices, edge_percent = map(int, graph_id.split('_'))
        #     if vertices not in results['exhaustive']:
        #         results['exhaustive'][vertices] = {}
        #     if edge_percent not in results['exhaustive'][vertices]:
        #         results['exhaustive'][vertices][edge_percent] = {}
        #     results['exhaustive'][vertices][edge_percent] = exhaustive_results[graph_id]
        
        greedy_results = run(graphs, greedy_heuristic_independent_set, runs=1, timeout=60)
        for graph_id in greedy_results.keys():
            if len(greedy_results[graph_id]["times"]) != 0:
                greedy_results[graph_id]["avg_time"] = sum(greedy_results[graph_id]["times"]) / len(greedy_results[graph_id]["times"])
        for graph_id in greedy_results.keys():
            vertices, edge_percent = map(int, graph_id.split('_'))
            if vertices not in results['greedy']:
                results['greedy'][vertices] = {}
            if edge_percent not in results['greedy'][vertices]:
                results['greedy'][vertices][edge_percent] = {}
            results['greedy'][vertices][edge_percent] = greedy_results[graph_id]

        # write results to file in json
        with open('results_exhaustive.json', 'w') as file:
            json.dump(results['exhaustive'], file, indent=4)

        # write results to file in json
        with open('results_greedy.json', 'w') as file:
            json.dump(results['greedy'], file, indent=4)


    elif sys.argv[1] == 'plot':
        exhaustive_results = {}
        greedy_results = {}
        with open('results_exhaustive.json', 'r') as file:
            exhaustive_results = json.load(file)
        with open('results_greedy.json', 'r') as file:
            greedy_results = json.load(file)


        exhaustive_vertices = sorted(list(exhaustive_results.keys()), key=int)
        exhaustive_times_125 = [exhaustive_results[v]["12"]['avg_time'] for v in exhaustive_vertices]
        exhaustive_times_25 = [exhaustive_results[v]["25"]['avg_time'] for v in exhaustive_vertices]
        exhaustive_times_50 = [exhaustive_results[v]["50"]['avg_time'] for v in exhaustive_vertices]
        exhaustive_times_75 = [exhaustive_results[v]["75"]['avg_time'] for v in exhaustive_vertices]

        plt.figure(figsize=(10, 5))
        plt.plot(exhaustive_vertices, exhaustive_times_125, label='0.125 edge ration')
        plt.plot(exhaustive_vertices, exhaustive_times_25, label='0.25 edge ration')
        plt.plot(exhaustive_vertices, exhaustive_times_50, label='0.5 edge ration')
        plt.plot(exhaustive_vertices, exhaustive_times_75, label='0.75 edge ration')
        plt.xlabel('Number of vertices')
        plt.ylabel('Time Taken (seconds) (log)')
        plt.yscale('log')
        plt.title('Time Taken for Exhaustive Search')
        plt.legend()
        plt.grid(True)
        plt.show()

        exhaustive_count_125 = [exhaustive_results[v]["12"]['operation_count'] for v in exhaustive_vertices]
        exhaustive_count_25 = [exhaustive_results[v]["25"]['operation_count'] for v in exhaustive_vertices]
        exhaustive_count_50 = [exhaustive_results[v]["50"]['operation_count'] for v in exhaustive_vertices]
        exhaustive_count_75 = [exhaustive_results[v]["75"]['operation_count'] for v in exhaustive_vertices]

        plt.figure(figsize=(10, 5))
        plt.plot(exhaustive_vertices, exhaustive_count_125, label='0.125 edge ration')
        plt.plot(exhaustive_vertices, exhaustive_count_25, label='0.25 edge ration')
        plt.plot(exhaustive_vertices, exhaustive_count_50, label='0.5 edge ration')
        plt.plot(exhaustive_vertices, exhaustive_count_75, label='0.75 edge ration')
        plt.xlabel('Number of vertices')
        plt.ylabel('Operation Count (log)')
        plt.yscale('log')
        plt.title('Operation Count for Exhaustive Search')
        plt.legend()
        plt.grid(True)
        plt.show()

        exhaustive_combinations_125 = [pow(2, int(v)) for v in exhaustive_vertices]
        exhaustive_combinations_25 = [pow(2, int(v)) for v in exhaustive_vertices]
        exhaustive_combinations_50 = [pow(2, int(v)) for v in exhaustive_vertices]
        exhaustive_combinations_75 = [pow(2, int(v)) for v in exhaustive_vertices]

        plt.figure(figsize=(10, 5))
        plt.plot(exhaustive_vertices, exhaustive_combinations_125, label='0.125 edge ration')
        plt.plot(exhaustive_vertices, exhaustive_combinations_25, label='0.25 edge ration')
        plt.plot(exhaustive_vertices, exhaustive_combinations_50, label='0.5 edge ration')
        plt.plot(exhaustive_vertices, exhaustive_combinations_75, label='0.75 edge ration')
        plt.xlabel('Number of vertices')
        plt.ylabel('Combinations (log)')
        plt.yscale('log')
        plt.title('Exhaustive Combinations for Exhaustive Search')
        plt.legend()
        plt.grid(True)
        plt.show()

        # set sizes (scatter plot with colors on labels)
        exhaustive_set_sizes_125 = [exhaustive_results[v]["12"]['set_size'] for v in exhaustive_vertices]
        exhaustive_set_sizes_25 = [exhaustive_results[v]["25"]['set_size'] for v in exhaustive_vertices]
        exhaustive_set_sizes_50 = [exhaustive_results[v]["50"]['set_size'] for v in exhaustive_vertices]
        exhaustive_set_sizes_75 = [exhaustive_results[v]["75"]['set_size'] for v in exhaustive_vertices]

        # Scatter plot for Exhaustive Search
        plt.figure(figsize=(10, 5))
        plt.scatter(exhaustive_vertices, exhaustive_set_sizes_125, c='red', label='0.125 edge ratio')
        plt.scatter(exhaustive_vertices, exhaustive_set_sizes_25, c='blue', label='0.25 edge ratio')
        plt.scatter(exhaustive_vertices, exhaustive_set_sizes_50, c='green', label='0.5 edge ratio')
        plt.scatter(exhaustive_vertices, exhaustive_set_sizes_75, c='orange', label='0.75 edge ratio')
        plt.xlabel('Number of vertices')
        plt.ylabel('Set Size')
        plt.title('Set Size for Exhaustive Search')
        plt.legend()
        plt.grid(True)
        plt.show()


        greedy_vertices = sorted(list(greedy_results.keys()), key=int)[0:-5]
        greedy_times_125 = [greedy_results[v]["12"]['avg_time'] for v in greedy_vertices]
        greedy_times_25 = [greedy_results[v]["25"]['avg_time'] for v in greedy_vertices]
        greedy_times_50 = [greedy_results[v]["50"]['avg_time'] for v in greedy_vertices]
        greedy_times_75 = [greedy_results[v]["75"]['avg_time'] for v in greedy_vertices]

        plt.figure(figsize=(10, 5))
        plt.plot(greedy_vertices, greedy_times_125, label='0.125 edge ratio')
        plt.plot(greedy_vertices, greedy_times_25, label='0.25 edge ration')
        plt.plot(greedy_vertices, greedy_times_50, label='0.5 edge ration')
        plt.plot(greedy_vertices, greedy_times_75, label='0.75 edge ration')
        plt.xlabel('Number of vertices')
        plt.xticks(range(-4, len(greedy_vertices), 10))
        plt.ylabel('Time Taken (seconds)')
        plt.title('Time Taken for Greedy Search')
        plt.legend()
        plt.grid(True)
        plt.show()

        greedy_count_125 = [greedy_results[v]["12"]['operation_count'] for v in greedy_vertices]
        greedy_count_25 = [greedy_results[v]["25"]['operation_count'] for v in greedy_vertices]
        greedy_count_50 = [greedy_results[v]["50"]['operation_count'] for v in greedy_vertices]
        greedy_count_75 = [greedy_results[v]["75"]['operation_count'] for v in greedy_vertices]

        plt.figure(figsize=(10, 5))
        plt.plot(greedy_vertices, greedy_count_125, label='0.125 edge ration')
        plt.plot(greedy_vertices, greedy_count_25, label='0.25 edge ration')
        plt.plot(greedy_vertices, greedy_count_50, label='0.5 edge ration')
        plt.plot(greedy_vertices, greedy_count_75, label='0.75 edge ration')
        plt.xlabel('Number of vertices')
        plt.xticks(range(-4, len(greedy_vertices), 10))
        plt.ylabel('Operation Count')
        plt.title('Operation Count for Greedy Search')
        plt.legend()
        plt.grid(True)
        plt.show()
        
        set_size_differences = {v: {ep: exhaustive_results[v][ep]['set_size'] - greedy_results[v][ep]['set_size'] for ep in exhaustive_results[v].keys()} for v in exhaustive_results.keys()}
        
        plt.figure(figsize=(10, 5))
        plt.bar(set_size_differences.keys(), [set_size_differences[v]["12"] for v in set_size_differences.keys()], label='0.125 edge ration')
        plt.bar(set_size_differences.keys(), [set_size_differences[v]["25"] for v in set_size_differences.keys()], label='0.25 edge ration')
        plt.bar(set_size_differences.keys(), [set_size_differences[v]["50"] for v in set_size_differences.keys()], label='0.5 edge ration')
        plt.bar(set_size_differences.keys(), [set_size_differences[v]["75"] for v in set_size_differences.keys()], label='0.75 edge ration')
        plt.xlabel('Graph ID')
        plt.ylabel('Set Size Difference')
        plt.title('Greedy Search Misses')
        plt.legend()
        plt.show()

        greedy_set_size = {}
        for key in ["12", "25", "50", "75"]:
            greedy_set_size[key] = [greedy_results[v][key]['set_size'] for v in greedy_vertices]
        plt.figure(figsize=(10, 5))
        colors = ['red', 'blue', 'green', 'purple']
        for idx, (key, values) in enumerate(greedy_set_size.items()):
            for x, y_list in zip(greedy_vertices, values):
                plt.scatter(x, y_list, color=colors[idx], label='0.' + key if x == greedy_vertices[0] else "")

        plt.xlabel('Number of vertices')
        plt.ylabel('Set Size')
        plt.title('Set Size for Randomized Search')
        plt.legend(title='Edge ratios')
        plt.grid(True)
        plt.show()