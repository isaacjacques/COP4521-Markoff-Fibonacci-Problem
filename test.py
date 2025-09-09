"""
Name:Isaac Jacques
Date:2025-09-09
Assignment: Module3 Properly Design and Build a Solution Using Events
Due Date:2025-09-14
About this project: Display all the Markoff-Fibonacci Numbers, less than 750, using events
Assumptions: 
All work below was performed by Isaac Jacques
"""
import argparse
import time
import solution_sequential
import solution_threads
import solution_multiprocessing


def run_and_time(func, n, label):
    start = time.perf_counter()
    func(n)
    end = time.perf_counter()
    print(f"{label} -> {end - start:.4f} seconds\n")


def main():
    parser = argparse.ArgumentParser(description="Display all the Markoff-Fibonacci Numbers using sequential processing")
    parser.add_argument(
        "-n", "--n",
        type=int,
        default=750,        
        help="Display all the Markoff-Fibonacci Numbers up to this number (def: 750)"
    )
    args = parser.parse_args()
    max = args.n

    print(f"Comparing implementations for when n={max}\n")

    run_and_time(solution_sequential.main, max, "Sequential solution")
    run_and_time(solution_threads.main, max, "Events + Threads solution")
    run_and_time(solution_multiprocessing.main, max, "Events + Processes solution")

if __name__ == "__main__":
    main()