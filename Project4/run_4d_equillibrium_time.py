import os
import sys
import numpy as np
import matplotlib.pyplot as plt

# File that compiles and runs c++ codes, plotting resulting data.

# ------------- Compilation -------------
all_cpp_codes = "./*.cpp"
os.system("echo compiling...")
# os.system("g++-10 -O3 -fopenmp -o main.exe" + " " + all_cpp_codes) # mac OS friendly
os.system("g++ -O3 -fopenmp -o main.exe" + " " + all_cpp_codes) # Linux friendly
# ---------------------------------------


""" -------------------- Load data --------------------  """

def produce_new_data():
    L = 20                  # Size system
    T1 = 1.0                # Temp below Tc
    T2 = 2.4                # Temp above Tc
    threads = 12    
    cutoff_fraction = 0.0   # For this test: Don't cut away any results!

    header_str = " Lattice size L  Temperature T      MC Cycles          <E>/N          <M>/N            C_V            chi        Threads       Time (s)"
   
    # Choose values for cycles linspace
    start_cycle = 10
    end_cycle = 1e6
    steps = 80

    # First make system with random initialization
    random_config = 1
    os.system(f'echo "{header_str}"  >> results.txt')
    for i, cycles in enumerate(np.linspace(start_cycle, end_cycle, steps), start=1):
        os.system("echo  ")
        os.system("echo execution " + str(i) + "/"  + str(steps) +  "...")
        os.system("./main.exe " + str(L) + " " + str(T1) + " " + str(int(cycles)) + " " + str(random_config) + " " + str(threads) + " " + str(cutoff_fraction))
        os.system("./main.exe " + str(L) + " " + str(T2) + " " + str(int(cycles)) + " " + str(random_config) + " " + str(threads) + " " + str(cutoff_fraction))

    new_name = "4d_equillibrium_time_random.txt"
    os.rename("results.txt", new_name)
    os.system("mv " + new_name +  " results")           # Move data to results directory.

    # Then make system with aligned initialization
    random_config = 0
    os.system(f'echo "{header_str}"  >> results.txt')
    for i, cycles in enumerate(np.linspace(start_cycle, end_cycle, steps), start=1):
        os.system("echo  ")
        os.system("echo execution " + str(i) + "/"  + str(steps) +   "...")
        os.system("./main.exe " + str(L) + " " + str(T1) + " " + str(int(cycles)) + " " + str(random_config) + " " + str(threads) + " " + str(cutoff_fraction))
        os.system("./main.exe " + str(L) + " " + str(T2) + " " + str(int(cycles)) + " " + str(random_config) + " " + str(threads) + " " + str(cutoff_fraction))

    new_name = "4d_equillibrium_time_aligned.txt"
    os.rename("results.txt", new_name)
    os.system("mv " + new_name +  " results")           # Move data to results directory.


# If not data doesn't already exist, run simulation
path1 = "./results/4d_equillibrium_time_aligned.txt"
path2 = "./results/4d_equillibrium_time_random.txt"
if not os.path.exists(path1) or not os.path.exists(path2) :
    print("Simulation data not found in results subfolder. Running simulations...")
    produce_new_data()
# If they to, give choice to remake data
else:
    remake_prompt = input("Found a set of usable data in results subfolder, this will be used by default. If you'd rather remake data, press 'Y' ")
    if remake_prompt == "Y" or remake_prompt == "y":
        print("Running simulations...")
        produce_new_data()
    else:
        print("Using existing data.")

""" -------------------- Plot --------------------  """

plt.style.use('seaborn')
os.chdir('./results')

data_aligned = np.loadtxt('4d_equillibrium_time_aligned.txt', skiprows=1)
T, cycles, E_aligned = data_aligned[:, 1], data_aligned[:, 2], data_aligned[:, 3]

data_random = np.loadtxt('4d_equillibrium_time_random.txt', skiprows=1)
E_random = data_random[:, 3]

Tvals = [2.4]
idx_dict = {i: np.where(T == i) for i in Tvals}
print(idx_dict)
for T in Tvals:
    idx = idx_dict[T]
    plt.plot(cycles[idx], E_aligned[idx], '-o', label='Aligned initialization')
    plt.plot(cycles[idx], E_random[idx], '-o', label='Random initialization')
# plt.xlabel(r'$T$')
# plt.ylabel(r'$\langle|M|\rangle/L^2$')
plt.legend()
plt.show()
print("Made it here!!!!!!!")