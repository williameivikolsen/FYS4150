#include "IsingModel.hpp"
#include <cstdio>
#include <iostream>

using namespace std;

int main(){
    IsingModel my_solver;
    my_solver.Initialize(2, 1.0);
    my_solver.MonteCarlo(10000);
    my_solver.Write_to_file();
    return 0;
}
