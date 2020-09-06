#include <iostream>
#include <armadillo>
#include <fstream>      // Write to file
#include <iomanip>      // Text formatting
#include "time.h"       // Timer
#include <chrono>       // Current time
#include <ctime>        // Print current time

using namespace std;
using namespace arma;

int main(int argc, char* argv[]){
  // Read number of grid points and function to be used
    int n;
    if( argc != 2 ){
          cout << "Bad Usage: " << argv[0] <<
              " needs dimension of matrix (n)" << endl;
          exit(1);
    }
        else{
        n = atoi(argv[1]);
    }

    // Define matrix A
    mat A = 2*eye<mat>(n,n);        // (n x n) matrix with 2 on diagonal
    for (int i = 0; i < n-1; i++){
        A(i, i+1) = -1;             // Set upper diagonal = -1
        A(i+1, i) = -1;             // Set lower diagonal = -1
    
    cout << A << endl;
    return 0;
}