import os
import sys

# File that compiles and runs c++ codes, plotting resulting data.

# ------------- Compilation -------------
all_cpp_codes = "./*.cpp"
os.system("echo compiling...")
os.system("g++ -O3 -fopenmp -o main.exe" + " " + all_cpp_codes)
# ---------------------------------------

cycles = 2e6
random_config = 1
threads = 12
cutoff_fraction = 0.1
bool_write_spins = 0
bool_write_energies = 0

header_str = " Lattice size L  Temperature T      MC Cycles          <E>/N          <M>/N            C_V            chi        Threads       Time (s)   Accept. rate"
os.system(f'echo "{header_str}"  > results.txt')

T_interval1 = [2.0 + 0.02*i for i in range(10)]     # [2.0, 2.2) 
T_interval2 = [2.2 + 0.004*i for i in range(50)]    # [2.2, 2.4)
T_interval3 = [2.4 + 0.02*i for i in range(11)]     # [2.4, 2.6]

T_total = T_interval1 + T_interval2 + T_interval3

for L in [40, 60, 80, 100]:
    for T in T_total:
        os.system("echo  ")
        os.system("echo executing for L = " + str(L) + ", T = " + str(T) + "...")
        os.system("./main.exe " + str(L) + " " + str(T) + " " + str(int(cycles)) + " " + str(random_config) + " " + str(threads) + " " + str(cutoff_fraction) + " " + str(bool_write_spins) + " " + str(bool_write_energies))

new_name = "phase_transitions.txt"
os.rename("results.txt", new_name)
os.system("mv " + new_name +  " results")           # Move data to results directory.
