#include "jacobi.hpp"

using namespace std;

void Beam::Init(int n, double epsilon, int maxit, int num_tests, string filename, bool test_bool) {
    // Initialiserer variabler fra Jacobi:
    Initialize(n, epsilon, maxit, num_tests, filename, test_bool);
    m_filename = filename;
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
    // If in testing mode: check orthogonality m_num_test times in final matrix m_R
    cout << "--------------------------------------------------------------------------" << endl;
    cout << "Checking beam eigenvalues against analytical values" << endl;
    if(m_test_bool == true){
        int err_count = 0;
        double eigval_analytical;
        for (int j = 0; j < m_n; j++) {
            eigval_analytical = m_d + 2*m_a*cos((j+1)*M_PI/(m_n+1));
            if (abs(m_v(j) - eigval_analytical > 0.1*eigval_analytical)) {
                cout << "Calculated eigenvalue not equal to analytical for i = " << j << endl;
                cout << "Calculated eigenvalue: " << m_v(j) << endl;
                cout << "Analytical eigenvalue: " << eigval_analytical << endl;
                err_count++;
            }
        }
        cout << "********************************************" << endl;
        cout << "In total: " << err_count << " errors" << endl;
        cout << "********************************************" << endl << endl;
    }
}