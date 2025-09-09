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

def markoff(max):
    result = set()

    for x in range(1, max + 1):
        for y in range(x, max + 1):
            for z in range(y, max + 1):
                if x*x + y*y + z*z == 3*x*y*z:
                    result.update([x, y, z])

    return result

def fibonacci(max):
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

def main(max=None):
    if max is None:
        parser = argparse.ArgumentParser(description="Display all the Markoff-Fibonacci Numbers using sequential processing")
        parser.add_argument(
            "-n", "--n",
            type=int,
            default=750,        
            help="Display all the Markoff-Fibonacci Numbers up to this number (def: 750)"
        )
        args = parser.parse_args()
        max = args.n

    result_markoff = markoff(max)
    result_fib = fibonacci(max)

    result = sorted(result_markoff.intersection(result_fib))
    print(result)



if __name__ == "__main__":
    main()