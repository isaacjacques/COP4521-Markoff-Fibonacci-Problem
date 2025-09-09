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
import threading

def markoff(x_start, x_end, max, out_set, lock, done_evt):
    result = set()
    for x in range(x_start, x_end):
        for y in range(x, max + 1):
            for z in range(y, max + 1):
                if x * x + y * y + z * z == 3 * x * y * z:
                    result.update((x, y, z))
    with lock:
        out_set.update(result)
    done_evt.set()


def fibonacci(max: int):
    if(max<0): return []

    result = [0]
    if(max==0): return result

    result.append(1)
    i,j=0,1
    while(True):
        new=i+j
        if(new>max):
            break
        result.append(new)
        i=j
        j=new
    return result


def fibonacci_worker(max, out_list, done_evt):
    fibs = fibonacci(max)
    out_list[:] = fibs
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
        parser = argparse.ArgumentParser(description="Display all the Markoff-Fibonacci Numbers using events + threads")
        parser.add_argument(
            "-n", "--n",
            type=int,
            default=750,        
            help="Display all the Markoff-Fibonacci Numbers up to this number (def: 750)"
        )
        args = parser.parse_args()
        max = args.n

    result_markoff= set()
    result_fib= []

    lock = threading.Lock()
    done_evts_markoff = [threading.Event() for _ in range(3)]
    done_evt_fib= threading.Event()

    #Create and start Markoff threads here
    ranges = partition(max, 3)
    threads_markoff = []
    for idx, (start, end) in enumerate(ranges):
        t = threading.Thread(
            target=markoff,
            args=(start, end, max, result_markoff, lock, done_evts_markoff[idx]),
            name=f"markoff-{idx+1}",
            daemon=True,
        )
        t.start()
        threads_markoff.append(t)


    #Create and start Fibonacci thread here
    thread_fib = threading.Thread(
        target=fibonacci_worker,
        args=(max, result_fib, done_evt_fib),
        name="fibonacci",
        daemon=True,
    )
    thread_fib.start()

    # WAit for threads to end
    for evt in done_evts_markoff:
        evt.wait()
    done_evt_fib.wait()
    for t in threads_markoff:
        t.join()
    thread_fib.join()

    # Results 
    result = sorted(result_markoff.intersection(result_fib))
    print(result)


if __name__ == "__main__":
    main()