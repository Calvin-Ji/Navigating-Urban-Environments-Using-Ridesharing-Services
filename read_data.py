"""
CSC111 Winter 2023 Course Project

By: Gerald Wang, Mark Estiller, Calvin Ji, Dharma Ong

This file contains functions that will read the dataset and output it in a format
that can be used for the computations.

Copyright and Usage Information
===============================
This file is Copyright (c) 2023 by Gerald Wang, Mark Estiller, Calvin Ji, Dharma Ong.
This module is expected to use data from:
https://www.kaggle.com/datasets/zusmani/uberdrives
"My Uber Drives" by user Zeeshan-Ul-Hassan Usmani. The data encompassed his Uber drives
in 2016 (1,175 drives total), and it was presented as a csv with the following columns going from left to right:
start date, end date, category, start, stop, number of miles, and purpose.
"""

from __future__ import annotations
import datetime


def read_csv(file_name: str) -> list[tuple[float, str, str, float]]:
    """ Reads the csv file and returns a list of tuples of (time, start_loc, stop_loc, distance)

    time is a float representing the amount of time taken in seconds
    start_loc is a string representing the starting neighborhood
    stop_loc is a string representing the stopping neighborhood
    distance is a float representing the distance travelled in miles

    Precondition:
    - file_name != ''
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
        'disable': ['E9992', 'E9997', 'E9999', 'E9998', 'R0914']
    })
