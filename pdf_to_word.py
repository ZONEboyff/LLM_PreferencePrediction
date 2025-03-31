import matplotlib.pyplot as plt
import networkx as nx


class Graph:
    def __init__(self, graph_dict=None):
        if graph_dict is None:
            graph_dict = {}
        self.graph_dict = graph_dict

    def vertices(self):
        return list(self.graph_dict.keys())

    def edges(self):
        return self.generate_edges()

    def add_vertex(self, vertex):
        if vertex not in self.graph_dict:
            self.graph_dict[vertex] = []

    def add_edge(self, edge):
        vertex1, vertex2 = tuple(edge)
        # Add both directions since it's an undirected graph
        if vertex1 in self.graph_dict:
            if vertex2 not in self.graph_dict[vertex1]:
                self.graph_dict[vertex1].append(vertex2)
        else:
            self.graph_dict[vertex1] = [vertex2]

        if vertex2 in self.graph_dict:
            if vertex1 not in self.graph_dict[vertex2]:
                self.graph_dict[vertex2].append(vertex1)
        else:
            self.graph_dict[vertex2] = [vertex1]

    def generate_edges(self):
        edges = []
        for vertex in self.graph_dict:
            for neighbor in self.graph_dict[vertex]:
                if {neighbor, vertex} not in edges:
                    edges.append({vertex, neighbor})
        return edges

    def __str__(self):
        res = "vertices: "
        for k in self.graph_dict:
            res += str(k) + " "
        res += "\nedges: "
        for edge in self.generate_edges():
            res += str(edge) + " "
        return res


def hill_climbing_search(graph, start, goal, heuristic):
    """
    Hill Climbing Search - moves to the neighbor with the best (lowest) heuristic value
    and stops when no neighbor has a better heuristic value than the current node.

    Parameters:
        graph: Graph object.
        start: Starting vertex.
        goal: Goal vertex.
        heuristic: Dictionary mapping vertices to heuristic cost values.

    Returns:
        path: List of vertices from start towards goal if path exists; otherwise, [].
        path_edges: List of directed edges showing search direction.
    """
    if start not in graph.graph_dict or goal not in graph.graph_dict:
        return [], []

    current = start
    path = [current]
    path_edges = []

    # Continue until we reach the goal or get stuck
    while current != goal:
        # Get all neighbors of the current vertex
        neighbors = graph.graph_dict[current]

        if not neighbors:
            # No neighbors, we're stuck
            return path, path_edges

        # Find the neighbor with the lowest heuristic value
        best_neighbor = None
        best_heuristic = float('inf')

        for neighbor in neighbors:
            if heuristic[neighbor] < best_heuristic:
                best_neighbor = neighbor
                best_heuristic = heuristic[neighbor]

        # If the best neighbor doesn't improve the heuristic, we're at a local minimum
        if best_heuristic >= heuristic[current]:
            print(f"Stopped at vertex {current} with heuristic value {heuristic[current]}")
            print(f"Best neighbor {best_neighbor} has heuristic value {best_heuristic}")
            return path, path_edges

        # Move to the best neighbor
        path_edges.append((current, best_neighbor))
        current = best_neighbor
        path.append(current)

        # If we've reached the goal, return the path
        if current == goal:
            return path, path_edges

    return path, path_edges


def visualize_graph(graph, path, heuristic, path_edges=[]):
    # Create a directed graph for showing the search direction
    G = nx.DiGraph()

    # Add edges to the graph
    for vertex in graph.graph_dict:
        for neighbor in graph.graph_dict[vertex]:
            G.add_edge(vertex, neighbor)

    # Create a layout - spring layout works well for most graphs
    pos = nx.spring_layout(G)

    # Create node labels with heuristic values
    node_labels = {node: f"{node}\nh={heuristic[node]}" for node in G.nodes()}

    # Draw the graph structure
    nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.3)

    # Draw path edges with different color and style
    if path_edges:
        nx.draw_networkx_edges(G, pos, edgelist=path_edges,
                               edge_color='r', width=2,
                               arrows=True, arrowsize=15,
                               arrowstyle='->')

    # Draw all nodes
    nx.draw_networkx_nodes(G, pos,
                           node_color='lightblue',
                           node_size=1500)

    # Highlight path nodes with different color
    if path:
        nx.draw_networkx_nodes(G, pos, nodelist=path,
                               node_color='orange',
                               node_size=1500)

    # Add node labels with heuristic values
    nx.draw_networkx_labels(G, pos, labels=node_labels,
                            font_size=9, font_weight='bold')

    plt.axis('off')
    plt.title('Hill Climbing Search with Heuristic Values')
    plt.show()


def main():
    # Input number of vertices and edges.
    v = int(input("Enter number of vertices: "))
    e = int(input("Enter number of edges: "))

    graph_dict = {}
    for i in range(v):
        graph_dict[str(i)] = []

    graph = Graph(graph_dict)
    print("Enter edges (space-separated vertices), one edge per line:")
    for i in range(e):
        u, w = input().split()
        # Use a set to add edge; Graph.add_edge expects a set/tuple.
        graph.add_edge({u, w})

    start = input("Enter start vertex: ")
    goal = input("Enter goal vertex: ")

    # Define a heuristic dictionary.
    # For hill climbing, lower heuristic values should be closer to the goal.
    heuristic = {}
    print("Enter heuristic values for each vertex (lower is better/closer to goal):")
    for vertex in graph.vertices():
        heuristic[vertex] = float(input(f"Heuristic for vertex {vertex}: "))

    path, path_edges = hill_climbing_search(graph, start, goal, heuristic)

    if path:
        if path[-1] == goal:
            print("Goal reached! Path found:", ' -> '.join(path))
        else:
            print("Got stuck at a local minimum. Partial path:", ' -> '.join(path))
    else:
        print("No path found!")

    visualize_graph(graph, path, heuristic, path_edges)


if __name__ == "__main__":
    main()