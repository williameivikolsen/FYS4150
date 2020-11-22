import os
import sys
import numpy as np

# File that compiles and runs c++ codes, plotting resulting data.

# ------------- Compilation -------------
all_cpp_codes = "./*.cpp"
os.system("echo compiling...")
os.system("g++ -O3 -fopenmp -o main.exe" + " " + all_cpp_codes)
# ---------------------------------------

L = 20
T = 1.0
random_config = 1

header_str = " Lattice size L  Temperature T      MC Cycles          <E>/N          <M>/N            C_V            chi        Threads       Time (s)"
os.system(f'echo "{header_str}"  >> results.txt')

for i, cycles in enumerate(np.logspace(2, 6, 100), start=1):
    os.system("echo  ")
    os.system("echo execution " + str(i) + "...")
    os.system("./main.exe " + str(L) + " " + str(T) + " " + str(int(cycles)) + " " + str(random_config) + " " + str(1))    # Execute code

for i, cycles in enumerate(np.logspace(2, 6, 100), start=1):
    os.system("echo  ")
    os.system("echo execution " + str(i) + "...")
    os.system("./main.exe " + str(L) + " " + str(T) + " " + str(int(cycles)) + " " + str(random_config) + " " + str(12))    # Execute code

new_name = "mctest.txt"
os.rename("results.txt", new_name)
os.system("mv " + new_name +  " results")           # Move data to results directory.
