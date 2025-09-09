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
import multiprocessing as mp

def markoff(x_start, x_end, max, out_queue, done_evt):
    result = set()
    for x in range(x_start, x_end):
        for y in range(x, max + 1):
            for z in range(y, max + 1):
                if x * x + y * y + z * z == 3 * x * y * z:
                    result.update((x, y, z))
    out_queue.put(list(result))
    done_evt.set()


def fibonacci(max):
    if max < 0:
        return []
    result = [0]
    if max == 0:
        return result
    result.append(1)
    i, j = 0, 1
    while True:
        new = i + j
        if new > max:
            break
        result.append(new)
        i, j = j, new
    return result


def fibonacci_worker(max, out_queue, done_evt):
    fibs = fibonacci(max)
    out_queue.put(fibs)
    done_evt.set()

def partition(length, parts):
    if length < 1:
        return []
    
    base = length // parts
    remainder = length % parts
    ranges = []
    start = 1
    for i in range(parts):
        size = base + (1 if i < remainder else 0)
        end = start + size
        ranges.append((start, end))
        start = end
    return ranges

def main(max=None):
    if max is None:
        parser = argparse.ArgumentParser(description="Display all the Markoff-Fibonacci Numbers using events + multiprocessing")
        parser.add_argument(
            "-n", "--n",
            type=int,
            default=750,        
            help="Display all the Markoff-Fibonacci Numbers up to this number (def: 750)"
        )
        args = parser.parse_args()
        max = args.n

    queue_markoff = mp.Queue()
    queue_fib = mp.Queue()

    done_evts_markoff = [mp.Event() for _ in range(3)]
    done_evt_fib = mp.Event()


    #Create and start Markoff processes
    ranges = partition(max, 3)
    processes_markoff = []
    for idx, (start, end) in enumerate(ranges):
        p = mp.Process(
            target=markoff,
            args=(start, end, max, queue_markoff, done_evts_markoff[idx]),
            name=f"markoff-{idx+1}",
        )
        p.start()
        processes_markoff.append(p)

    #Create and start Fibonacci process
    process_fib = mp.Process(
        target=fibonacci_worker,
        args=(max, queue_fib, done_evt_fib),
        name="fibonacci",
    )
    process_fib.start()

    # Wait for processes to end
    for evt in done_evts_markoff:
        evt.wait()
    done_evt_fib.wait()

    result_markoff = set()
    for _ in range(3):
        payload = queue_markoff.get()
        result_markoff.update(payload)

    result_fib = queue_fib.get()

    for p in processes_markoff:
        p.join()
    process_fib.join()

    result = sorted(result_markoff.intersection(result_fib))
    print(result)


if __name__ == "__main__":
    main()