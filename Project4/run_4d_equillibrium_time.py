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
    random_config = 1
    cutoff_fraction = 0.0   # For this test: Don't cut away any results!

    header_str = " Lattice size L  Temperature T      MC Cycles          <E>/N          <M>/N            C_V            chi        Threads       Time (s)"
    os.system(f'echo "{header_str}"  >> results.txt')

    for i, cycles in enumerate(np.linspace(10, 1e6, 100), start=1):
        os.system("echo  ")
        os.system("echo execution " + str(i) + "...")
        os.system("./main.exe " + str(L) + " " + str(T1) + " " + str(int(cycles)) + " " + str(random_config) + " " + str(threads) + " " + str(cutoff_fraction))
        os.system("./main.exe " + str(L) + " " + str(T2) + " " + str(int(cycles)) + " " + str(random_config) + " " + str(threads) + " " + str(cutoff_fraction))

    new_name = "4d_equillibrium_time.txt"
    os.rename("results.txt", new_name)
    os.system("mv " + new_name +  " results")           # Move data to results directory.


# If not data doesn't already exist, run simulation
path = "./results/4d_equillibrium_time.txt"
if not os.path.exists(path):
    print("Simulation data not found in results subfolder. Running simulations...")
    produce_new_data()
# If they to, give choice to remake data
else:
    remake_prompt = input("Found a set of usable data in results subfolder. Press 'Y' to remake data.")
    if remake_prompt == "Y" or remake_prompt == "y":
        print("Running simulations...")
        produce_new_data()
    else:
        print("Using existing data.")

""" -------------------- Plot --------------------  """

plt.style.use('seaborn')
os.chdir('./results')
data = np.loadtxt('4d_equillibrium_time.txt', skiprows=1)

L, T, E = data[:, 0], data[:, 1], data[:, 3]

Lvals = [40, 60, 80, 100]
idx_dict = {i: np.where(L == i) for i in Lvals}

for L in Lvals:
    idx = idx_dict[L]
    plt.plot(T[idx], E[idx], 'o', label='L = %i' % L)
plt.xlabel(r'$T$')
plt.ylabel(r'$\langle|M|\rangle/L^2$')
plt.legend()
plt.show()
print("Made it here!!!!!!!")