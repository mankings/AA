from itertools import combinations

def is_independent_set(graph, vertices_set):
    """
    Check if a given set of vertices is an independent set in the graph.
    An independent set has no edges between any two vertices in the set.
    """
    count = 0

    for v1 in vertices_set:
        for v2 in vertices_set:
            count += 1 
            if v1 != v2:
                count += 1 
                if graph.has_edge(v1, v2):
                    count += 1  
                    return False, count

    count += 1
    return True, count


def exhaustive_search_independent_set(graph):
    """
    Perform an exhaustive search to find the maximum independent set.
    """
    count = 0

    n = len(graph.nodes)
    max_set = set()

    # all possible combinations of vertices
    for i in range(n, 0, -1):  # larger sets first for efficiency
        for vertices_subset in combinations(graph.nodes, i):

            is_independent, independent_count = is_independent_set(graph, vertices_subset)
            count += independent_count

            if is_independent:
                count += 1 

                if len(vertices_subset) > len(max_set):
                    count += 1 
                    max_set = set(vertices_subset)

                return max_set, count

    return max_set, count
