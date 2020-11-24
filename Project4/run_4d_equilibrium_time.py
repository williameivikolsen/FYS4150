import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import seaborn

# This file solves solves task 4d of the assignment. 

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
    threads = 12    
    cutoff_fraction = 0.0   # For this test: Don't cut away any results!
    bool_write_spins = 0
    bool_write_energies = 0

    header_str = " Lattice size L  Temperature T      MC Cycles          <E>/N          <M>/N            C_V            chi        Threads       Time (s)   Accept. rate"
   
    # Choose values for cycles linspace
    start_cycle = 3     # Exponent of 10 (used in logspace)
    end_cycle = 6       # Exponent of 10 (used in logspace)
    steps = 100

    # First make system with random initialization
    random_config = 1
    os.system(f'echo "{header_str}"  > results.txt')
    for i, cycles in enumerate(np.logspace(start_cycle, end_cycle, steps), start=1):
        os.system("echo  ")
        os.system("echo execution " + str(i) + "/"  + str(steps) +  "...")
        os.system("./main.exe " + str(L) + " " + str(T1) + " " + str(int(cycles)) + " " + str(random_config) + " " + str(threads) + " " + str(cutoff_fraction) + " " + str(bool_write_spins) + " " + str(bool_write_energies))
        os.system("./main.exe " + str(L) + " " + str(T2) + " " + str(int(cycles)) + " " + str(random_config) + " " + str(threads) + " " + str(cutoff_fraction) + " " + str(bool_write_spins) + " " + str(bool_write_energies))

    new_name = "4d_equilibrium_time_random.txt"
    os.rename("results.txt", new_name)
    os.system("mv " + new_name +  "./results")           # Move data to results directory.

    # Then make system with aligned initialization
    random_config = 0
    os.system(f'echo "{header_str}"  > results.txt')
    for i, cycles in enumerate(np.logspace(start_cycle, end_cycle, steps), start=1):
        os.system("echo  ")
        os.system("echo execution " + str(i) + "/"  + str(steps) +   "...")
        os.system("./main.exe " + str(L) + " " + str(T1) + " " + str(int(cycles)) + " " + str(random_config) + " " + str(threads) + " " + str(cutoff_fraction) + " " + str(bool_write_spins) + " " + str(bool_write_energies))
        os.system("./main.exe " + str(L) + " " + str(T2) + " " + str(int(cycles)) + " " + str(random_config) + " " + str(threads) + " " + str(cutoff_fraction) + " " + str(bool_write_spins) + " " + str(bool_write_energies))

    new_name = "4d_equilibrium_time_aligned.txt"
    os.rename("results.txt", new_name)
    os.system("mv " + new_name +  " results")           # Move data to results directory.

""" -------------------- Load data --------------------  """

# If not data doesn't already exist, run simulation
path1 = "./results/4d_equilibrium_time_aligned.txt"
path2 = "./results/4d_equilibrium_time_random.txt"
if not os.path.exists(path1) or not os.path.exists(path2) :
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
seaborn.set(font_scale=1)
os.chdir('./results')

data_aligned = np.loadtxt('4d_equilibrium_time_aligned.txt', skiprows=1)
T, cycles, E_aligned, M_aligned, acceptancerate_aligned = data_aligned[:, 1], data_aligned[:, 2], data_aligned[:, 3], data_aligned[:,4], data_aligned[:,9]

data_random = np.loadtxt('4d_equilibrium_time_random.txt', skiprows=1)
E_random, M_random, acceptancerate_random = data_random[:, 3], data_random[:,4], data_random[:,9]


T1 = 1.0    # Temp below Tc
T2 = 2.4    # Temp above Tc

idx_dict = {i: np.where(T == i) for i in [T1, T2]}
    
# Figure 1: Energies
plt.figure(1,figsize=((6,6)))
plt.subplot(2,1,1)
plt.plot(cycles[idx_dict[T1]], E_aligned[idx_dict[T1]], '-o', label=r'Aligned init., $T$ = 1.0 $J/k$')
plt.plot(cycles[idx_dict[T1]], E_random[idx_dict[T1]], '-o', label=r'Random init., $T$ = 1.0 $J/k$')
plt.ylabel(r'$\langle E\rangle/N$ [J]')
plt.xscale('log')
plt.legend()

plt.subplot(2,1,2)
plt.plot(cycles[idx_dict[T2]], E_aligned[idx_dict[T2]], '-o', label=r'Aligned init., $T$ = 2.4 $J/k$')
plt.plot(cycles[idx_dict[T2]], E_random[idx_dict[T2]], '-o', label=r'Random init., $T$ = 2.4 $J/k$')
plt.ylabel(r'$\langle E\rangle/N$ [J]')
plt.xlabel("Monte Carlo cycles")
plt.xscale('log')
plt.legend()
plt.tight_layout()
plt.savefig("4d_equilibrium_time_energy.pdf")
os.system("mv 4d_equilibrium_time_energy.pdf ../plots")


# Figure 2: Magnetization
plt.figure(2,figsize=((6,6)))
plt.subplot(2,1,1)
plt.plot(cycles[idx_dict[T1]], M_aligned[idx_dict[T1]], '-o', label=r'Aligned init., $T$ = 1.0 $J/k$')
plt.plot(cycles[idx_dict[T1]], M_random[idx_dict[T1]], '-o', label=r'Random init., $T$ = 1.0 $J/k$')
plt.ylabel(r'$\langle |M|\rangle/N$ [1]')
plt.xscale('log')
plt.legend()

plt.subplot(2,1,2)
plt.plot(cycles[idx_dict[T2]], M_aligned[idx_dict[T2]], '-o', label=r'Aligned init., $T$ = 2.4 $J/k$')
plt.plot(cycles[idx_dict[T2]], M_random[idx_dict[T2]], '-o', label=r'Random init., $T$ = 2.4 $J/k$')
plt.ylabel(r'$\langle |M|\rangle/N$ [1]')
plt.xlabel("Monte Carlo cycles")
plt.xscale('log')
plt.legend()
plt.tight_layout()
plt.savefig("4d_equilibrium_time_magnetization.pdf")
os.system("mv 4d_equilibrium_time_magnetization.pdf ../plots")

# Figure 3: Acceptance rate
plt.figure(3,figsize=((6,6)))
plt.subplot(2,1,1)
plt.plot(cycles[idx_dict[T1]], acceptancerate_aligned[idx_dict[T1]], '-o', label=r'Aligned init., $T$ = 1.0 $J/k$')
plt.plot(cycles[idx_dict[T1]], acceptancerate_random[idx_dict[T1]], '-o', label=r'Random init., $T$ = 1.0 $J/k$')
plt.ylabel(r'Acceptance rate')
plt.xscale('log')
plt.legend()

plt.subplot(2,1,2)
plt.plot(cycles[idx_dict[T2]], acceptancerate_aligned[idx_dict[T2]], '-o', label=r'Aligned init., $T$ = 2.4 $J/k$')
plt.plot(cycles[idx_dict[T2]], acceptancerate_random[idx_dict[T2]], '-o', label=r'Random init., $T$ = 2.4 $J/k$')
plt.ylabel(r'Acceptance rate')
plt.xlabel("Monte Carlo cycles")
plt.xscale('log')
plt.legend()
plt.tight_layout()
plt.savefig("4d_equilibrium_time_acceptance.pdf")
os.system("mv 4d_equilibrium_time_acceptance.pdf ../plots")

# Show produced plots
plt.show()