import networkx as nx
import random

def generate_random_solution(graph, min_size, max_size):
    """Generate a random subset of vertices as a candidate solution, with a minimum size constraint."""
    return set(random.sample(graph.nodes(), random.randint(min_size, max_size)))

def is_independent_set(graph, subset, operation_count):
    """ Check if the given subset of nodes forms an independent set in the graph. """
    checked = set()
    for u in subset:
        operation_count += len(checked)  # Increment operation count less frequently
        for v in graph.neighbors(u):
            if v in subset and v not in checked:
                return False, operation_count
        checked.add(u)
    return True, operation_count

def randomized_search_independent_set(graph, max_iterations=10000):
    tested_solutions = set()
    best_solution = set()
    best_score = 0
    operation_count = 0  # Initialize operation counter

    for _ in range(max_iterations):
        candidate = generate_random_solution(graph, min_size=best_score, max_size=len(graph))
        candidate_frozen = frozenset(candidate)  # to store in a set
        operation_count += 1  # Counting the add operation

        if candidate_frozen not in tested_solutions:
            operation_count += 1  # Counting the 'not in' operation
            tested_solutions.add(candidate_frozen)
            
            is_independent, operation_count = is_independent_set(graph, candidate, operation_count)
            if is_independent:
                score = len(candidate)
                operation_count += 1  # Counting the len operation

                if score > best_score:
                    best_solution = candidate
                    best_score = score
                    print(best_score)
                    operation_count += 2  # Counting the score comparison and assignment operations

    return best_solution, operation_count, len(tested_solutions)
