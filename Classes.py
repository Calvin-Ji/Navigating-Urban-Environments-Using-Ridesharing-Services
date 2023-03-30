import matplotlib.pyplot as plt
import networkx as nx
import read_data
import numpy as np
import scipy


def create_graph(data: list[tuple[float, str, str, float]]) -> nx.Graph:
    """
    Create a networkx graph based on the data

    Preconditions:
    - data follows the format from the function header
    """
    g = nx.Graph()

    unique_neighborhoods = set()

    for item in data:
        if item[1] not in unique_neighborhoods:
            unique_neighborhoods.add(item[1])
        if item[2] not in unique_neighborhoods:
            unique_neighborhoods.add(item[2])

    # print(list(unique_neighborhoods))

    g.add_nodes_from(list(unique_neighborhoods))

    return g


def visualize(graph: nx.Graph) -> None:
    """
    Plot the graph using networkx and matplotlib.pyplot
    """
    nx.draw_networkx(graph)
    plt.show()


if __name__ == '__main__':
    ex_data = [
        (50, 'n1', 'n2', 1),
        (60, 'n3', 'n3', 3),
        (70, 'n3', 'n2', 5)
    ]
    g = create_graph(ex_data)
    visualize(g)

    data = read_data.read_csv("data/small_test.csv")
    calculated_data = read_data.get_avg_times_and_miles(data)


def find_coordinates(distances: list[list[int]]) -> np.array:
    """
    Distances represents an n x n matrix.
    Each row in the list is an object
    is a python list with distances to other points as its elements

    Example:
    >>> dist = [
    >>>    [0, 1, 2],  # object A
    >>>    [1, 0, 3],  # object B
    >>>    [2, 3, 0]   # object C
    >>> ]

    Notice that the diagonals will always be 0, since the distance from a point to itself is always 0
    Distance from object A to object B is equal to dist[0][1],
    Distance from object A to object C is equal to dist[0][2],
    Distance from object B to object C is equal to dist[1][2],
    etc.

    Given this matrix, find the coordinates of all the objects

    Preconditions:
    - all(distances[n][n] == 0 for n in range(len(distances)))
    """
    matrix = np.array(distances)
    mds = scipy.MDS(n_components=2, dissimilarity='precomputed')
    coordinates = mds.fit_transform(matrix)

    return coordinates


def plot_points(coordinates: np.array, graph: nx.Graph) -> None:
    """
    Given the coordinates of the points, plot them on a networkx graph and return this graph
    """
    positions = {}
    i = 0

    for node in graph.nodes:
        positions[node] = coordinates[i]
        i += 1

    nx.draw_networkx(graph, positions, with_labels=True)

# class nxGraph:
#     """
#     A networkx graph that has neighborhoods as nodes and
#     the average distance and time for a ride as its links


#     """
#     _nodes:

#     def __init__(self, data: list[tuple(int, str, str, float)]) -> None:
#         """
#         Initialize the nxGraph given the data

#         Preconditions:
#         - data follows the format from the header
#         """
#         unique_neighborhoods = set()

#         for item in data:
#             if item[1] not in unique_neighborhoods:
#                 unique_neighborhoods.add(item[1])
#             if item[2] not in unique_neighborhoods:
#                 unique_neighborhoods.add(item[2])

#         for neighborhood in unique_neighborhoods:
