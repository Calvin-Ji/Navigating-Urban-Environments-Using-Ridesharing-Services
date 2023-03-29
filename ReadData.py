import datetime
from math import pi, inf #This is for the estimate size function - Calvin

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

            # print(start_time)
            temp = start_time.split()
            # print(temp)
            date_params = temp[0].split('/')
            # print(date_params)
            time_params = temp[1].split(':')
            # print(time_params)

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

            # print(time_delta)
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


def estimate_county_size(county_name: str, data: dict[tuple[str]:list[float]]) -> float:
    """Make a very rough estimate of of the county size in miles squared and return it.
    We can first assume that the county is a perfect sphere and assume that on average that the start
    location is in the middle of the county. We could find the average distance 
    from the city whose area we are trying to approximate to every other city that it is connected to. 
    We take the smallest average distance because presumably that would be the closest city that is 
    nearby, and that could be a guess for our radius."""
    # lower_radius = 0
    # for set_of_county_names in data:
    #     if set_of_county_names == (county_name, county_name):
    #         lower_radius = data[set_of_county_names][1]
    # lower_bound = pi * (lower_radius) ** 2

    avg_distances_to_cities = [inf]
    for set_of_county_names in data:
        if county_name in set_of_county_names and set_of_county_names != (county_name, county_name):
            avg_distances_to_cities.append(data[set_of_county_names][1])
    upper_radius = min(avg_distances_to_cities)
    upper_bound = pi * (upper_radius) ** 2

    return upper_bound



if __name__ == '__main__':
    #print(read_csv('data/large_test.csv'))
    print(estimate_county_size("Midtown", get_avg_times_and_miles(read_csv('data/My Uber Drives - 2016.csv'))))
