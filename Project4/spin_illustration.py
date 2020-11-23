import os
import sys
import numpy as np
import matplotlib.pyplot as plt

# File that compiles and runs c++ codes, plotting resulting data.

# ------------- Compilation -------------
all_cpp_codes = "./*.cpp"
os.system("echo compiling...")
os.system("g++-10 -O3 -fopenmp -o main.exe" + " " + all_cpp_codes)
# ---------------------------------------

# physical values and simulation values
L = 100
T = 2.5
random_config = 1
cycles = 100000
threads = 4

os.system("echo  ")
os.system("./main.exe " + str(L) + " " + str(T) + " " + str(cycles) + " " + str(random_config) + " " + str(threads))    # Execute code

os.system("mv " + "spins.txt" + " results")           # Move data to results directory.

os.chdir("./results/")
data = np.loadtxt('spins.txt')
print(data)

s = plt.imshow(data,cmap ='binary')
plt.axis('off')
#plt.colorbar(s) # black = spin up, white = spin down
plt.show()
