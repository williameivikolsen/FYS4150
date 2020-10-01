#ifndef JACOBI_HPP
#define JACOBI_HPP
#include <armadillo>
#include <iostream>
#include <cmath>
#include <stdlib.h>
#include <string>
#include <iomanip>      // Text formatting

using namespace arma;
using namespace std;

class Jacobi {
protected:
    int m_n;                      // Number of matrix points
    double m_h;                   // Step size
    double m_d;                   // Diagonal elements
    double m_a;                   // Off-diagonal elements
    double m_epsilon;             // Tolerance
    int m_maxit;                  // Maximum number of iterations
    double m_maxsq;               // Max squared off-diagonal element
    mat m_A;                      // Matrix                     (nxn)
    mat m_A0;                     // Copy of original matrix A  (nxn)   
    mat m_R;                      // Eigenvector matrix         (nxn)
    vec m_v;                      // Eigenvalue vector          (nx1)
    bool m_test_bool;             // Whether to preform tests or not 
    int m_num_tests;              // Number of (evenly spaced out) tests to be performed per test function
    string m_filename;            // Filename for data to be saved
    void Rotate();                // Perform Jacobi rotation and return max off-diagonal value

public:
    void Initialize(int n, double epsilon, int maxit, int num_tests, string filename, bool test_bool);   // Initialize parameters n, h, d, a, epsilon, maxit, A and R
    void Loop();
    void Test_results_armadillo();
    void Test_results_orthogonality();
    void Print_to_file();
};

class Beam : public Jacobi {
public:
    void Init(int n, double epsilon, int maxit, int num_tests, string filename, bool test_bool);
    void Test_results_analytic();
};

class One_electron_HO : public Jacobi {
private:
    double m_rho_max;             // Cut-off for rho in HO-cases  
public:
    void Init(int n, double epsilon, int maxit, int num_tests, string filename, bool test_bool, double rho_max);
    void Test_results_analytic();
};

class Two_electron_HO : public Jacobi {
private:
    double m_rho_max;             // Cut-off for rho in HO-cases 
    vec m_omega;                // Values of HO frequency
public:
    void Init(int n, double epsilon, int maxit, int num_tests, string filename, bool test_bool, double rho_max);
    void Test_results_analytic();
};
#endif