import os
import sys
import numpy as np

# File that compiles and runs c++ codes, plotting resulting data.

# ------------- Compilation -------------
all_cpp_codes = "./*.cpp"
os.system("echo compiling...")
os.system("g++-10 -O3 -fopenmp -o main.exe" + " " + all_cpp_codes) # mac OS friendly
#os.system("g++ -O3 -fopenmp -o main.exe" + " " + all_cpp_codes) # Linux friendly
# ---------------------------------------

L = 2
T = 1.0
beta = 1/T
random_config = 0
cycles = 1e9
threads = 1

Z = 4*np.cosh(8*beta) + 12      #The partition function for A

#Calculating the analytical mean values
analytical_E = -32*np.sinh(8*beta)/Z
analytical_E2 = 256*np.cosh(8*beta)/Z
analytical_absM = 8*(np.exp(8*beta)+2)/Z
analytical_M2 = 32*(np.exp(8*beta)+1)/Z

CV = (analytical_E2 - analytical_E**2)/(T**2*L**2)         # Heat capacity
chi = (analytical_M2 - analytical_absM**2)/(T*L**2)        # Susceptibility

print('E = ', analytical_E/4)
print('|M| = ', analytical_absM/4)
print('C_V = ', CV)
print('chi = ', chi)


header_str = " Lattice size L  Temperature T      MC Cycles          <E>/N          <M>/N            C_V            chi        Threads       Time (s)"
os.system(f'echo "{header_str}"  > results .txt')

os.system("echo  ")
os.system("./main.exe " + str(L) + " " + str(T) + " " + str(int(cycles)) + " " + str(random_config) + " " + str(threads))    # Execute code

new_name = "2x2.txt"
os.rename("results.txt", new_name)
os.system("mv " + new_name +  " results")           # Move data to results directory.

os.chdir("./results/")
data = open('2x2.txt','r')
for line in data:
    print(line)
