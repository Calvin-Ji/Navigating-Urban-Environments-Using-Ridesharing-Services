import read_data
import classes
import computations

# Test graph to see if find shortest path works
def run_find_best_path_for_key() -> None:
    data = read_data.read_csv("data/large_test.csv")
    get_dictionary = computations.get_avg_times_and_miles(data)
    generated_graph = read_data.create_graph_from_read_csv(get_dictionary)

    

    

if __name__ == '__main__':
    run_find_best_path_for_key()