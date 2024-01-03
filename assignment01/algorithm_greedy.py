import networkx as nx

def sort_vertices(graph: nx.Graph):
    count = 0

    def merge(left, right):
        nonlocal count
        merged = []
        while left and right:
            count += 1
            if graph.degree(left[0]) <= graph.degree(right[0]):
                count += 1
                merged.append(left.pop(0))
            else:
                count += 1
                merged.append(right.pop(0))

        count += len(left) + len(right)
        merged.extend(left if left else right)
        return merged
    
    def merge_sort(nodes):
        if len(nodes) <= 1:
            return nodes
        
        mid = len(nodes) // 2
        left = merge_sort(nodes[:mid])
        right = merge_sort(nodes[mid:])
        return merge(left, right)
    
    return merge_sort(list(graph.nodes)), count


def greedy_heuristic_independent_set(graph: nx.Graph):
    """
    Find an independent set using a greedy heuristic approach.
    """

    sorted_vertices, count = sort_vertices(graph)

    max_independent_set = set()

    while(len(sorted_vertices) > 0):
        v = sorted_vertices[0]
        
        count += 1
        # Add the vertex to the independent set
        max_independent_set.add(v)

        # Mark the vertex and all its neighbors as considered
        sorted_vertices.remove(v)

        neighbors = set(graph.neighbors(v))
        sorted_vertices = [v for v in sorted_vertices if v not in neighbors]
        count += len(neighbors)
    
    return max_independent_set, count
