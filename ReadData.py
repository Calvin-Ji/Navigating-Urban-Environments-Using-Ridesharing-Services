import datetime


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


if __name__ == '__main__':
    print(read_csv('data/test.csv'))
