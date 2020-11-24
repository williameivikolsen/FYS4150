## 🎲 FYS4150 - Project 4: Studies of Phase Transitions in Magnetic Systems 🧲

The files in this folder solves the [given assignment](http://compphysics.github.io/ComputationalPhysics/doc/Projects/2020/Project4/pdf/Project4.pdf).

The simulations are performed with the class IsingModel as defined in `IsingModel.hpp` and `IsingModel.cpp`.

The main program `main.cpp` takes in command line arguments for the lattice length `L`, temperature `T`, number of cycles `cycles`, an initial spin configuration variable `random_config`, the number of threads `threads` and a cutoff fraction `cutoff_fraction` for calculating expectation values, a choice for printing out the final spin state `write_final_spins` and a choice of printing the lattice energy after computing cycles `write_energy_distribution`. The following example makefile compiles and executes the program:
``` Ruby
all: compile execute

compile:
	g++ -fopenmp -o main.exe main.cpp IsingModel.cpp

execute:
	./main.exe 100 2.4 100000 1 12 0.1 0 0 
```
With the above execution, main.cpp takes in `L = 100`, `T = 2.4`, `cycles = 1000`, `random_config = 1`, `threads = 12`, `cutoff_fraction = 0.1`, `write_final_spins = 0` and `write_energy_distribution = 0`.

The main program then creates an instance of the class `IsingModel`, and goes on to perform the calculations using the Metropolis Monte Carlo method. If the number of threads is set to 1, everything is run on a single thread. If not, the OpenMP API is used to parallelize and run the calculations on the chosen number of threads.

The final results containing the expectation values of energy, magnetization, heat capacity and susceptibility are written to a file `results.txt`. This file also includes information about the time used to run the simulation.

The other Python files in the folder are used to the generate data and plots found in the report file `Project4.pdf`.
