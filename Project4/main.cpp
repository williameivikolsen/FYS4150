#include "IsingModel.hpp"
#include <cstdio>
#include <iostream>

using namespace std;

int main(){
    IsingModel my_solver;
    my_solver.Initialize(2, 1.0);
    my_solver.Metropolis();
    return 0;
}
