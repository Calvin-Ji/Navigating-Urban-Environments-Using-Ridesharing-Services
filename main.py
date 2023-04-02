"""
CSC111 Winter 2023 Course Project

By: Gerald Wang, Mark Estiller, Calvin Ji, Dharma Ong

This file contains the function to run the entire project
"""


from __future__ import annotations
import read_data
from classes import Neighborhood, Link, Network
import computations
import visualizations


# Test graph to see if find shortest path works


def run_find_best_path_for_time() -> list[Link]:
    data = read_data.read_csv("data/My Uber Drives - 2016.csv")

    # Accumulates the average times, miles, and costs
    avg_times_and_miles = computations.get_avg_times_and_miles(data)
    avg_costs = computations.get_avg_costs(avg_times_and_miles)

    # Combines them into one dictionary
    combined_dict_times_miles_cost = computations.combine_dict_times_miles_cost(
        avg_times_and_miles, avg_costs)

    # Generates the graph using the dictionary
    generated_graph = read_data.create_graph_from_read_csv(
        combined_dict_times_miles_cost)

    # keys in {computations.compute_path_time, computations.compute_path_distance, computations.compute_path_cost}
    best_path = generated_graph.find_best_path_for_key(
        'Flatiron District', 'Midtown East', computations.compute_path_time)
    
    return best_path

def run_find_best_path_for_distance() -> list[Link]:
    data = read_data.read_csv("data/My Uber Drives - 2016.csv")

    # Accumulates the average times, miles, and costs
    avg_times_and_miles = computations.get_avg_times_and_miles(data)
    avg_costs = computations.get_avg_costs(avg_times_and_miles)

    # Combines them into one dictionary
    combined_dict_times_miles_cost = computations.combine_dict_times_miles_cost(
        avg_times_and_miles, avg_costs)

    # Generates the graph using the dictionary
    generated_graph = read_data.create_graph_from_read_csv(
        combined_dict_times_miles_cost)

    # keys in {computations.compute_path_time, computations.compute_path_distance, computations.compute_path_cost}
    best_path = generated_graph.find_best_path_for_key(
        'Flatiron District', 'Midtown East', computations.compute_path_distance)
    
    return best_path

def run_find_best_path_for_cost() -> list[Link]:
    data = read_data.read_csv("data/My Uber Drives - 2016.csv")

    # Accumulates the average times, miles, and costs
    avg_times_and_miles = computations.get_avg_times_and_miles(data)
    avg_costs = computations.get_avg_costs(avg_times_and_miles)

    # Combines them into one dictionary
    combined_dict_times_miles_cost = computations.combine_dict_times_miles_cost(
        avg_times_and_miles, avg_costs)

    # Generates the graph using the dictionary
    generated_graph = read_data.create_graph_from_read_csv(
        combined_dict_times_miles_cost)

    # keys in {computations.compute_path_time, computations.compute_path_distance, computations.compute_path_cost}
    best_path = generated_graph.find_best_path_for_key(
        'Flatiron District', 'Midtown East', computations.compute_path_cost)
    
    return best_path

def run_find_best_path_for_time_dijsktras() -> tuple[float, list[str]]:

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

def display_graph() -> None:
     data = read_data.read_csv("data/large_test.csv")

   # Accumulates the average times, miles, and costs into final_dict
    times_and_miles = computations.get_avg_times_and_miles(data)
    costs = computations.get_avg_costs(data)
    final_dict = computations.combine_dict_times_miles_cost(times_and_miles, costs)

    #Create a network
    network = read_data.create_graph_from_read_csv(final_dict)
    nx_graph = visualizations.convert_to_nx(network)
    visualizations.display_graph(nx_graph)





if __name__ == '__main__':

    print(run_find_best_path_for_time())
    print(run_find_best_path_for_distance())
    print(run_find_best_path_for_cost())

    print(run_find_best_path_for_time_dijsktra())
    print(run_find_best_path_for_distance_dijsktra())
    print(run_find_best_path_for__dijsktra())



    #run_estimate_neighborhood_size()
    #run_initialize_sizes()