import random
import time

def generate_random_solution(graph, min_size, max_size, operation_count):
    # Calculate weights (e.g., inversely proportional to degree)
    weights = {}
    for node in graph.nodes():
        operation_count += 1  # Accessing node in graph
        degree = graph.degree(node)
        operation_count += 1  # Calling graph.degree(node)
        if degree > 0:
            operation_count += 2  # Comparison and division
            weights[node] = 1 / degree
        else:
            operation_count += 1  # Assignment operation
            weights[node] = 1
        operation_count += 1  # Assignment of the weight

    # Normalize weights
    total_weight = sum(weights.values())
    operation_count += len(weights)  # Sum operation

    normalized_weights = {}
    for node, weight in weights.items():
        operation_count += 3  # Accessing node and weight, and division operation
        normalized_weights[node] = weight / total_weight
        operation_count += 1  # Assignment of normalized weight

    # Generate a weighted random sample of nodes
    sample_size = random.randint(min_size, max_size)
    operation_count += 1  # random.randint call

    sample = set(random.choices(list(graph.nodes()), weights=normalized_weights.values(), k=sample_size))
    operation_count += 2  # random.choices call and set conversion

    return sample, operation_count


def is_independent_set(graph, subset, operation_count):
    checked = set()

    for u in subset:
        operation_count += 1  # For loop iteration
        for v in graph.neighbors(u):
            operation_count += 1  # Nested for lo   op iteration
            operation_count += 1  # Checking if v is in subset
            if v in subset:
                operation_count += 1  # Checking if v is not in checked
                if v not in checked:
                    return False, operation_count
            operation_count += 1  # Completion of the inner loop for a specific u
        checked.add(u)
        operation_count += 1  # Adding u to the checked set

    return True, operation_count



def subset_to_bitvector(subset, node_index_map):
    """Convert a subset of nodes to a bit vector representation using a node to index mapping."""
    bitvector = 0
    for node in subset:
        bitvector |= 1 << node_index_map[node]  # Set the bit at the mapped index to 1

    return bitvector


def randomized_search_independent_set(graph, max_iterations=10000, failure_threshold=100, max_time_seconds=60):
    node_index_map = {node: index for index, node in enumerate(graph.nodes())}
    tested_bitvectors = set()
    max_combinations = 2 ** len(graph.nodes())
    tested_count = 0
    
    best_solution = set()
    best_score = 0

    operation_count = 0
    stop_condition = "iterations"

    failure_count = 0  # Initialize failure counter
    start_time = time.time()  # Record the start time
    
    for _ in range(max_iterations):
        operation_count += 1
        operation_count += 1
        if time.time() - start_time > max_time_seconds:
            stop_condition = "time_limit"
            break
    
        operation_count += 1
        if tested_count >= max_combinations:
            stop_condition = "exhausted"
            break


        candidate, operation_count = generate_random_solution(graph, min_size=best_score, max_size=len(graph), operation_count=operation_count)
        candidate_bitvector = subset_to_bitvector(candidate, node_index_map)

        operation_count += 1
        if candidate_bitvector not in tested_bitvectors:
            operation_count += 1
            tested_count += 1
            tested_bitvectors.add(candidate_bitvector)
            
            is_independent, operation_count = is_independent_set(graph, candidate, operation_count)
            operation_count += 1
            if is_independent:
                operation_count += 1
                score = len(candidate)
                operation_count += 1
                if score > best_score:
                    best_solution = candidate
                    best_score = score
                    failure_count = 0  # Reset failure count on improvement
                    operation_count += 3
                else:
                    failure_count += 1  # Increment failure count
                    operation_count += 1
                    operation_count += 1
                    if failure_count >= failure_threshold:  # Check failure threshold
                        stop_condition = "failure_threshold"
                        break
        
    
    return best_solution, operation_count, len(tested_bitvectors), stop_condition