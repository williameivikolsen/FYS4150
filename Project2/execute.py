import os
import sys

# File that compiles and runs c++ codes, storing and plotting resulting data.

N = int(input("Give number of mesh points N: "))
system = input("Choose system: [beam/HO1/HO2]: ")
epsilon = float(input("Choose tolerance: "))
compile = input("Compile? [Y/N]: ")
if compile != "Y" and compile != "N":
    print('Command not recognized. Skipping compilation...')

all_cpp_codes = "./*.cpp"
compiler_flags = "-larmadillo"              # Linker to Armadillo.
if compile == "Y":
    os.system("echo compiling...")
    os.system("c++ -o main.out" + " " + all_cpp_codes + " " + compiler_flags)

os.system("echo executing...")
os.system("./main.exe")                     # Execute code