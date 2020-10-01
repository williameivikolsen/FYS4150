import os
import numpy as np

# File that runs main.cpp for system "beam", with large range of n.

# Standard parameters:
system = "beam"
maxit = "100000"
epsilon = "1e-8"

n_array_float = np.logspace(1,3,31)
n_array_int = np.round(n_array_float).astype(int)

for i in range(len(n_array_int)):
    print("Executing for n = " + str(n_array_int[i]))
    n = str(n_array_int[i])
    filename = system + "_" + n + ".txt"
    path = "./" + system
    os.system("echo executing...")
    os.system("./main.exe" + " " + system + " " + n + " " + epsilon + " " + maxit + " " + filename)

    if not os.path.exists(path):
        os.makedirs(path)                               #Creates the directory
    os.system("mv" + " " + filename + " " + path)   # Move data file to results directory.