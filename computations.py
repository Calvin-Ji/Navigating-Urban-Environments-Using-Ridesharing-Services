import math


def estimate_neighborhood_size(neighborhood_name: str, data: dict[tuple[str]:list[float]]) -> float:
    """
    Make a very rough estimate of of the neighborhood size in miles squared and return it.
    We can first assume that the neighborhood is a perfect circle and assume that on average that the start
    location is in the middle of the neighborhood. We could find the average distance 
    from the city whose area we are trying to approximate to every other city that it is connected to. 
    We take the smallest average distance because presumably that would be the closest city that is 
    nearby, and that could be a guess for our radius.

    Preconditions:
    - any(neighborhood_name in pair for pair in data)  # neighborhood_name exists in data
    """
    # lower_radius = 0
    # for set_of_neighborhood_names in data:
    #     if set_of_neighborhood_names == (neighborhood_name, neighborhood_name):
    #         lower_radius = data[set_of_neighborhood_names][1]
    # lower_bound = pi * (lower_radius) ** 2

    avg_distances_to_cities = [math.inf]
    for set_of_neighborhood_names in data:
        if neighborhood_name in set_of_neighborhood_names:
            avg_distances_to_cities.append(data[set_of_neighborhood_names][1])
    upper_radius = min(avg_distances_to_cities)
    upper_bound = math.pi * (upper_radius) ** 2

    return upper_bound
