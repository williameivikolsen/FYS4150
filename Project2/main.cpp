#include "jacobi.hpp"
#include <iostream>
#include <cmath>
//#include <cstring>      // Compare strings
using namespace std;

int main(int argc, char *argv[]) {
    
    bool test;
    if(argc == 1){
        test = false;
    }
    else if(strcmp(argv[1], "test")== 0){
        test = true;
    }
    else{
        test = false;
    }

    int n = 10;
    int maxit = 1000;
    double epsilon = 1e-8;
    Jacobi my_solver;
    my_solver.Initialize(n, epsilon, maxit);
    my_solver.Loop(test);
    return 0;
}