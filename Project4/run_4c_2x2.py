import os
import sys
import numpy as np

# This file compares numerical and analytical values of the L=2 lattice

# ------------- Compilation -------------
all_cpp_codes = "./*.cpp"
os.system("echo compiling...")
os.system("g++-10 -O3 -fopenmp -o main.exe" + " " + all_cpp_codes) # mac OS friendly
#os.system("g++ -O3 -fopenmp -o main.exe" + " " + all_cpp_codes) # Linux friendly
# ---------------------------------------

L = 2                   # Size system
T = 1.0                 # Temperature in unit [J/k]
threads = 1             # Number of threads
cutoff_fraction = 0.1   # Fraction of first samples to skip
bool_write_spins = 0    # 1 for writing spin matrix to file, 0 for not
bool_write_energies = 0 # 1 for writing energies to file, 0 for not
bool_random_config = 0  # 1 for random initial spin config, 0 for spin ordered in same direction

beta = 1/T
Z = 4*np.cosh(8*beta) + 12      #The partition function

#Calculating the analytical mean values
analytical_E = -32*np.sinh(8*beta)/Z
analytical_E2 = 256*np.cosh(8*beta)/Z
analytical_absM = 8*(np.exp(8*beta)+2)/Z
analytical_M2 = 32*(np.exp(8*beta)+1)/Z

CV = (analytical_E2 - analytical_E**2)/(T**2)         # Heat capacity
chi = (analytical_M2 - analytical_absM**2)/(T)        # Susceptibility

print('E = ', analytical_E/L**2)
print('|M| = ', analytical_absM/L**2)
print('C_V = ', CV/L**2)
print('chi = ', chi/L**2)

header_str = " Lattice size L  Temperature T      MC Cycles          <E>/N          <M>/N            C_V            chi        Threads       Time (s)   Accept. rate"


cycles = [1e4,1e6,1e8]
for cycle in cycles:
    os.system(f'echo "{header_str}"  >> results.txt')
    os.system("echo  ")
    os.system("./main.exe " + str(L) + " " + str(T) + " " + str(int(cycle)) + " " + str(bool_random_config) + " " + str(threads) + " " + str(cutoff_fraction) + " " + str(bool_write_spins) + " " + str(bool_write_energies))
    new_name = "2x2_cycles_" + str(int(cycle)) + ".txt"
    os.rename("results.txt", new_name)
    os.system("mv " + new_name +  " results")           # Move data to results directory.

os.chdir("./results/")


for cycle in cycles:
    data = np.loadtxt("2x2_cycles_" + str(int(cycle)) + ".txt", skiprows = 1)
    E_diff = abs(analytical_E/L**2 - data[3])
    M_diff = abs(analytical_absM/L**2 - data[4])
    Cv_diff = abs(CV/L**2 - data[5])
    chi_diff = abs(chi/L**2 - data[6])
    print('E = ', format(E_diff,".2E"), 'for number of cycles=', int(cycle))
    print('|M| = ',format(M_diff,".2E"))
    print('C_V = ', format(Cv_diff,".2E"))
    print('chi = ', format(chi_diff,".2E"))
