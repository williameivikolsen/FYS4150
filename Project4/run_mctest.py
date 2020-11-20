import os
import sys
import numpy as np

# File that compiles and runs c++ codes, plotting resulting data.

# ------------- Compilation -------------
all_cpp_codes = "./*.cpp"
os.system("echo compiling...")
os.system("c++ -o main.exe" + " " + all_cpp_codes)
# ---------------------------------------

L = 20
T = 1.0
i = 1

for cycles in np.logspace(2, 6, 100):
    os.system("echo  ")
    os.system("echo execution " + str(i) + "...")
    os.system("./main.exe " + str(L) + " " + str(T) + " " + str(int(cycles)))    # Execute code
    i += 1

new_name = "mctest.txt"
os.rename("results.txt", new_name)
os.system("mv " + new_name +  " results")           # Move data to results directory.
