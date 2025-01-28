import networkx as nx
import matplotlib.pyplot as plt
from collections import deque


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


def depth_first_search(graph, start, goal):
    if start not in graph.graph_dict or goal not in graph.graph_dict:
        return []

    stack = [(start, [start])]
    visited = set()

    while stack:
        vertex, path = stack.pop()

        if vertex == goal:
            return path

        if vertex not in visited:
            visited.add(vertex)

            # Add neighbors in reverse order to maintain DFS property
            for neighbor in reversed(graph.graph_dict[vertex]):
                if neighbor not in visited:
                    new_path = path + [neighbor]
                    stack.append((neighbor, new_path))

    return []


def visualize_graph(graph, path):
    G = nx.Graph()
    for vertex in graph.graph_dict:
        for neighbor in graph.graph_dict[vertex]:
            G.add_edge(vertex, neighbor)

    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='lightblue',
            node_size=1000, font_size=10, font_weight='bold')

    if path:
        path_edges = list(zip(path, path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges,
                               edge_color='r', width=2)
        nx.draw_networkx_nodes(G, pos, nodelist=path,
                               node_color='orange')

    plt.show()


def main():
    v = int(input("Enter number of vertices: "))
    e = int(input("Enter number of edges: "))

    graph_dict = {}
    for i in range(v):
        graph_dict[str(i)] = []

    graph = Graph(graph_dict)
    print("Enter edges (space-separated vertices), one edge per line:")
    for i in range(e):
        u, v = input().split()
        graph.add_edge({u, v})

    start = input("Enter start vertex: ")
    goal = input("Enter goal vertex: ")

    path = depth_first_search(graph, start, goal)
    if path:
        print("Path:", ' -> '.join(path))
    else:
        print("No path found!")

    visualize_graph(graph, path)


if __name__ == "__main__":
    main()