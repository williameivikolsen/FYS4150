#ifndef JACOBI_HPP
#define JACOBI_HPP
#include <armadillo>

using namespace arma;

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

public:
    void Initialize(int n, double epsilon, int maxit);   // Initialize parameters n, h, d, a, epsilon, maxit, A and R
    void Loop();
    void Rotate();           // Perform Jacobi rotation and return max off-diagonal value
    void Test_results(int num_tests, bool test_bool=false);
};

class Beam : public Jacobi {
public:
    void Init(int n, double epsilon, int maxit);
    void Solve();
};

class Oscillator : public Jacobi {
    void Init(int n, double epsilon, int maxit, vec V);
    void Solve();
};

#endif