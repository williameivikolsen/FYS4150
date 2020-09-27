#ifndef JACOBI_HPP
#define JACOBI_HPP
#include <armadillo>

using namespace arma;

class Jacobi {
private:
    int m_n;                      // Number of matrix points
    double m_h;                   // Step size
    double m_d;                   // Diagonal elements
    double m_a;                   // Off-diagonal elements
    double m_epsilon;             // Tolerance
    int m_maxit;                  // Maximum number of iterations
    double m_maxsq;               // Max squared off-diagonal element
    mat m_A;                      // Matrix             (nxn)
    mat m_R;                      // Eigenvector matrix (nxn)
public:
    void Initialize(int n, double epsilon, int maxit);   // Initialize parameters n, h, d, a, epsilon and maxit
    void Loop();
    void Rotate();           // Perform Jacobi rotation and return max off-diagonal value
};
#endif