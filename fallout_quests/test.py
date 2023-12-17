from multiprocessing.dummy import Pool
import os
print(os.cpu_count())

def multiply_arguments(args):
    # Unpack the arguments
    x, y = args
    result = x * y
    return result

if __name__ == "__main__":
    # Create a thread pool with, for example, 4 worker threads
    with Pool(processes=4) as pool:
        arguments_list = []
        for i in range(5):
            arguments_list.append((i, i),)        
        # List of argument tuples
        # arguments_list = [(1, 2), (3, 4), (5, 6), (7, 8), (9, 10)]

        # Use pool.map to apply the function to each tuple of arguments
        result = pool.map(multiply_arguments, arguments_list)

    # result now contains the results of the function applied to each set of arguments
    print(result)