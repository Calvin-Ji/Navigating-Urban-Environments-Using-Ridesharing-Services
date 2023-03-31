import math
from classes import Neighborhood, Link, Network
import numpy as np
from sklearn.manifold import MDS
import networkx as nx


def estimate_neighborhood_size(neighborhood_name: str, data: dict[tuple[str]:list[float]]) -> float:
    """
    Make a very rough estimate of of the neighborhood size in miles squared and return it.
    We can first assume that the neighborhood is a perfect circle and assume that on average that the start
    location is in the middle of the neighborhood. We could find the average distance 
    from the city whose area we are trying to approximate to every other city that it is connected to. 
    We take the smallest average distance because presumably that would be the closest city that is 
    nearby, and that could be a guess for our radius.

    Preconditions:
    - any(neighborhood_name in pair for pair in data)  # neighborhood_name exists in data
    """
    # lower_radius = 0
    # for set_of_neighborhood_names in data:
    #     if set_of_neighborhood_names == (neighborhood_name, neighborhood_name):
    #         lower_radius = data[set_of_neighborhood_names][1]
    # lower_bound = pi * (lower_radius) ** 2

    avg_distances_to_cities = [math.inf]
    for set_of_neighborhood_names in data:
        if neighborhood_name in set_of_neighborhood_names:
            avg_distances_to_cities.append(data[set_of_neighborhood_names][1])
    upper_radius = min(avg_distances_to_cities)
    upper_bound = math.pi * (upper_radius) ** 2

    return upper_bound



# DO NOT TOUCH THESE THINGS!!!!!!!!!!!!
#################################################################################
#################################################################################
################################################################################# 

# # We will assume that we have the GRAPH already, and probably place this inside the graph class
# def find_shortest_path_every_neighborhood(self, end: str, visited: set[str]) -> list[str]:
#     """
#     Finds the shortest path that traverses every neighbourhood, given a starting point and 
#     end point. The path score is defined as the total distance (adding up every weighted links) 
#     from the starting point
#     to the end point.
#     """
#     # Accumulates every possible path 
#     all_possible_paths = find_all_possible_paths(end, visited)

#     # Filters out every path that does not go through every node, and computes its corresponding path scores
#     all_possible_paths_every_neighborhood = [path for path in all_possible_paths]
#     all_possible_path_scores_every_neighborhood = [compute_path_score(path) for path in all_possible_paths_every_neighborhood]

#     # Retrieves the minimum path score
#     minimum_path_score = min(all_possible_path_scores_every_neighborhood)

#     # Obtains the path that corresponds to the minimum path score
#     for i in range(0, len(all_possible_path_scores_every_neighborhood)):
#         if all_possible_path_scores_every_neighborhood[i] ==  minimum_path_score:
#             return all_possible_paths_every_neighborhood[i]
    
#     # This should never happen but this is to prevent a python TA error
#     return []


# # This is a node method
# def find_all_possible_paths(self, end: str, visited: set[str]) -> list[list[Link]]:
#     """Helper method 1 - Returns all possible paths. Each path is represented by a list of links.
#     """
#     if self.name == end:
#         return [[]]
  
#     all_paths = []  
#     new_visited = visited.union({self})  
#     for link in list(self.links.values()):  
#         path_so_far = [link]  
#         if link.get_other_endpoint(self) not in visited:  
#             paths = link.get_other_endpoint(self).find_all_possible_paths(end, new_visited)  
#             for path in paths:  
#                 path_so_far.extend(path)
#                 all_paths.append(path_so_far)  
#                 path_so_far = [link]  
#     return all_paths

# #This is a graph method
# def find_all_possible_paths(self, start: str, end: str, visited: set[str]) -> list[list[Link]]:
#     start_node = self._nodes[start]
#     return start_node.find_paths(end, set())


# def compute_path_score(path: list[Link]) -> float:
#     """Returns the path score by adding every distance in the path's weighted links."""
#     path_score_so_far = 0
#     for link in path:
#         path_score_so_far += link.path_score
#     return path_score_so_far

    
#################################################################################
#################################################################################
################################################################################# 

def find_shortest_path_dijsktras(network: Network, start: str, stop: str) -> tuple(float, list[str]):
    """ Return the shortest path and its distance between the start neighborhood and the stop neighborhood using Dijsktra's algorithm
    """

    if not network.is_connected(start, stop):
        return (0.0, [])
    
    


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
    mds = MDS(n_components=2, dissimilarity='precomputed')
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