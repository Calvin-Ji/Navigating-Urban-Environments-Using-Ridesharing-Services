import matplotlib.pyplot as plt
import networkx as nx
import read_data


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
