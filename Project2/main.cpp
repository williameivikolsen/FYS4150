#include "jacobi.hpp"

using namespace std;

int main(int argc, char *argv[]) {

    string syst = argv[1];
    int n = atoi(argv[2]);
    double epsilon = atof(argv[3]);
    int maxit = atoi(argv[4]);
    string filename = argv[5];

    bool test_bool = false;     // Default is false for testing
    int num_tests;              // Number of (evenly spaced out) tests to be performed per test function
    float rho_max;              // Cut-off for rho in HO-cases  
    if(strcmp(argv[6], "test") == 0){
        test_bool = true;
        num_tests = atoi(argv[7]);
        if(strcmp(argv[1], "HO1") == 0 && strcmp(argv[1], "HO2")){
            rho_max = atof(argv[8]);
        }
    }
    else{
        if(strcmp(argv[1], "HO1") == 0 && strcmp(argv[1], "HO2")){
            rho_max = atof(argv[6]);
        }
    }

    // Now run class functions for chosen system:
    if (syst.compare("beam") == 0) {
        Beam my_solver;
        my_solver.Init(n, epsilon, maxit, num_tests, filename, test_bool);
        my_solver.Loop();
        // my_solver.Test_results_armadillo();
        my_solver.Test_results_analytic();
        my_solver.Test_results_orthogonality();
        my_solver.Print_to_file();
    }
    else if (syst.compare("HO1") == 0) {
        One_electron_HO my_solver;
        my_solver.Init(n, epsilon, maxit, num_tests, filename, test_bool, rho_max);
        my_solver.Loop();
        // my_solver.Test_results_armadillo();
        // my_solver.Test_results_analytic();
        my_solver.Test_results_orthogonality();
        my_solver.Print_to_file();

    }
    else if (syst.compare("HO2") == 0) {
        cout << "The chosen syst is yet to be added as class." << endl;
        exit(EXIT_FAILURE);
    }
    else {
        cout << "Something is wrong with python script." << endl;
        exit(EXIT_FAILURE);
    }
    return 0;
}