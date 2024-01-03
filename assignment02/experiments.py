import time
import json
import sys
import jsonlines
import matplotlib.pyplot as plt

from graph_loaders import *
from algorithm_randomized_v2 import randomized_search_independent_set

def run(graphs, algo, runs=1):
    for graph_id in sorted(graphs.keys()):
        results = {
            "times": [],
            "operation_counts": [],
            "set_sizes": [],
            "combinations_tested": [],
            "stop_conditions": []
        }

        with jsonlines.open('results_' + sys.argv[2] + '.jsonl', 'a') as file:
            for i in range(runs):
                print(f"Running {graph_id}, run {i}")

                start_time = time.perf_counter()
                max_set, count, combinations, stop_condition = algo(graphs[graph_id], max_iterations=100000, max_time_seconds=600)
                end_time = time.perf_counter()
                total_time = end_time - start_time

                results["times"].append(total_time)
                results["operation_counts"].append(count)
                results["set_sizes"].append(len(max_set))
                results["combinations_tested"].append(combinations)
                results["stop_conditions"].append(stop_condition)

            file.write({graph_id: results})

if __name__ == "__main__":
    # cli arg parsing
    if sys.argv[1] not in ['run', 'plot']:
        print("Usage: python3 experiments.py [run | plot]")
        sys.exit(1)


    # run mode
    if sys.argv[1] == 'run':
        # cli arg parsing
        if len(sys.argv) != 3 or sys.argv[2] not in ['twitter', 'twitch', 'wikipedia', 'batch']:
            print("Usage: run_experiments.py run [twitter | twitch | wikipedia | batch]")
            sys.exit(1)
    

        print(f"Loading graphs...")
        if sys.argv[2] == 'batch': graphs = load_graphs('graphs/graphs')
        elif sys.argv[2] == 'twitter': graphs = load_graphs('graphs/twitter')
        elif sys.argv[2] == 'twitch': graphs = load_twitch_graphs('graphs/twitch')
        elif sys.argv[2] == 'wikipedia': graphs = load_wiki_graphs('graphs/wikipedia')
        print("Done.")

        print("Running...")
        with open('results_' + sys.argv[2] + '.jsonl', 'w') as file:
            pass
        run(graphs, randomized_search_independent_set)
        print("Done.")


    # plot mode
    elif sys.argv[1] == 'plot':
        # cli arg parsing
        if len(sys.argv) != 3 or sys.argv[2] not in ['twitter', 'twitch', 'wikipedia', 'batch']:
            print("Usage: run_experiments.py plot [twitter | twitch | wikipedia | batch]")
            sys.exit(1)


        if sys.argv[2] == 'batch':
            raw_results = {}
            with jsonlines.open('results_batch.jsonl', 'r') as file:
                for line in file:
                    raw_results.update(line)
            
            results = {}
            edge_percents = set()
            for graph_id in raw_results.keys():
                vertices, edge_percent = graph_id.split('_')
                edge_percents.add(edge_percent)
                vertices = int(vertices)
                if vertices not in results.keys():
                    results[vertices] = {}
                results[vertices][edge_percent] = raw_results[graph_id]

            randomized_vertices = sorted(results.keys(), key=lambda x: int(x))

            randomized_times = {}
            for key in edge_percents:
                randomized_times[key] = [results[v][key]['times'] for v in randomized_vertices]
            for key in randomized_times.keys():
                randomized_times[key] = [sum(x)/len(x) for x in randomized_times[key]]
            plt.figure(figsize=(10, 5))
            for key in randomized_times.keys():
                plt.plot(randomized_vertices, randomized_times[key], label='0.' + key + ' edge ratio')
            plt.xlabel('Number of vertices')
            plt.ylabel('Time Taken (seconds)')
            plt.title('Time Taken for Randomized Search')
            plt.legend()
            plt.grid(True)
            plt.show()

            randomized_counts = {}
            for key in edge_percents:
                randomized_counts[key] = [results[v][key]['operation_counts'] for v in randomized_vertices]
            for key in randomized_counts.keys():
                randomized_counts[key] = [sum(x)/len(x) for x in randomized_counts[key]]
            plt.figure(figsize=(10, 5))
            for key in randomized_counts.keys():
                plt.plot(randomized_vertices, randomized_counts[key], label='0.' + key + ' edge ratio')
            plt.xlabel('Number of vertices')
            plt.ylabel('Operation Count')
            plt.title('Operation Count for Randomized Search')
            plt.legend()
            plt.grid(True)
            plt.show()

            randomized_combinations = {}
            for key in edge_percents:
                randomized_combinations[key] = [results[v][key]['combinations_tested'] for v in randomized_vertices]
            for key in randomized_combinations.keys():
                randomized_combinations[key] = [sum(x)/len(x) for x in randomized_combinations[key]]
            plt.figure(figsize=(10, 5))
            for key in randomized_combinations.keys():
                plt.plot(randomized_vertices, randomized_combinations[key], label='0.' + key + ' edge ratio')
            plt.xlabel('Number of vertices')
            plt.ylabel('Combinations')
            plt.title('Combinations Tested for Randomized Search')
            plt.legend()
            plt.grid(True)
            plt.show()

            randomized_set_sizes = {}
            for key in edge_percents:
                randomized_set_sizes[key] = [max(results[v][key]['set_sizes']) for v in randomized_vertices]
            plt.figure(figsize=(10, 5))
            colors = ['purple', 'blue', 'green', 'red']
            for idx, (key, values) in enumerate(randomized_set_sizes.items()):
                for x, y_list in zip(randomized_vertices, values):
                    plt.scatter(x, y_list, color=colors[idx], label='0.' + key if x == randomized_vertices[0] else "")
            plt.xlabel('Number of vertices')
            plt.ylabel('Set Size')
            plt.title('Set Size for Randomized Search')
            plt.legend(title='Edge ratios')
            plt.grid(True)
            plt.show()