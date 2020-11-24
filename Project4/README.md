## 🎲 FYS4150 - Project 4: Studies of Phase Transitions in Magnetic Systems 🧲

The files in this folder solves the [given assignment](http://compphysics.github.io/ComputationalPhysics/doc/Projects/2020/Project4/pdf/Project4.pdf).

The simulations are performed with the class IsingModel defined in `IsingModel.hpp` and `IsingModel.cpp`.

The main program `main.cpp` takes in command line arguments for the lattice length `L`, temperature `T`, number of cycles `cycles`, a variable `random_config`, the number of threads `threads` and the cutoff fraction `cutoff_fraction` for the equilibration time of the lattice. The following example makefile compiles and executes the program:
``` Ruby
all: compile execute

compile:
	g++ -fopenmp -o main.exe main.cpp IsingModel.cpp

execute:
	./main.exe 100 2.4 100000 1 12 0.1 0 0 
```
With the above execution, main.cpp takes in `L = 100`, `T = 2.4`, `cycles = 1000`, `random_config = 1`, `threads = 12` and `cutoff_fraction = 0.1`.

The main program then creates an instance of the class and goes on to perform the calculations. If the number of threads is set to 1, it runs everything on a single thread. If not, it uses the OpenMP API to parallelize and run the calculations on the chosen number of threads.

The final results of the expectation values of energy and magnetization and the heat capacity and susceptibility are written to a file `results.txt`.
