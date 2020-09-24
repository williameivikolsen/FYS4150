#ifndef JACOBI_HPP
#define JACOBI_HPP

class Jacobi {
private:
    int m_n;                      // Number of matrix points
    double m_h;                   // Step size
    double m_d;                   // Diagonal elements
    double m_a;                   // Off-diagonal elements
    double m_epsilon;             // Tolerance
    double **m_A;                 // Matrix
public:
    void Initialize(int n, double epsilon);   // Initialize parameters n, h, d, a and epsilon
    void Loop();
    double Rotate();  // Perform Jacobi rotation and return max off-diagonal value
};
#endif