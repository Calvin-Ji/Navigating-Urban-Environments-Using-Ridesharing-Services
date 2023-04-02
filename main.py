"""
CSC111 Winter 2023 Course Project

By: Gerald Wang, Mark Estiller, Calvin Ji, Dharma Ong

This file contains the function to run the entire project
"""


from __future__ import annotations
import read_data
from classes import Neighborhood, Link, Network
import computations


# Test graph to see if find shortest path works


def run_find_best_path_for_key() -> list[Link]:
    data = read_data.read_csv("data/large_test.csv")

    # Accumulates the average times, miles, and costs
    avg_times_and_miles = computations.get_avg_times_and_miles(data)
    avg_costs = computations.get_avg_costs(avg_times_and_miles)

    # Combines them into one dictionary
    combined_dict_times_miles_cost = computations.combine_dict_times_miles_cost(
        avg_times_and_miles, avg_costs)

    # Generates the graph using the dictionary
    generated_graph = read_data.create_graph_from_read_csv(
        combined_dict_times_miles_cost)

    best_path = generated_graph.find_best_path_for_key(
        'Fort Pierce', 'Downtown', computations.compute_path_distance)  # end neighborhood, set
    return best_path

def run_estimate_neighborhood_size() -> float:
    data = read_data.read_csv("data/large_test.csv")

    # Accumulates the average times, miles, and costs into final_dict
    times_and_miles = computations.get_avg_times_and_miles(data)
    costs = computations.get_avg_costs(data)
    final_dict = computations.combine_dict_times_miles_cost(times_and_miles, costs)

    #Create a network and a accumulator
    network = read_data.create_graph_from_read_csv(final_dict)
    NC_size_estimate = 0

    #iterate through the neighbourhoodnames and update the accumulator
    for neighborhoodname in network._neighborhoods:
        NC_size_estimate += computations.estimate_neighborhood_size(neighborhoodname, final_dict)

    #return the accumulator after the for loop is done
    return NC_size_estimate

def run_initialize_sizes() -> float:
    data = read_data.read_csv("data/large_test.csv")

   # Accumulates the average times, miles, and costs into final_dict
    times_and_miles = computations.get_avg_times_and_miles(data)
    costs = computations.get_avg_costs(data)
    final_dict = computations.combine_dict_times_miles_cost(times_and_miles, costs)

    #Create a network and a accumulator
    network = read_data.create_graph_from_read_csv(final_dict)
    network.initialize_sizes

    #accumulator for size
    NC_size = 0

    #iterate through the neighbourhoodnames and update the accumulator
    for neighborhoodname in network._neighborhoods:
       NC_size += network._neighborhoods[neighborhoodname].size

    #return the accumulator after the for loop is done
    return NC_size




if __name__ == '__main__':
    #run_find_best_path_for_key()
    #run_estimate_neighborhood_size()
    run_initialize_sizes()