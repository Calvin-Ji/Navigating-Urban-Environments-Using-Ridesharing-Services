"""
This python file 
"""
from classes import Network
import networkx as nx



def convert(graph: Network) -> nx.Graph:
    """
    This function converts our graph class into a networkx graph
    This way, we can visualize the graph
    """
    new = nx.Graph()

    result = graph.to_list()

    neighborhoods = result[0]
    
    for neighborhood in neighborhoods:
        new.add_node(neighborhood)
    




