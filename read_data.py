"""
CSC111 Winter 2023 Course Project

By: Gerald Wang, Mark Estiller, Calvin Ji, Dharma Ong

This file contains functions that will read the dataset and output it in a format
that can be used for the computations
"""


from __future__ import annotations
import datetime
# import math  # This is for the estimate size function - Calvin
import computations
import numpy as np
from classes import Network # Neighborhood, Link, Network


def read_csv(file_name: str) -> list[tuple[float, str, str, float]]:
    """ Reads the csv file and returns a list of tuples of (time, start_loc, stop_loc, distance)

    time is a float representing the amount of time taken in seconds
    start_loc is a string representing the starting neighborhood
    stop_loc is a string representing the stopping neighborhood
    distance is a float representing the distance travelled in miles
    """
    trip_data = []
    with open(file_name, 'r') as f:
        data = f.readlines()
    rows = data[1:]

    for row in rows:
        row = row.split(',')
        start_time = row[0]
        end_time = row[1]
        start_loc = row[3]
        stop_loc = row[4]
        distance = row[5]

        # print(row)
        # print(row[0])

        if start_loc != stop_loc and start_loc != 'Unknown Location' and stop_loc != 'Unknown Location':
            # converting the times to datetimes

            temp = start_time.split()
            date_params = temp[0].split('/')
            time_params = temp[1].split(':')

            start_datetime = datetime.datetime(
                int(date_params[2]), int(date_params[0]), int(date_params[1]), int(time_params[0]), int(time_params[1]))

            temp = end_time.split()
            date_params = temp[0].split('/')
            time_params = temp[1].split(':')

            stop_datetime = datetime.datetime(
                int(date_params[2]), int(date_params[0]), int(date_params[1]), int(time_params[0]), int(time_params[1]))

            time_delta = stop_datetime - start_datetime

            trip_data.append(
                (time_delta.total_seconds(), start_loc, stop_loc, float(distance)))

    return trip_data


def create_graph_from_read_csv(d: dict[tuple[str, str], list[float]]) -> Network:
    """
    Generates and returns a network, given a tuple consisting of the neighborhood endpoints as keys,
    with its corresponidng average time at index 0,average distance at index 1, and average cost at index 2.
    """

    network = Network()

    for endpoints in d:
        selected_endpoints = d[endpoints]
        network.add_link(endpoints[0], endpoints[1],
                         selected_endpoints[0], selected_endpoints[1], selected_endpoints[2])

    return network


if __name__ == '__main__':

    pass
