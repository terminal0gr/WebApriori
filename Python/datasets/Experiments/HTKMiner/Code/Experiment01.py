from concurrent.futures import ProcessPoolExecutor

# Define a costly function
def costly_operation(value):
    return [x**2 for x in value]  # Example of a costly computation


# It is vital for the parallel proccessings
if __name__ == '__main__':

    # Example dictionary
    data = {
        "key1": [1, 2, 3],
        "key2": [4, 5, 6],
        "key3": [7, 8, 9]
    }

    # Parallel processing
    with ProcessPoolExecutor() as executor:
        # Map each dictionary value to the costly operation
        result = {key: result for key, result in zip(data.keys(), executor.map(costly_operation, data.values()))}

    print(result)