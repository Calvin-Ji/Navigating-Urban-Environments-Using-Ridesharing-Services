"""
CSC111 Winter 2023 Course Project

By: Gerald Wang, Mark Estiller, Calvin Ji, Dharma Ong

This python file helps visualize the network we have created.

Copyright and Usage Information
===============================
This file is Copyright (c) 2023 by Gerald Wang, Mark Estiller, Calvin Ji, Dharma Ong.
This module is expected to use data from:
https://www.kaggle.com/datasets/zusmani/uberdrives
"My Uber Drives" by user Zeeshan-Ul-Hassan Usmani. The data encompassed his Uber drives primarily in North Carolina
in 2016 (1,175 drives total), and it was presented as a csv with the following columns going from left to right:
start date, end date, category, start, stop, number of miles, and purpose.
"""
from __future__ import annotations
from typing import Optional
from classes import Network
import matplotlib.pyplot as plt
import networkx as nx
import math


def convert_to_nx(graph: Network, path_tuple: Optional[tuple(float, list[str])] = None) -> nx.Graph:
    """
    This function converts our graph class into a networkx graph
    This way, we can visualize the graph

    Preconditions:
    - graph is a valid network
    """
    new = nx.Graph()
    links = graph.get_all_links()

    if path_tuple is not None:
        path = path_tuple[1]
        path_endpoints_list = [{path[i], path[i + 1]} for i in range(0, len(path) - 1)]

    for link in links:
        endpoints = list(link.get_endpoints())
        cost = link.cost

        for n in endpoints:
            if not new.has_node(n.name):
                new.add_node(n.name, size=int(math.log(n.size + 1) * 50))

        endpoints_string_set = {endpoints[0].name, endpoints[1].name}
        if path_tuple is not None and endpoints_string_set in path_endpoints_list:
            new.add_edge(endpoints[0].name, endpoints[1].name, weight=cost, color='red')
        else:
            new.add_edge(endpoints[0].name, endpoints[1].name, weight=cost, color='black')

    return new


def display_graph(nx_graph: nx.Graph) -> None:
    """ Display a networkx graph using matplotlib.pyplot

    >>> network = Network()
    >>> network.add_link('A', 'B', 0, 10, 10)
    >>> network.add_link('B', 'C', 0, 9, 40)
    >>> network.add_link('D', 'C', 0, 3, 30)
    >>> network.add_link('F', 'D', 0, 4, 50)
    >>> network.add_link('A', 'E', 0, 5, 60)
    >>> network.initialize_test_sizes()
    >>> nx_graph = convert_to_nx(network, (0.0, ['A', 'B', 'C']))
    >>> display_graph(nx_graph)
    """
    pos = nx.spring_layout(nx_graph, k=5 / math.sqrt(nx_graph.order()), seed=7)

    sizes = [s for s in nx.get_node_attributes(nx_graph, 'size').values()]
    nx.draw_networkx_nodes(nx_graph, pos, node_size=sizes, node_color="red")

    edges = nx_graph.edges()
    colors = [nx_graph[u][v]['color'] for u, v in edges]
    nx.draw_networkx_edges(nx_graph, pos, width=1, edge_color=colors)
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
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['E9999', 'E9969', 'R1721', 'C0411']
    })
