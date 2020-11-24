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
    threads = 1             # This task can only be ran single-threaded (will give error)
    cutoff_fraction = 0.1   # For this task: Keep cut-off at 10%
    bool_write_spins = 0
    bool_write_energies = 1 # Writes the total systems energy to text file "energies.txt"
    bool_random_config = 1

    os.system("echo executing...")
    # First make energy distribution for low temperature T = 1
    os.system("./main.exe " + str(L) + " " + str(T1) + " " + str(int(cycles)) + " " + str(bool_random_config) + " " + str(threads) + " " + str(cutoff_fraction) + " " + str(bool_write_spins) + " " + str(bool_write_energies))
    # Move results to subfolder
    os.system("mv 'energies.txt' './results/4e_probability_density_lowT.txt'")
    # Then make new distribution for high temperature T = 2.4
    os.system("./main.exe " + str(L) + " " + str(T2) + " " + str(int(cycles)) + " " + str(bool_random_config) + " " + str(threads) + " " + str(cutoff_fraction) + " " + str(bool_write_spins) + " " + str(bool_write_energies))
    # Move results to subfolder
    os.system("mv 'energies.txt' './results/4e_probability_density_highT.txt'")

    os.system("rm results.txt")     # We are not interested in keeping the main results file for this task


""" -------------------- Load data --------------------  """

# If not data doesn't already exist, run simulation

path1 = "./results/4e_probability_density_lowT.txt"
path2 = "./results/4e_probability_density_highT.txt"

if not os.path.exists(path1) or not os.path.exists(path2):
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

E_lowT = np.loadtxt('4e_probability_density_lowT.txt')
E_highT = np.loadtxt('4e_probability_density_highT.txt')

variance_lowT = np.var(E_lowT)
variance_highT = np.var(E_highT)


# Print variance of energies
print(f"Variance of energies T=1.0: {variance_lowT}")
print(f"Variance of energies T=2.4: {variance_highT}")   

# Make histogram
hist_lowT, bin_edges_lowT = np.histogram(E_lowT, bins=np.arange(min(E_lowT)-4, max(E_lowT)-4 + 8, 8))
hist_highT, bin_edges_highT = np.histogram(E_highT, bins=np.arange(min(E_highT)-4, max(E_highT)-4 + 8, 8))

# Scale for probability
prob_lowT = hist_lowT/float(hist_lowT.sum())
prob_highT = hist_highT/float(hist_highT.sum())

# Get mid points of each bin
bin_middles_lowT = (bin_edges_lowT[1:]+bin_edges_lowT[:-1])/2.0 
bin_middles_highT = (bin_edges_highT[1:]+bin_edges_highT[:-1])/2.0

# Compute the bin-width
bin_width_lowT = bin_edges_lowT[1] - bin_edges_lowT[0]
bin_width_highT = bin_edges_highT[1] - bin_edges_highT[0]

# Figure 1: Can finally make scaled histograms (as bar plots)
plt.figure(1)
plt.bar(bin_middles_lowT, prob_lowT, width=bin_width_lowT, label='$T$ = 1.0 $J/k$')
plt.bar(bin_middles_highT, prob_highT, width=bin_width_highT, label='$T$ = 2.4 $J/k$')
plt.xlabel(r'System energy $E$ [$J$]')
plt.ylabel(r'Probability')
plt.yticks(np.arange(0, 1, 0.1))
plt.legend()
plt.tight_layout()
plt.savefig("4e_probability_histogram.pdf")
os.system("mv 4e_probability_histogram.pdf ../plots")

# Show produced plots
plt.show()
