"""
CSC111 Winter 2023 Course Project

By: Gerald Wang, Mark Estiller, Calvin Ji, Dharma Ong

This file contains the runner functions that combines all the algorithms and computations from every file 
to output the core values for this project.

Comment out the function calls under the main block to see what each of them outputs! When testing the
functions that require start and end arguments, make sure to pass in valid neighborhoods. Refer 
to the global variable ALL_NEIGHBORHOODS to see valid neighborhoods.

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
import read_data
from classes import Link
import computations
import visualizations
from typing import Optional


ALL_NEIGHBORHOODS = {'Central', 'Briar Meadow', 'Covington', 'Chessington', 'Huntington Woods', 'Hayesville', 
                     'Parkway Museums', 'Nugegoda', 'Kissimmee', 'French Quarter', 'Topton', 'Tribeca', 
                     'Convention Center District', 'K Street', 'East Elmhurst', 'Cary', 'El Cerrito', 'Redmond', 
                     'Wayne Ridge', 'Potrero Flats', 'Holly Springs', 'Sugar Land', 'West Palm Beach', 'Kenner', 
                     'Leesville Hollow', 'North Berkeley Hills', 'Townes at Everett Crossing', 'Arlington Park at Amberly', 
                     'NOMA', 'New York', 'Hazelwood', 'Mebane', 'College Avenue', 'Ilukwatta', 'East Austin', 'Arlington', 
                     'Port Bolivar', 'Jackson Heights', 'Burtrose', 'University District', 'Tanglewood', 'Winston Salem', 
                     'Lakeview', 'Eastgate', 'Metairie', 'Midtown West', 'Katy', 'Fairmont', 'Gulfton', 'Banner Elk', 
                     'Umstead', 'San Jose', 'Queens County', 'Wake Co.', 'Vista East', 'Sky Lake', 'Bellevue', 
                     'Gramercy-Flatiron', 'Bywater', 'Kalorama Triangle', 'Fort Pierce', 'Sunnyside', 'Lower Garden District', 
                     'Flatiron District', 'Mountain View', 'Durham', 'Stonewater', 'Queens', 'Arts District', 'Menlo Park', 
                     'Asheville', 'Tenderloin', 'Gampaha', 'Rawalpindi', 'Rose Hill', 'Noorpur Shahan', 'Williamsburg Manor', 
                     'Meredith', 'Florence', 'Walnut Terrace', 'Katunayake', 'Palm Beach', 'Colombo', 'Financial District', 
                     'East Harlem', 'Summerwinds', 'Jacksonville', 'Kilarney Woods', 'Storyville', 'Columbia Heights', 
                     'Parkway', 'Katunayaka', 'Alief', 'Krendle Woods', 'Morrisville', 'Downtown', 'Galveston', 'Kips Bay', 
                     'Midtown East', 'Lake Wellingborough', 'South Congress', 'Hudson Square', 'Meredith Townes', 'Coxville', 
                     'Boone', 'Austin', 'Edgehill Farms', 'Medical Centre', 'Sand Lake Commons', 'Sunnyvale', 'Washington', 
                     'Heritage Pines', 'Faubourg Marigny', 'Newland', 'Southwest Berkeley', 'Eagan Park', 'Ingleside', 'Latta', 
                     'Chalmette', 'Chapel Hill', 'Couples Glen', 'NoMad', 'Depot Historic District', 'Bay Farm Island', 
                     'Washington Avenue', 'West University', 'Greater Greenspoint', 'Seattle', 'Elmhurst', 'Renaissance', 
                     'Apex', 'Cedar Hill', 'Marigny', 'Houston', 'CBD', 'Hog Island', 'Savon Height', 'Agnew', 'Southside', 
                     'North Austin', 'Georgian Acres', 'Waverly Place', 'Elk Park', 'Ridgeland', 'Oakland', 'San Francisco', 
                     'Newark', 'Isles of Buena Vista', 'St Thomas', 'Palo Alto', 'West End', 'Wake Forest', 'Almond', 'Cory', 
                     'Eagle Rock', 'Preston', 'Seaport', 'Kildaire Farms', 'Macgregor Downs', 'Capitol One', 'Jamaica', 
                     'Harden Place', 'Pontchartrain Beach', 'Raleigh', 'SOMISSPO', 'Tudor City', "Hell's Kitchen", 'Mandeville', 
                     'Islamabad', 'Red River District', 'Midtown', 'Lower Manhattan', 'Farmington Woods', 'Orlando', 'Santa Clara', 
                     'Long Island City', 'Jamestown Court', 'Whitebridge', 'Emeryville', 'Bryson City', 'Congress Ave District', 
                     'Lexington Park at Amberly', 'R?walpindi', 'South Berkeley', 'Fayetteville Street', 'Old City', 'Mcvan', 
                     'Northwest Rectangle', 'Berkeley', 'Connecticut Avenue', 'Northwoods', 'Westpark Place', 'The Drag', 'Arabi', 
                     'New Orleans', 'South', 'Sharpstown', 'Daytona Beach', 'Weston', 'Soho', 'West Berkeley', 'Fuquay-Varina'}


def run_get_all_neighbourhoods() -> list[str]:
    data = read_data.read_csv("data/My Uber Drives - 2016.csv")
    set_so_far = set()
    for tuple in data:
        set_so_far.add(tuple[1])
        set_so_far.add(tuple[2])
    return set_so_far    
        

def run_find_best_path_for_time(start: str, end: str) -> list[Link]:
    """Returns the best path to take in order to optimize TIME (seconds).
    If the start and end are the same or if there is no path, return an empty list.
    Preconditions:
    - start in ALL_NEIGHBORHOODS 
    - end in ALL_NEIGHBORHOODS 
    """
    data = read_data.read_csv("data/My Uber Drives - 2016.csv")

    # Accumulates the average times, miles, and costs
    avg_times_and_miles = computations.get_avg_times_and_miles(data)
    avg_costs = computations.get_avg_costs(avg_times_and_miles)

    # Combines them into one dictionary
    combined_dict_times_miles_cost = computations.combine_dict_times_miles_cost(
        avg_times_and_miles, avg_costs)

    # Generates the graph using the dictionary
    generated_graph = computations.create_graph(
        combined_dict_times_miles_cost)

    # keys in {computations.compute_path_time, computations.compute_path_distance, computations.compute_path_cost}
    best_path = generated_graph.find_best_path_for_key(
        start, end, computations.compute_path_time)
    
    return best_path

def run_find_best_path_for_distance(start: str, end: str) -> list[Link]:
    """Returns the best path to take in order to optimize DISTANCE (miles).
     If the start and end are the same or if there is no path, return an empty list.
    Preconditions:
    - start in ALL_NEIGHBORHOODS 
    - end in ALL_NEIGHBORHOODS 
    """
    data = read_data.read_csv("data/My Uber Drives - 2016.csv")

    # Accumulates the average times, miles, and costs
    avg_times_and_miles = computations.get_avg_times_and_miles(data)
    avg_costs = computations.get_avg_costs(avg_times_and_miles)

    # Combines them into one dictionary
    combined_dict_times_miles_cost = computations.combine_dict_times_miles_cost(
        avg_times_and_miles, avg_costs)

    # Generates the graph using the dictionary
    generated_graph = computations.create_graph(
        combined_dict_times_miles_cost)

    # keys in {computations.compute_path_time, computations.compute_path_distance, computations.compute_path_cost}
    best_path = generated_graph.find_best_path_for_key(
        start, end, computations.compute_path_distance)
    
    return best_path

def run_find_best_path_for_cost(start: str, end: str) -> list[Link]:
    """Returns the best path to take in order to optimize COST (in USD) 
     If the start and end are the same or if there is no path, return an empty list.
    Preconditions:
    - start in ALL_NEIGHBORHOODS 
    - end in ALL_NEIGHBORHOODS 
    """
    data = read_data.read_csv("data/My Uber Drives - 2016.csv")

    # Accumulates the average times, miles, and costs
    avg_times_and_miles = computations.get_avg_times_and_miles(data)
    avg_costs = computations.get_avg_costs(avg_times_and_miles)

    # Combines them into one dictionary
    combined_dict_times_miles_cost = computations.combine_dict_times_miles_cost(
        avg_times_and_miles, avg_costs)

    # Generates the graph using the dictionary
    generated_graph = computations.create_graph(
        combined_dict_times_miles_cost)

    # keys in {computations.compute_path_time, computations.compute_path_distance, computations.compute_path_cost}
    best_path = generated_graph.find_best_path_for_key(
        start, end, computations.compute_path_cost)
    
    return best_path

def run_find_best_path_for_time_dijsktras(start: str, end: str) -> tuple[float, list[str]]:
    """Returns the best path to take in order to optimize TIME (seconds) using the Dijsktras Algorithm
    
    Preconditions:
    - start in ALL_NEIGHBORHOODS 
    - end in ALL_NEIGHBORHOODS 
    """
    data = read_data.read_csv("data/My Uber Drives - 2016.csv")

    # Accumulates the average times, miles, and costs
    avg_times_and_miles = computations.get_avg_times_and_miles(data)
    avg_costs = computations.get_avg_costs(avg_times_and_miles)

    # Combines them into one dictionary
    combined_dict_times_miles_cost = computations.combine_dict_times_miles_cost(
        avg_times_and_miles, avg_costs)

    # Generates the graph using the dictionary
    generated_graph = computations.create_graph(
        combined_dict_times_miles_cost)
    
    best_path = computations.find_best_path_dijsktras(generated_graph, start, end, 'time')

    return best_path

def run_find_best_path_for_distance_dijsktras(start: str, end: str) -> tuple[float, list[str]]:
    """Returns the best path to take in order to optimize DISTANCE (miles) using the Dijsktras Algorithm
    
    Preconditions:
    - start in ALL_NEIGHBORHOODS 
    - end in ALL_NEIGHBORHOODS 
    """
    data = read_data.read_csv("data/My Uber Drives - 2016.csv")

    # Accumulates the average times, miles, and costs
    avg_times_and_miles = computations.get_avg_times_and_miles(data)
    avg_costs = computations.get_avg_costs(avg_times_and_miles)

    # Combines them into one dictionary
    combined_dict_times_miles_cost = computations.combine_dict_times_miles_cost(
        avg_times_and_miles, avg_costs)

    # Generates the graph using the dictionary
    generated_graph = computations.create_graph(
        combined_dict_times_miles_cost)
    
    best_path = computations.find_best_path_dijsktras(generated_graph, start, end, 'distance')

    return best_path

def run_find_best_path_for_cost_dijsktras(start: str, end: str) -> tuple[float, list[str]]:
    """Returns the best path to take in order to optimize COST (in USD) using the Dijsktras Algorithm
    
    Preconditions:
    - start in ALL_NEIGHBORHOODS 
    - end in ALL_NEIGHBORHOODS 
    """
    data = read_data.read_csv("data/My Uber Drives - 2016.csv")

    # Accumulates the average times, miles, and costs
    avg_times_and_miles = computations.get_avg_times_and_miles(data)
    avg_costs = computations.get_avg_costs(avg_times_and_miles)

    # Combines them into one dictionary
    combined_dict_times_miles_cost = computations.combine_dict_times_miles_cost(
        avg_times_and_miles, avg_costs)

    # Generates the graph using the dictionary
    generated_graph = computations.create_graph(
        combined_dict_times_miles_cost)
    
    best_path = computations.find_best_path_dijsktras(generated_graph, start, end, 'cost')

    return best_path


def run_estimate_neighborhood_size(neighborhood: str) -> float:
    """Returns an estimate of the size of North Carolina by adding up all the estimated neighborhood sizes
    
    Preconditions:
    - neighborhood in ALL_NEIGHBORHOODS
    """
    data = read_data.read_csv("data/My Uber Drives - 2016.csv")

    # Accumulates the average times, miles, and costs into final_dict
    times_and_miles = computations.get_avg_times_and_miles(data)
    costs = computations.get_avg_costs(times_and_miles)
    final_dict = computations.combine_dict_times_miles_cost(times_and_miles, costs)

    network = computations.create_graph(final_dict)

    # return computations.estimate_neighborhood_size(neighborhood, final_dict)
    return network.get_neighborhood(neighborhood).size


def display_graph(path: Optional[tuple[float, list[str]]] = None) -> None:
    """Displays the whole network"""
    data = read_data.read_csv("data/My Uber Drives - 2016.csv")

    # Accumulates the average times, miles, and costs into final_dict
    times_and_miles = computations.get_avg_times_and_miles(data)
    costs = computations.get_avg_costs(times_and_miles)
    final_dict = computations.combine_dict_times_miles_cost(times_and_miles, costs)

    # Create a network
    network = computations.create_graph(final_dict)
    nx_graph = visualizations.convert_to_nx(network, path)
    visualizations.display_graph(nx_graph)



def runner() -> None:
    """"
    Function that takes user inputs and runs the program based on the inputs.
    n, n1, and n2 must be valid neighborhoods in the ALL_NEIGHBORHOODS global variable
    """
    action1 = int(input("Estimate neighborhood size/Find best path (0/1): "))

    if action1 == 0:
        n = input("Input a neighborhood (Proper Capitalization): ")
        print(run_estimate_neighborhood_size(n))
    elif action1 == 1:
        action2 = int(input("Optimize time/distance/cost (0/1/2): "))
        action3 = input("Use Dijkstra's algorithm? (y/n): ")

        n1 = input("Input neighborhood 1 (Proper Capitalization): ")
        n2 = input("Input neighborhood 2 (Proper Capitalization): ")

        if action2 == 0 and action3.lower() == 'y':
            print(run_find_best_path_for_time_dijsktras(n1, n2))
            display_graph(run_find_best_path_for_time_dijsktras(n1, n2))
        elif action2 == 1 and action3.lower() == 'y':
            print(run_find_best_path_for_distance_dijsktras(n1, n2))
            display_graph(run_find_best_path_for_distance_dijsktras(n1, n2))
        elif action2 == 2 and action3.lower() == 'y':
            print(run_find_best_path_for_cost_dijsktras(n1, n2))
            display_graph(run_find_best_path_for_cost_dijsktras(n1, n2))
        elif action2 == 0 and action3.lower() == 'n':
            print(run_find_best_path_for_time(n1, n2))
            display_graph(run_find_best_path_for_time(n1, n2))
        elif action2 == 1 and action3.lower() == 'n':
            print(run_find_best_path_for_distance(n1, n2))
            display_graph(run_find_best_path_for_distance(n1, n2))
        else:
            print(run_find_best_path_for_cost(n1, n2))
            display_graph(run_find_best_path_for_cost(n1, n2))
        
        
        


if __name__ == '__main__':
    start = True
    
    while start:
        runner()
        start = bool(input("Continue? True/False: "))
        if str(start).lower() == 'true':
            start = True
        else:
            start = False


        

    # print(run_get_all_neighbourhoods())
    display_graph(run_find_best_path_for_cost_dijsktras('Boone', 'Chapel Hill'))

    # print(run_find_best_path_for_time('Flatiron District', 'Midtown East'))
    # print(run_find_best_path_for_distance('Flatiron District', 'Midtown East'))
    # print(run_find_best_path_for_cost('Flatiron District', 'Midtown East'))

    # print(run_find_best_path_for_time_dijsktras('Flatiron District', 'Midtown East'))
    # print(run_find_best_path_for_distance_dijsktras('Flatiron District', 'Midtown East'))
    print(run_find_best_path_for_cost_dijsktras('Boone', 'Chapel Hill'))

    # print(run_estimate_neighborhood_size("Westpark Place"))
    

    # print(run_estimate_neighborhood_size("Durham"))


    # print(run_estimate_neighborhood_size("Midtown"))


    # print(run_estimate_neighborhood_size("Cary"))
