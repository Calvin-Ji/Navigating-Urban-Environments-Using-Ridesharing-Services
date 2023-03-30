import datetime
import math  # This is for the estimate size function - Calvin
import computations
import numpy as np


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


def get_avg_times_and_miles(l: list[tuple[float, str, str, float]]) -> dict[tuple[str, str]:list[float]]:
    """Return a dictionary where a set of 2 endpoints are keys and the list containing the
    average time at index 0 and average distance at index 1."""
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
        final_dict[(start, stop)] = [avg_time]

    for item in links_so_far_with_miles:
        avg_miles = sum(
            links_so_far_with_miles[item]) / len(links_so_far_with_miles[item])
        listy = item.split(':')
        start = listy[0]
        stop = listy[1]
        final_dict[(start, stop)] += [avg_miles]
    return final_dict


def data_to_np(data_dict: dict[tuple[str, str]: list[float]]) -> np.array:
    """
      0 1 2 3 4
    0 0 d d d d
    1 d 0 d d d
    2 d d 0 d d
    3 d d d 0 d
    4 d d d d 0
    """
    # first, we want to figure out the unique neighborhoods in a list
    index_mapping = {}
    index = 0

    print(data_dict)

    for key in data_dict:
        if key[0] not in index_mapping:
            index_mapping[key[0]] = index
            index += 1
        if key[1] not in index_mapping:
            index_mapping[key[1]] = index
            index += 1

    # print(index_mapping)
    # assert 'Palm Beach' in index_mapping
    # now, we want to initialize an np array
    size = len(index_mapping)
    array = np.zeros((size, size))
    # print(array)

    for key in data_dict:
        # print(key)
        distance = data_dict[key][1]
        x = index_mapping[key[0]]
        y = index_mapping[key[1]]

        # print(f'{x}   {y}')

        array[x][y] = distance
        array[y][x] = distance

    return array

    # def
if __name__ == '__main__':
    # print(read_csv('data/large_test.csv'))
    # print(computations.estimate_neighborhood_size("Sunnyside", get_avg_times_and_miles(
    #     read_csv('data/My Uber Drives - 2016.csv'))))

    # print(get_avg_times_and_miles(read_csv('data/My Uber Drives - 2016.csv')))

    np.set_printoptions(threshold=np.inf)
    print(data_to_np(get_avg_times_and_miles(
        read_csv('data/My Uber Drives - 2016.csv'))))

    # TODO: Path propagation
