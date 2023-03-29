import datetime
from math import pi #This is for the estimate size function - Calvin

def read_csv(file_name: str) -> tuple[float, str, str, float]:
    """ Reads the csv file and returns a tuple of (time, start_loc, stop_loc, distance)

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
                (time_delta.total_seconds(), start_loc, stop_loc, distance))

            # print(time_delta)
    return trip_data


def get_avg_times_and_miles(l: list[tuple[datetime.time, str, str, float]]) -> dict[set[str]:list[float]]:
    """Return a dictionary where a set of 2 endpoints are keys and the list containing the
    average time at index 0 and average distance at index 1 as keys."""
    links_so_far_with_times = {}
    links_so_far_with_miles = {}
    final_dict = {}
    for data in l:
        # Get all the times
        if links_so_far_with_times[f'{l[1]}:{l[2]}'] is None:
            links_so_far_with_times[f'{l[1]}:{l[2]}'] = [l[0]]
        links_so_far_with_times[f'{l[1]}:{l[2]}'] += [l[0]]
        # Get all the distances
        if links_so_far_with_miles[f'{l[1]}:{l[2]}'] is None:
            links_so_far_with_miles[f'{l[1]}:{l[2]}'] = [l[3]]
        links_so_far_with_miles[f'{l[1]} {l[2]}'] += [l[3]]

    for item in links_so_far_with_times:
        avg_time = sum(
            links_so_far_with_times[item]) / len(links_so_far_with_times[item])
        listy = item.split(':')
        start = listy[0]
        stop = listy[1]
        final_dict[{start, stop}] = [avg_time]

    for item in links_so_far_with_miles:
        avg_miles = sum(
            links_so_far_with_miles[item]) / len(links_so_far_with_miles[item])
        listy = item.split(':')
        start = listy[0]
        stop = listy[1]
        final_dict[{start, stop}] += [avg_miles]
    return final_dict


def estimate_county_size(county_name: str, data: dict[set[str]:list[float]]) -> tuple[float]:
    """Make a rough estimate of of the county size in miles squared and return it, where 
    the first float in the tuple is a lower bound and the second float in the tuple is a upper bound.
    We can assume that the county is a perfect sphere and assume that on average that the start
    location is in the middle of the county. So we get the average length of rides that start and 
    stop in the same city, and that is our lower bound for our radius. So lower bound of the area
    is the average length of rides that start and stop in the same city squared times pi (we could 
    approximate pi as 3.14 or use math.pi) Then for upper bound we could find the average distance 
    from the city whose area we are trying to approximate to every other city that it is connected to. 
    We take the smallest average distance because presumably that would be the closest city that is 
    nearby, and that could be a upper bound for our radius."""
    lower_radius = 0
    for set_of_county_names in data:
        if set_of_county_names == {county_name, county_name}:
            lower_radius = data[set_of_county_names][1]
    lower_bound = pi * (lower_radius) ** 2

    avg_distances_to_cities = [0]
    for set_of_county_names in data:
        if set_of_county_names.contains(county_name) and set_of_county_names != {county_name, county_name}:
            avg_distances_to_cities.append(data[set_of_county_names][1])
    upper_radius = min(avg_distances_to_cities)
    upper_bound = pi * (upper_radius) ** 2

    return (lower_bound, upper_bound)



if __name__ == '__main__':
    print(read_csv('data/test.csv'))