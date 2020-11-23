import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import seaborn

# This file solves solves task 4e of the assignment. 

def produce_new_data():

    # ------------- Compilation -------------
    all_cpp_codes = "./*.cpp"
    os.system("echo compiling...")
    # os.system("g++-10 -O3 -fopenmp -o main.exe" + " " + all_cpp_codes) # mac OS friendly
    os.system("g++ -O3 -fopenmp -o main.exe" + " " + all_cpp_codes) # Linux friendly
    # ---------------------------------------

    L = 20                  # Size system
    T1 = 1.0                # Temp below Tc
    T2 = 2.4                # Temp above Tc
    cycles = 1e5
    threads = 12    
    cutoff_fraction = 0.0   # For this test: Don't cut away any results!
    bool_write_spins = 0
    bool_write_energies = 0
    bool_random_config = 1

    os.system("./main.exe " + str(L) + " " + str(T1) + " " + str(int(cycles)) + " " + str(bool_random_config) + " " + str(threads) + " " + str(cutoff_fraction) + " " + str(bool_write_spins) + " " + str(bool_write_energies))
    os.system("./main.exe " + str(L) + " " + str(T2) + " " + str(int(cycles)) + " " + str(bool_random_config) + " " + str(threads) + " " + str(cutoff_fraction) + " " + str(bool_write_spins) + " " + str(bool_write_energies))

    os.system("rm results.txt")     # We are not interested in keeping the main results file for this task


""" -------------------- Load data --------------------  """

# If not data doesn't already exist, run simulation
path = "./results/4e_probability_density.txt"
if not os.path.exists(path):
    print("Simulation data not found in results subfolder. Running simulations...")
    produce_new_data()

# If they do, give choice to remake data
else:
    remake_prompt = input("Found a set of usable data in results subfolder, this will be used by default. If you'd rather remake data, press 'Y' ")
    if remake_prompt == "Y" or remake_prompt == "y":
        print("Running simulations...")
        produce_new_data()
    else:
        print("Using existing data.")


""" -------------------- Plot --------------------  """

plt.style.use('seaborn')
seaborn.set(font_scale=1.3)
os.chdir('./results')

# data_aligned = np.loadtxt('4d_equilibrium_time_aligned.txt', skiprows=1)
# T, cycles, E_aligned, acceptancerate_aligned = data_aligned[:, 1], data_aligned[:, 2], data_aligned[:, 3], data_aligned[:,9]

# data_random = np.loadtxt('4d_equilibrium_time_random.txt', skiprows=1)
# E_random, acceptancerate_random = data_random[:, 3], data_random[:,9]


# T1 = 1.0    # Temp below Tc
# T2 = 2.4    # Temp above Tc

# idx_dict = {i: np.where(T == i) for i in [T1, T2]}
    
# Figure 1: Energies for T = 1
# plt.figure(1)
# plt.plot(cycles[idx_dict[T1]], E_aligned[idx_dict[T1]], '-o', label='Aligned initialization')
# plt.plot(cycles[idx_dict[T1]], E_random[idx_dict[T1]], '-o', label='Random initialization')
# plt.xlabel("Monte Carlo cycles")
# plt.ylabel(r'Average energy per spin $\langle E\rangle/L^2$ [J]')
# plt.xscale('log')
# plt.legend()
# plt.tight_layout()
# plt.savefig("4d_equilibrium_time_lowT_energy.pdf")
# os.system("mv 4d_equilibrium_time_lowT_energy.pdf ../plots")

# Show produced plots
# plt.show()