import os
import sys
import numpy as np

# File that compiles and runs c++ codes, plotting resulting data.

# ------------- Compilation -------------
all_cpp_codes = "./*.cpp"
os.system("echo compiling...")
os.system("g++ -O3 -fopenmp -o main.exe" + " " + all_cpp_codes)
# ---------------------------------------

L = 2
T = 1.0
cycles = 1000000

header_str = " Lattice size L  Temperature T      MC Cycles          <E>/N          <M>/N      C_V            chi              Threads       Time (s)"
os.system(f'echo "{header_str}"  >> results.txt')

os.system("echo  ")
os.system("./main.exe " + str(L) + " " + str(T) + " " + str(cycles) + " " + str(4))    # Execute code

new_name = "2x2.txt"
os.rename("results.txt", new_name)
os.system("mv " + new_name +  " results")           # Move data to results directory.
