#include "jacobi.hpp"
#include <iostream>
#include <cmath>
//#include <cstring>      // Compare strings
using namespace std;

int main(int argc, char *argv[]) {
    
    bool test_bool;
    if(argc == 1){
        test_bool = false;
    }
    else if(strcmp(argv[1], "test")== 0){
        test_bool = true;
    }
    else{
        test_bool = false;
    }

    int n = 15;
    int maxit = 1000;
    double epsilon = 1e-8;
    int num_tests = 6;          // A check will be performed on every num_test'th value 
    Beam my_solver;
    my_solver.Init(n, epsilon, maxit, num_tests, test_bool);
    my_solver.Loop();
    // my_solver.Test_results_armadillo();
    my_solver.Test_results_analytic();
    my_solver.Test_results_orthogonality();
    return 0;
}