#include "IsingModel.hpp"
#include <cstdio>
#include <iostream>

using namespace std;

int main(){
    IsingModel my_solver;
    bool random_config;
    my_solver.Initialize(20, 1.0,random_config = true);
    my_solver.MonteCarlo(1000);
    return 0;
}
