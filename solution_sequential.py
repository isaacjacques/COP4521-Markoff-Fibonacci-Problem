"""
Name:Isaac Jacques
Date:2025-09-09
Assignment: Module3 Properly Design and Build a Solution Using Events
Due Date:2025-09-14
About this project: Display all the Markoff-Fibonacci Numbers, less than 750,  using sequential processing
Assumptions: 
All work below was performed by Isaac Jacques
"""
import argparse

def markoff(max: int) -> list[int]:
    result = set()

    for x in range(1, max + 1):
        for y in range(x, max + 1):
            for z in range(y, max + 1):
                if x*x + y*y + z*z == 3*x*y*z:
                    result.update([x, y, z])

    return sorted(result)

def fibonacci(max: int) -> list[int]:
    result = list()
    
    i=0
    j=1
    result.append(i)
    result.append(j)
    while(True):
        new=i+j
        if(new>max):
            break
        result.append(new)
        i=j
        j=new
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Display all the Markoff-Fibonacci Numbers using sequential processing")
    parser.add_argument(
        "-n", "--n",
        type=int,
        default=750,        
        help="Display all the Markoff-Fibonacci Numbers up to this number (def: 750)"
    )
    args = parser.parse_args()

    union = sorted(set(markoff(args.n)) & set(fibonacci(args.n)))
    print(union)