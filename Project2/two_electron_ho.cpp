#include "jacobi.hpp"

void Two_electron_HO::Init(int n, double epsilon, int maxit, int num_tests, string filename, bool test_bool, double omega) {
    // Initializing variables from Jacobi:
    Initialize(n, epsilon, maxit, num_tests, filename, test_bool);
    m_filename = filename;
    m_omega = omega;
    // Define rho from rho_max:
    m_rhomax = 100;
    vec rho = linspace(0.0, m_rhomax, m_n);
    // Generate matrix:
    for (int i = 0; i < m_n - 1; i++) {
        m_A(i, i) = m_d + omega*omega*rho(i)*rho(i);
        m_A(i + 1, i) = m_a;
        m_A(i, i + 1) = m_a;
    }
    m_A(m_n-1, m_n-1) = m_d + omega*omega*rho(m_n-1)*rho(m_n-1);
}

void Two_electron_HO::Test_results_analytic(){
    if(m_test_bool == true){  
        cout << "There is no test >:)" << endl;
    }
}