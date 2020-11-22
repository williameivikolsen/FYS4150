import os
import sys

# File that compiles and runs c++ codes, plotting resulting data.

# ------------- Compilation -------------
all_cpp_codes = "./*.cpp"
os.system("echo compiling...")
os.system("g++ -O3 -fopenmp -o main.exe" + " " + all_cpp_codes)
# ---------------------------------------

cycles = 1000000
random_config = 1
threads = 12

header_str = " Lattice size L  Temperature T      MC Cycles          <E>/N          <M>/N            C_V            chi        Threads       Time (s)"
os.system(f'echo "{header_str}"  >> results.txt')

for L in [40, 60, 80, 100]:
    for T in [2.0, 2.05, 2.1, 2.15, 2.2, 2.25, 2.3]:
        os.system("echo  ")
        os.system("echo executing for L = " + str(L) + ", T = " + str(T) + "...")
        os.system("./main.exe " + str(L) + " " + str(T) + " " + str(cycles) + " " + str(random_config) + " " + str(threads))    # Execute code

# new_name = "phase_transitions.txt"
# os.rename("results.txt", new_name)
# os.system("mv " + new_name +  " results")           # Move data to results directory.
