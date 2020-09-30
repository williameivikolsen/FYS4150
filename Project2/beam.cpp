#include "jacobi.hpp"

void Beam::Init(int n, double epsilon, int maxit, int num_tests, bool test_bool) {
    // Initialiserer variabler fra Jacobi:
    Initialize(n, epsilon, maxit, num_tests, test_bool);
    // Genererer matrise:
    for (int i = 0; i < m_n - 1; i++) {
        m_A(i, i) = m_d;
        m_A(i + 1, i) = m_a;
        m_A(i, i + 1) = m_a;
    }
    m_A(m_n - 1, m_n - 1) = m_d;
    m_A0 = m_A;
}

void Beam::Test_results_analytic(){
    vec eigval_analytical = zeros<vec>(m_n); 

    cout << "--------------" << endl << "eigenvals: " << endl;
    cout << "m_d: " << m_d << ", m_a: " << m_a << endl;
    for (int j = 0; j < m_n; j++)
    {
        // cout << cos(j*M_PI/m_n) << endl;
        eigval_analytical(j) = m_d + 2*m_a*cos((j+1)*M_PI/(m_n+1));
    }
    cout << "Analytical eigvals:" << endl;
    eigval_analytical.print();
    cout << endl;
    
    cout << "Calculated eigvals:" << endl;
    m_v.print();
    cout << endl;

    vec eigval_arma;     // Will be listed in ascending order
    mat eigvec_arma;     // Stored as column vectors
    eig_sym(eigval_arma, eigvec_arma, m_A0);


    cout << "Armadillo eigvals:" << endl;
    eigval_arma.print();
    
    cout << "--------------" << endl << "eigenvecs: " << endl;



}