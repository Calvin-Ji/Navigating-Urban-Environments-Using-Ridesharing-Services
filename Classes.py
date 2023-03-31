"""
CSC111 Winter 2023 Course Project

By: Dharma Ong, Gerald Wang, Mark Estiller, Calvin Ji
"""
# import matplotlib.pyplot as plt
# import networkx as nx
# import read_data
# import numpy as np
# import scipy
from __future__ import annotations


class Neighborhood:
    """
    A neighborhood in the network

    Instance Attributes:
    - name: 
        the name of this neighborhood
    - links:
        A mapping that contains the links of this node
        Each key represents the name of the other neighborhoods connected by this node
        The corresponding value is the link leading to that neighborhood
    - size:
        The size of this neighborhood. This will be estimated by another function from the 
        computations file. 

    Representation Invariants:
    - self.name not in self.links
    """
    name: str
    links: dict[str, Link]
    size: float
    
    def __init__(self, name: str) -> None:
        """
        Initialize a neighborhood without any neighbors yet.
        The size of the neighborhood will be set to 0
        """
        self.name = name
        self.neighbors = {}
        self.size = 0.0

    def __repr__(self) -> str:
        """
        Return a string representation of this neighborhood
        """
        return f'Neighborhood({self.name})'
    
class Link:
    """
    A link between 2 neighborhoods

    Instance attributes:
    - endpoints: the 2 neighborhoods that are connected by this link

    Representation Invariants:
    - len(endpoints) == 2
    """
    endpoints: set[Neighborhood]

    def __init__(self, neighborhood1: Neighborhood, neighborhood2: Neighborhood) -> None:
        """
        Iniitalize a link between 2 neighborhoods

        Preconditions:
        - neighborhood1 != neighborhood2
        - there isn't already an existing link between the 2 neighborhoods
        """
        self.endpoints = {neighborhood1, neighborhood2}
        neighborhood1.links[neighborhood2.name] = self
        neighborhood2.links[neighborhood1.name] = self

    def __repr__(self) -> str:
        """
        Return a string representation of this link
        """
        endpoints = list(self.endpoints)
        return f'Links({endpoints[0]}, {endpoints[1]})'
    
    def get_other_endpoint(self, neighborhood: Neighborhood) -> Neighborhood:  
        """Return the endpoint of this link that is not equal to the given neighborhood. 
 
        Preconditions: 
            - neighborhood in self.endpoints 
        """  
        return (self.endpoints - {neighborhood}).pop() 

class Network:  # graph
    """
    A network of Neighborhood(s) connected by Links

    Private Instance Attributes:
        - _nodes: a mapping from names of the neighborhoods to the Neighborhood in this network
    """
        
    _neighborhoods: dict[str, Neighborhood]

    def __init__(self) -> None:
        """
        Initialize an empty network
        """
        self._neighborhoods = {}
    
    def add_neighborhood(self, name: str) -> Neighborhood:
        """
        Add a neighborhood into this network class and return it
        
        Preconditions:
        - name not in self._nodes
        """
        new = Neighborhood(name)
        self._neighborhoods[name] = new
        return new

    def add_link(self, n1: str, n2: str) -> None:
        """
        Add a link between 2 neighborhoods in the network
        """
        if n1 not in self._neighborhoods:
            self.add_neighborhood(n1)
        if n2 not in self._neighborhoods:
            self.add_neighborhood(n2)

        Link(self._neighborhoods[n1], self._neighborhoods[n2])

    def to_list(self) -> tuple[list[str], list[float]]:
        """
        Return a tuple containing:
        1. A list of the names of the neighborhoods in this network
        2. The sizes of these neighborhoods
        """
        neighborhoods = []
        sizes = []
    
        for neighborhood in self._neighborhoods:
            neighborhoods.append(neighborhood)
            sizes.append(self._neighborhoods[neighborhood].size)
    
        return (neighborhoods, sizes)
    


    
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
        'disable': ['E9992', 'E9997']
    })


    # ex_data = [
    #     (50, 'n1', 'n2', 1),
    #     (60, 'n3', 'n3', 3),
    #     (70, 'n3', 'n2', 5)
    # ]
    # g = create_graph(ex_data)
    # visualize(g)

    # data = read_data.read_csv("data/small_test.csv")
    # calculated_data = read_data.get_avg_times_and_miles(data)




##################################################
# Disregard code below
##################################################



# def create_graph(data: list[tuple[float, str, str, float]]) -> nx.Graph:
#     """
#     Create a networkx graph based on the data

#     Preconditions:
#     - data follows the format from the function header
#     """
#     g = nx.Graph()

#     unique_neighborhoods = set()

#     for item in data:
#         if item[1] not in unique_neighborhoods:
#             unique_neighborhoods.add(item[1])
#         if item[2] not in unique_neighborhoods:
#             unique_neighborhoods.add(item[2])
#     # print(list(unique_neighborhoods))
#     g.add_nodes_from(list(unique_neighborhoods))
#     return g
# def visualize(graph: nx.Graph) -> None:
#     """
#     Plot the graph using networkx and matplotlib.pyplot
#     """
#     nx.draw_networkx(graph)
#     plt.show()



    
# if __name__ == '__main__':
#     ex_data = [
#         (50, 'n1', 'n2', 1),
#         (60, 'n3', 'n3', 3),
#         (70, 'n3', 'n2', 5)
#     ]
#     g = create_graph(ex_data)
#     visualize(g)

#     data = read_data.read_csv("data/small_test.csv")
#     calculated_data = read_data.get_avg_times_and_miles(data)

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
