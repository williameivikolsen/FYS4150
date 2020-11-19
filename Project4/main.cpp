#include "IsingModel.hpp"
#include <cstdio>
#include <iostream>

using namespace std;

int main(){
    IsingModel my_solver;
    my_solver.Initialize(20, 1.0);
    my_solver.MonteCarlo(1000);
    return 0;
}
