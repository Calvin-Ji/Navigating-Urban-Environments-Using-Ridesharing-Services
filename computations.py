"""
CSC111 Winter 2023 Course Project

By: Gerald Wang, Mark Estiller, Calvin Ji, Dharma Ong

This file contains the functions that are used for the main computations in this project.

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
import math
from classes import Link, Network


def estimate_neighborhood_size(neighborhood_name: str, data: dict[tuple[str], list[float]]) -> float:
    """
    Make a very rough estimate of the neighborhood size in miles squared and return it.
    We can first assume that the neighborhood is a perfect circle and assume that on average that
    the start location is in the middle of the neighborhood. We could find the average distance from
    the city whose area we are trying to approximate to every other city that it is connected to.
    We take the smallest average distance because presumably that would be the closest city that is
    nearby, and that could be a guess for our radius.

    Preconditions:
    - any(neighborhood_name in pair for pair in data)  # neighborhood_name exists in data
    """
    avg_distances_to_cities = [math.inf]
    for set_of_neighborhood_names in data:
        if neighborhood_name in set_of_neighborhood_names:
            avg_distances_to_cities.append(data[set_of_neighborhood_names][1])
    upper_radius = min(avg_distances_to_cities)
    upper_bound = math.pi * (upper_radius ** 2)

    return upper_bound


def get_avg_times_and_miles(l: list[tuple[float, str, str, float]]) -> dict[tuple[str], list[float]]:
    """
    Return a dictionary where a set of 2 endpoints are keys and the list containing the
    average time at index 0, average distance at index 1, and average cost at index 2
    """
    # A mapping of the endpoints to time
    links_so_far_with_times = {}
    # A mapping of the endpoints to distance
    links_so_far_with_miles = {}

    final_dict = {}
    for data in l:
        # Get all the times
        if f'{data[1]}:{data[2]}' not in links_so_far_with_times:
            links_so_far_with_times[f'{data[1]}:{data[2]}'] = [data[0]]
        else:
            links_so_far_with_times[f'{data[1]}:{data[2]}'] += [data[0]]
        # Get all the distances
        if f'{data[1]}:{data[2]}' not in links_so_far_with_miles:
            links_so_far_with_miles[f'{data[1]}:{data[2]}'] = [data[3]]
        else:
            links_so_far_with_miles[f'{data[1]}:{data[2]}'] += [data[3]]

    for item in links_so_far_with_times:
        avg_time = sum(
            links_so_far_with_times[item]) / len(links_so_far_with_times[item])
        listy = item.split(':')
        start = listy[0]
        stop = listy[1]
        final_dict[(start, stop)] = [round(avg_time, 2)]

    for item in links_so_far_with_miles:
        avg_miles = sum(
            links_so_far_with_miles[item]) / len(links_so_far_with_miles[item])
        listy = item.split(':')
        start = listy[0]
        stop = listy[1]
        final_dict[(start, stop)] += [round(avg_miles, 2)]
    return final_dict


def get_avg_costs(d: dict[tuple[str], list[float]]) -> dict[tuple[str], float]:
    """
    Calculates the average cost to get from one neighbourhood to another neighborhood.
    Returns a dictionary with the endpoints as keys and the average cost as its corresponding values.
    This formula is based on Uber's base fare of $1.55 plus 20 cents per minute, and $1.20 per mile.
    There is also an additional $1.00 "safe rides fee"

    Preconditions:
    - d is a dictionary with a tuple of endpoints as its keys, and a list containing the time at
    index 0, and miles at index 1 as its values
    """
    new_dict = {}
    base_fare = 1.55
    safe_rides_fee = 1.00
    assert isinstance(d, dict)
    for key in d:
        new_dict[key] = round(base_fare + 0.20 * (d[key][0] * 1 / 60) + 1.20 * (d[key][1]) + safe_rides_fee, 2)
    return new_dict


def combine_dict_times_miles_cost(avg_times_and_miles: dict[tuple[str], list[float]],
                                  avg_costs: dict[tuple[str], float]) -> dict[tuple[str], list[float]]:
    """
    Mutates and returns the dictionary containing the times and miles values to also include costs.

    Preconditions:
    - avg_times_and_miles is a dictionary with a tuple of endpoints as its keys, and a list containing the time at
    index 0, and miles at index 1 as their values
    - avg_costs is a dictionary with a tuple of endpoints as its keys, and a float representing the cost as their value
    """
    for endpoints in avg_costs:
        avg_times_and_miles[endpoints].append(avg_costs[endpoints])

    return avg_times_and_miles


def create_graph(d: dict[tuple[str, str], list[float]]) -> Network:
    """
    Generates and returns a network, given a tuple consisting of the neighborhood endpoints as keys,
    with its corresponidng average time at index 0,average distance at index 1, and average cost at index 2.
    """

    network = Network()

    for endpoints in d:
        selected_endpoints = d[endpoints]
        network.add_link(endpoints[0], endpoints[1],
                         selected_endpoints[0], selected_endpoints[1], selected_endpoints[2])

    for neighborhood in network.get_all_neighborhoods():
        neighborhood.size = estimate_neighborhood_size(neighborhood.name, d)

    return network


def find_best_path_dijsktras(network: Network, start: str, stop: str, optimize: str) -> tuple[float, list[str]]:
    """
    Return the best path and its optimized variable between the start
    neighborhood and the stop neighborhood using Dijsktra's algorithm

    >>> network = Network()
    >>> network.add_link('A', 'B', 0, 0, 1.0)
    >>> network.add_link('B', 'C', 0, 0, 2.0)
    >>> network.add_link('C', 'D', 0, 0, 3.0)
    >>> find_best_path_dijsktras(network, 'A', 'D', 'cost')
    (6.0, ['A', 'B', 'C', 'D'])
    >>> network.add_link('A', 'D', 0, 0, 4.0)
    >>> find_best_path_dijsktras(network, 'A', 'D', 'cost')
    (4.0, ['A', 'D'])
    >>> network.add_link('A', 'C', 0, 0, 0.0)
    >>> find_best_path_dijsktras(network, 'A', 'D', 'cost')
    (3.0, ['A', 'C', 'D'])
    """

    if not network.is_connected(start, stop):
        return (0.0, [])

    visited_neighborhoods = set()
    unvisited_neighborhoods = set()
    lowest_costs = {}

    for n in network.to_list()[0]:
        unvisited_neighborhoods.add(network.get_neighborhood(n))
        lowest_costs[n] = [math.inf, None]

    lowest_costs[start] = [0, None]

    # start searching

    current_node = network.get_neighborhood(start)

    while current_node is not None:
        # temporary variables used to determine which node to look at next
        next_node = None
        # path_cost = math.inf

        node_cost_so_far = lowest_costs[current_node.name][0]
        assert node_cost_so_far != math.inf

        for link in current_node.links.values():
            # decide which to optimize:
            if optimize == 'cost':
                link_cost = link.cost
            elif optimize == 'time':
                link_cost = link.time
            elif optimize == 'distance':
                link_cost = link.distance
            else:
                raise ValueError

            node_cost_so_far = lowest_costs[current_node.name][0]
            other_node = link.get_other_endpoint(current_node)
            other_node_cost = node_cost_so_far + link_cost

            if other_node_cost < lowest_costs[other_node.name][0] and other_node not in visited_neighborhoods:
                lowest_costs[other_node.name] = [
                    other_node_cost, current_node]

            if link_cost <= other_node_cost and other_node not in visited_neighborhoods:
                next_node = other_node
                node_cost_so_far = other_node_cost

        visited_neighborhoods.add(current_node)
        unvisited_neighborhoods.remove(current_node)
        current_node = next_node

    # reconstruct the path and return
    distance = lowest_costs[stop][0]

    path = []
    next_name = stop
    prev_node = lowest_costs[next_name][1]

    while prev_node is not None:
        path.insert(0, next_name)
        next_name = prev_node.name
        prev_node = lowest_costs[next_name][1]
    path.insert(0, start)

    return (distance, path)


def compute_path_time(path: list[Link]) -> float:
    """
    Returns the path score by adding every time taken in the path's weighted links.
    The path's score is the total time taken
    """
    path_score_so_far = 0
    for link in path:
        path_score_so_far += link.time
    return path_score_so_far


def compute_path_distance(path: list[Link]) -> float:
    """
    Returns the path score by adding every distance in the path's weighted links.
    The path's score is the total distance
    """
    path_score_so_far = 0
    for link in path:
        path_score_so_far += link.distance
    return path_score_so_far


def compute_path_cost(path: list[Link]) -> float:
    """
    Returns the path score by adding every cost in the path's weighted links.
    The path's score is the total cost
    """
    path_score_so_far = 0
    for link in path:
        path_score_so_far += link.cost
    return path_score_so_far


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
        'disable': ['E9992', 'E9997', 'E9999', 'R0914', 'E9969', 'E9989']
    })
