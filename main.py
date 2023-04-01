import read_data
import classes
import computations

# Test graph to see if find shortest path works


def run_find_best_path_for_key() -> list:
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

    # generated_graph.initialize_distances()
    # generated_graph.initialize_times()
    # generated_graph.initialize_costs()

    generated_graph.find_best_path_for_key(
        'Fort Pierce', 'Downtown', computations.compute_path_distance)  # end neighborhood, set


if __name__ == '__main__':
    run_find_best_path_for_key()
