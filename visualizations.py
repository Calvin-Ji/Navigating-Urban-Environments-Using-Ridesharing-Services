"""
This python file helps visualize the network we've created
"""
from __future__ import annotations
from classes import Network
import matplotlib.pyplot as plt
import networkx as nx
import math
import graphviz


def convert_to_nx(graph: Network) -> nx.Graph:
    """
    This function converts our graph class into a networkx graph
    This way, we can visualize the graph

    Preconditions:
    - graph is a valid network
    """
    new = nx.Graph()
    links = graph.get_all_links()

    for link in links:
        endpoints = list(link.get_endpoints())
        cost = link.cost

        new.add_edge(endpoints[0].name, endpoints[1].name, weight=cost)

    return new


def display_graph(nx_graph: nx.Graph) -> None:
    """ Display a networkx graph using matplotlib.pyplot

    >>> network = Network()
    >>> network.add_link('A', 'B', 0, 0, 10)
    >>> network.add_link('B', 'C', 0, 0, 40)
    >>> network.add_link('D', 'C', 0, 0, 30)
    >>> network.add_link('F', 'D', 0, 0, 50)
    >>> network.add_link('A', 'E', 0, 0, 60)
    >>> nx_graph = convert_to_nx(network)
    >>> display_graph(nx_graph)
    """

    # pos = nx.spring_layout(nx_graph, k=30.0, seed=7)
    pos = nx.spring_layout(nx_graph, k=5/math.sqrt(nx_graph.order()), seed=7)
    
    nx.draw_networkx_nodes(nx_graph, pos, node_size=200, node_color="red")
    nx.draw_networkx_edges(nx_graph, pos, width=1)
    nx.draw_networkx_labels(nx_graph, pos, font_size=5,
                            font_family="sans-serif")

    edge_labels = nx.get_edge_attributes(nx_graph, "weight")
    nx.draw_networkx_edge_labels(nx_graph, pos, edge_labels, font_size=5, font_color="blue")

    ax = plt.gca()
    ax.margins(0.08)
    plt.axis("off")
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)

    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (In PyCharm, select the lines below and press Ctrl/Cmd + / to toggle comments.)
    # You can use "Run file in Python Console" to run PythonTA,
    # and then also test your methods manually in the console.
    # import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'disable': ['E9992', 'E9997']
    # })
