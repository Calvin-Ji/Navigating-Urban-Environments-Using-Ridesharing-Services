"""
CSC111 Winter 2023 Course Project

By: Gerald Wang, Mark Estiller, Calvin Ji, Dharma Ong

This file contains a collection of Python classes and functions that will be used to represent a
network using neighborhoods found in the dataset. One of the calls to the core computations for this
project, which is about finding the best path to optimize certain variables (time, distance, cost), is
contained in this file. 

Copyright and Usage Information
===============================
This file is Copyright (c) 2023 by Gerald Wang, Mark Estiller, Calvin Ji, Dharma Ong.
This module is expected to use data from:
https://www.kaggle.com/datasets/zusmani/uberdrives
"My Uber Drives" by user Zeeshan-Ul-Hassan Usmani. The data encompassed his Uber drives primarily in North Carolina in 2016
(1,175 drives total), and it was presented as a csv with the following columns going from left to right: start date, end date,
category, start, stop, number of miles, and purpose.
"""

from __future__ import annotations
from typing import Callable
import math
# from computations import compute_path_cost, compute_path_distance, compute_path_time


class Neighborhood:
    """
    A neighborhood in the network

    Instance Attributes:
    - name: the name of this neighborhood
    - links: A mapping that contains the links of this node. Each key represents the name of the other
    neighborhoods connected by this node. The corresponding value is the link leading to that neighborhood
    - size: The size of this neighborhood. This will be estimated by another function from the
    computations file.

    Representation Invariants:
    - self.name not in self.links
    - self.size >= 0
    """
    name: str
    links: dict[str, Link]
    size: float

    def __init__(self, name: str) -> None:
        """
        Initialize a neighborhood without any neighbors yet.
        The size of the neighborhood will be set to 0.
        """
        self.name = name
        self.links = {}
        self.size = 0.0

    def __repr__(self) -> str:
        """
        Return a string representation of this neighborhood
        """
        return f'Neighborhood({self.name})'

    def find_all_possible_paths(self, end: str, visited: set[Neighborhood]) -> list[list[Link]]:
        """
        Returns all possible paths. Each path is represented by a list of links.

        Preconditions:
        - self not in visited
        """
        if self.name == end:
            return [[]]

        all_paths = []
        new_visited = visited.union({self})
        for link in list(self.links.values()):
            path_so_far = [link]
            if link.get_other_endpoint(self) not in visited:
                paths = link.get_other_endpoint(
                    self).find_all_possible_paths(end, new_visited)
                for path in paths:
                    path_so_far.extend(path)
                    all_paths.append(path_so_far)
                    path_so_far = [link]
        return all_paths
    
    def check_connected(self, target_name: str, visited: set[Neighborhood]) -> bool:
        """
        Check whether this neighborhood is connected to the target_name neighborhood

        Preconditions:
        - self.name != ''
        - target_name != ''
        """

        if self.name == target_name:
            return True

        visited.add(self)
        for u in self.links:
            neighboring = self.links[u].get_other_endpoint(self)
            if neighboring not in visited:
                if neighboring.check_connected(target_name, visited):
                    return True

        return False


class Link:
    """
    A link between 2 neighborhoods

    Instance attributes:
    - endpoints: the 2 neighborhoods that are connected by this link
    - time: the time taken to go from one endpoint to the other
    - distance: the distance from one endpoint to the other
    - cost: the cost from one endpoint to the other

    Representation Invariants:
    - len(self.endpoints) == 2
    - self.time >= 0
    - self.distance >= 0
    - self.cost >= 0
    """
    endpoints: set[Neighborhood]
    time: float
    distance: float
    cost: float

    def __init__(self, neighborhood1: Neighborhood, neighborhood2: Neighborhood,
                 time: float, distance: float, cost: float) -> None:
        """
        Iniitalize a link between 2 neighborhoods. This link contains information about the
        time, distance, and cost to go from the first neighborhood to the second.

        Preconditions:
        - neighborhood1 != neighborhood2
        - there isn't already an existing link between the 2 neighborhoods
        - time >= 0
        - float >= 0
        - cost >= 0
        """
        self.endpoints = {neighborhood1, neighborhood2}
        neighborhood1.links[neighborhood2.name] = self
        neighborhood2.links[neighborhood1.name] = self
        self.time = time
        self.distance = distance
        self.cost = cost

    def __repr__(self) -> str:
        """
        Return a string representation of this link
        """
        endpoints = list(self.endpoints)
        return f'Links({endpoints[0]}, {endpoints[1]})'

    def get_other_endpoint(self, neighborhood: Neighborhood) -> Neighborhood:
        """
        Return the endpoint of this link that is not equal to the given neighborhood.
        
        Preconditions: 
        - neighborhood in self.endpoints 
        """
        return (self.endpoints - {neighborhood}).pop()

    def get_endpoints(self) -> set[Neighborhood]:
        """
        Return the endpoints in this link.
        """
        return self.endpoints


class Network:  # graph
    """A network of Neighborhood(s) connected by Links."""
    # Private Instance Attributes:
    #    - _neighborhoods: a mapping from names of the neighborhoods to the Neighborhood in this network

    _neighborhoods: dict[str, Neighborhood]

    def __init__(self) -> None:
        """
        Initialize an empty network
        """
        self._neighborhoods = {}

    def initialize_test_sizes(self) -> None:
        for n in self._neighborhoods.values():
            links_list = list(n.links.values())
            n.size = links_list[0].distance

    def get_all_sizes(self) -> dict[str, float]:
        """
        """
        size_dict = {}

        for neighborhood in self._neighborhoods.values():
            size_dict[neighborhood.name] = neighborhood.size
        
        return size_dict

    def add_neighborhood(self, name: str) -> Neighborhood:
        """
        Add a neighborhood into this network class and return it

        Preconditions:
        - name not in self._nodes
        """
        new = Neighborhood(name)
        self._neighborhoods[name] = new
        return new

    def add_link(self, n1: str, n2: str, time: float, distance: float, cost: float) -> None:
        """
        Add a link between 2 neighborhoods in the network.
        This method also initializes the distance, time, and cost attributes for Link
        Return this link

        Preconditions:
        - n1 != ''
        - n2 != ''
        - time >= 0
        - distance >= 0
        - cost >= 0
        """
        if n1 not in self._neighborhoods:
            self.add_neighborhood(n1)
        if n2 not in self._neighborhoods:
            self.add_neighborhood(n2)

        Link(self._neighborhoods[n1],
             self._neighborhoods[n2], time, distance, cost)

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

    def find_best_path_for_key(self, start: str, end: str, key: Callable) -> list[Link]:
        """
        Finds the best path for a certain variable, either time, distance, or cost, given a starting point and 
        end point. The path score is defined as either the total distance, the total time taken, or the total cost 
        (adding up every weighted link in the path depending on the key) from the starting point to the end point,
        and we are trying to minimize the path score

        Preconditions:
        - start in self._neighborhoods
        - end in self._neighborhoods
        - key in {compute_path_time, compute_path_distance, compute_path_cost}

        >>> network = Network()
        >>> network.add_link('A', 'B', 5.0, 10.0, 10.0)
        >>> network.add_link('B', 'C', 10.0, 5.0, 10.0)   
        >>> network.add_link('C', 'D', 10.0, 10.0, 10.0)
        >>> network.add_link('D', 'E', 10.0, 10.0, 8.0)   
        >>> network.add_link('E', 'F', 10.0, 10.0, 10.0)
        >>> network.add_link('F', 'A', 10.0, 10.0, 10.0)   
        >>> network.find_best_path_for_key('A', 'D', compute_path_time)
        [Links(Neighborhood(A), Neighborhood(B)), Links(Neighborhood(B), Neighborhood(C)), Links(Neighborhood(C), Neighborhood(D))]
        >>> network.find_best_path_for_key('A', 'D', compute_path_distance)
        [Links(Neighborhood(A), Neighborhood(B)), Links(Neighborhood(B), Neighborhood(C)), Links(Neighborhood(C), Neighborhood(D))]  
        >>> network.find_best_path_for_key('A', 'D', compute_path_cost)
        [Links(Neighborhood(F), Neighborhood(A)), Links(Neighborhood(F), Neighborhood(E)), Links(Neighborhood(D), Neighborhood(E))]
        """
        # Accumulates every possible path
        all_possible_paths = self.find_all_possible_paths(start, end)

        # Computes its corresponding path scores (distance/time/cost)
        all_possible_path_scores = [key(path) for path in all_possible_paths]

        # Retrieves the minimum path score
        minimum_path_score = min(all_possible_path_scores)

        # Obtains the path that corresponds to the minimum path score
        for i in range(0, len(all_possible_path_scores)):
            if all_possible_path_scores[i] == minimum_path_score:
                return all_possible_paths[i]

        # This should never happen but this is to prevent a python TA error
        return []

    # Helper method for above method
    def find_all_possible_paths(self, start: str, end: str) -> list[list[Link]]:
        """Return a list of all paths in this graph between start and end. 

        Preconditions: 
        - start in self._neighborhoods 
        - end in self._neighborhoods
        """
        start_neighborhood = self._neighborhoods[start]
        return start_neighborhood.find_all_possible_paths(end, set())

    def is_connected(self, neighborhood1: str, neighborhood2: str) -> bool:
        """
        Return True if neighborhood1 and neighborhood2 are connected
        Return False otherwise
        - neighborhood1 != ''
        - neighborhood2 != ''
        """
        if neighborhood1 in self._neighborhoods and neighborhood2 in self._neighborhoods:
            n1 = self._neighborhoods[neighborhood1]
            return n1.check_connected(neighborhood2, set())
        return False

    def get_neighborhood(self, name: str) -> Neighborhood:
        """ 
        Returns the neighborhood object corresponding to the name of the neighborhood

        Preconditions:
        - name in self._neighborhoods
        """
        return self._neighborhoods[name]

    def get_all_links(self) -> set[Link]:
        """
        Get a set of all the links in this network
        """
        set_of_links = set()

        for n in self._neighborhoods.values():
            for link in n.links.values():
                set_of_links.add(link)

        return set_of_links
    
    def get_all_neighborhoods(self) -> set[Neighborhood]:
        """
        """
        set_of_neighborhoods = set()

        for n in self._neighborhoods.values():
            set_of_neighborhoods.add(n)

        return set_of_neighborhoods


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
        'disable': ['E9992', 'E9997'],
        'extra_imports': [math]
    })

    # network = Network()
    # network.add_link('A', 'B', 0, 9, 0)
    # network.add_link('A', 'C', 0, 10, 0)
    # network.add_link('A', 'D', 0, 11, 0)
    # network.add_link('A', 'E', 0, 12, 0)
    # print(network.get_neighborhood('A').size)

    # ex_data = [
    #     (50, 'n1', 'n2', 1),
    #     (60, 'n3', 'n3', 3),
    #     (70, 'n3', 'n2', 5)
    # ]
    # g = create_graph(ex_data)
    # visualize(g)

    # data = read_data.read_csv("data/small_test.csv")
    # calculated_data = read_data.get_avg_times_and_miles(data)
