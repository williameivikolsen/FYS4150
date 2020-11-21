#include "IsingModel.hpp"
#include <cstdio>
#include <iostream>

using namespace std;

int main(int argc, char *argv[]){
    int L = atoi(argv[1]);              // Size of Lattice: LxL
    double T = atof(argv[2]);          // Run for only one temperture
    int cycles = atoi(argv[3]);         // Number of MonteCarlo cycles

    IsingModel my_solver;
    bool random_config;
    my_solver.Initialize(L, T, random_config = true);
    my_solver.MonteCarlo(cycles);

    return 0;
}
