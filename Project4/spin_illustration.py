import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# This file illustrates spin configurations for different situations
T1 = 1.0                # Temp below Tc
T2 = 2.4                # Temp above Tc
cycles1 = 0
cycles2 = 1e2
cycles3 = 1e5


def produce_new_data():

    # ------------- Compilation -------------
    all_cpp_codes = "./*.cpp"
    os.system("echo compiling...")
    os.system("g++-10 -O3 -fopenmp -o main.exe" + " " + all_cpp_codes) # mac OS friendly
    # os.system("g++ -O3 -fopenmp -o main.exe" + " " + all_cpp_codes) # Linux friendly
    # ---------------------------------------

    L = 80                 # Size system
    threads = 4
    cutoff_fraction = 0.1   #
    bool_write_spins = 1
    bool_write_energies = 0
    bool_random_config = 1


    for temp in [T1,T2]:
        for cycle in [cycles1,cycles2,cycles3]:
            os.system("./main.exe " + str(L) + " " + str(temp) + " " + str(int(cycle)) + " " + str(bool_random_config) + " " + str(threads) + " " + str(cutoff_fraction) + " " + str(bool_write_spins) + " " + str(bool_write_energies))
            #os.system("./main.exe " + str(L) + " " + str(T2) + " " + str(int(cycles)) + " " + str(bool_random_config) + " " + str(threads) + " " + str(cutoff_fraction) + " " + str(bool_write_spins) + " " + str(bool_write_energies))
            os.system("rm results.txt")     # We are not interested in keeping the main results file for this task
            newname = "spins_T_" + str(temp) + "_cycles_" + str(cycle) + ".txt"
            os.rename("spins.txt", newname)
            os.system("mv " + newname + " results")           # Move data to results directory.


# -------------------- Load data --------------------

#produce_new_data()

os.chdir("./results/")


i = 1

plt.style.use('seaborn')
sns.set(font_scale=1.3)
plt.subplots(2,3)
for temp in [T1,T2]:
    for cycle in [cycles1,cycles2,cycles3]:
        data = np.loadtxt("spins_T_" + str(temp) + "_cycles_" + str(cycle) + ".txt")
        plt.subplot(2,3,i)
        #plt.title("temp=" + str(temp) + "cycles = " + str(int(cycle)))
        plt.imshow(data, cmap ='tab20b')
        if i ==1:
            plt.ylabel(r'$T = 1.0$ [k/J]')
        if i == 4:
            plt.xlabel(r'$c = 0$')
            plt.ylabel(r'$T = 2.4$ [k/J]')
        if i == 5:
            plt.xlabel(r'$c = 10^2$')
        if i == 6:
            plt.xlabel(r'$c = 10^5$')
        #plt.axis('off')
        plt.xticks([])
        plt.yticks([])
        i += 1

plt.tight_layout()
os.chdir("../plots/")
plt.savefig("spins.pdf",dpi=300)
plt.show()
