#include "jacobi.hpp"
#include <iostream>
#include <cmath>
#include <armadillo>

using namespace std;
using namespace arma;

void Jacobi::Initialize(int n, double epsilon, int maxit, int num_tests, bool test_bool) {
    m_n = n;
    m_h = 1/double(n);
    m_d = 2/(m_h*m_h);
    m_a = -1/(m_h*m_h);
    m_epsilon = epsilon;
    m_maxit = maxit;
    m_maxsq = m_a*m_a;

    m_v = zeros<vec>(m_n);      // To be filled
    m_A = zeros<mat>(m_n, m_n); // To be filled

    m_R = eye<mat>(m_n, m_n);
    m_test_bool = test_bool;
    m_num_tests = num_tests;
}

void Jacobi::Loop() {
    // We define the squared maximim off-diagonal element of A
    // to be a value known to be larger than epsilon to begin with:
    // Iteration counter:
    int it = 0;
    m_A.print();

    while (m_maxsq > m_epsilon and it < m_maxit) {
        Rotate();
        it++;
    }

    // Fill m_v with eigenvectors
    for (int i = 0; i < m_n; i++)
    {
        m_v(i) = m_A(i,i);
    }
    
    //cout << m_A << endl;
    //cout << m_R << endl;
    cout << "Loop finished. Number of loops: " << it << endl;
}

void Jacobi::Rotate() {
    // Variables to be used in calculations
    int k, l;
    double tau, t, c, s;
    double a_kl = 0.0;     // Max off-diagonal element of A

    // We find the maximum off-diagonal element of A.
    // Note: We only go through the upper triangle of the matrix (why?),
    // so we do not need to check that i!=j as the algorithm requires.
    for (int i = 0; i < m_n; i++) {
        for (int j = i+1; j < m_n; j++) {
            if (fabs(m_A(i, j)) > a_kl) {
                a_kl = fabs(m_A(i, j));
                l = i;
                k = j;
            }
        }
    }
    // Update max squared off-diagonal element:
    m_maxsq = a_kl*a_kl;
    // Now we calculate tau, tan, cos and sin:
    if (a_kl != 0.0) {
        tau = (m_A(l, l) - m_A(k, k))/(2.0*a_kl);
        if (tau >= 0.0) {
            t = 1.0/(tau + sqrt(1.0 + tau*tau));
        }
        else {
            t = -1.0/(-tau - sqrt(1.0 + tau*tau));
        }
        c = 1.0/sqrt(1.0 + t*t);
        s = t*c;
    }
    else {
        c = 1.0;
        s = 0.0;
    }
    // Now we calculate the transformed matrix
    double a_kk, a_ll, a_ik, a_il, r_ik, r_il;
    a_kk = m_A(k, k);
    a_ll = m_A(l, l);
    m_A(k, k) = c*c*a_kk - 2.0*c*s*m_A(k, l) + s*s*a_ll;
    m_A(l, l) = s*s*a_kk + 2.0*c*s*m_A(k, l) + c*c*a_ll;
    m_A(k, l) = 0.0;
    m_A(l, k) = 0.0;
    for (int i = 0; i < m_n; i++) {
        if (i != k && i != l) {
            a_ik = m_A(i, k);
            a_il = m_A(i, l);
            m_A(i, k) = c*a_ik - s*a_il;
            m_A(k, i) = m_A(i, k);
            m_A(i, l) = c*a_il + s*a_ik;
            m_A(l, i) = m_A(i, l);
        }
        // The new eigenvectors become
        r_ik = m_R(i, k);
        r_il = m_R(i, l);

        m_R(i, k) = c * r_ik - s * r_il;
        m_R(i, l) = c * r_il + s * r_ik;
    }
}

void Jacobi::Test_results_armadillo(){
if (m_test_bool==true){      
    // Test eigenvectors and eigenvalues against Armadillo
    int freq_check = m_n/(m_num_tests-1); // Frequency of testing
    cout << endl << "--------------------------------------------------------------------------" << endl;
    cout << "Testing against Armadillo for every " << freq_check << " value + last value. Tolerance: " << m_epsilon << endl;     
 
    vec eigval;     // Will be listed in ascending order
    mat eigvec;     // Stored as column vectors
    eig_sym(eigval, eigvec, m_A0);
 
    uvec sort_indices = sort_index(m_v); // Indexes needed to sort m_v


    // Compare eigenvectors
    cout << "Executing eigenvalue tests: " << endl;
    int error_count = 0;
    

    for (int i = 0; i < m_n; i++){
        if(i % freq_check == 0 || i == m_n-1){ // Test only for select values of i
        cout << "Testing for i = " << i << "..."<< endl;

        int sort_idx = sort_indices[i]; // Corresponding index for m_v
        
            if(abs(eigval[i]-m_v[sort_idx]) > m_epsilon){ // m_epsilon
                cout << "***********************" << endl;
                cout << "Eigenvalue check fails!" << endl;
                cout << "Armadillo eigenvalue: " << eigval[i] << endl;
                cout << "Jacobi eigenvalue: " << m_v[sort_idx] << endl;
                cout << "Absolute difference is " << abs(eigval[i]-m_v[sort_idx]);
                cout <<  ", which is higher than tolerance " << m_epsilon << endl;
                cout << "***********************" << endl;
                error_count++;
            }
        }

    }
    if(error_count == 0){
        cout << m_num_tests <<"/" << m_num_tests << " eigenvalue tests passed!" << endl;
    }
    else{
        cout << error_count <<"/" << m_num_tests << " eigenvalue tests failed" << endl;
    }

    // // Compare norm of eigenvectors
    // cout << endl << "Executing eigenvector tests: " << endl;
    // error_count = 0;
    // eigvec.print();
    // cout << endl;
    // m_R.print();

    // cout << endl;
    // m_A0.print();
    // for (int i = 0; i < m_n; i++){
    
    //     if(i % (m_n/(num_tests-1)) == 0 || i == m_n-1){ // Test only for select values of i
    //     cout << "Testing for i = " << i << "..."<< endl;

    //     int sort_idx = sort_indices[i]; // Corresponding index for m_v
    //     // vec jacobi_eigenvec = m_R.row(sort_idx).as_col(); // Relevant eigenvector is row sort_idx of m_R
    //     // jacobi_eigenvec.print();
    //     // cout << endl;
    //     // vec armadillo_eigenvec = eigvec.col(i);
    //     // armadillo_eigenvec.print();
    //     // m_A.print();
    //         // if(norm(eigvec[i]-jacobi_eigenvec) > m_epsilon){
    //         //     cout << "***********************" << endl;
    //         //     cout << "Eigenvector check fails!" << endl;
    //         //     cout << "Armadillo eigenvector: " << eigvec[i] << endl;
    //         //     cout << "Jacobi eigenvector: " << jacobi_eigenvec << endl;
    //         //     cout << "Difference of vectors has norm " << norm(eigvec[i]-jacobi_eigenvec);
    //         //     cout <<  ", which is higher than tolerance " << m_epsilon << endl;
    //         //     cout << "***********************" << endl;
    //         //     error_count++;
    //         // }
    //     }

    // }
    // if(error_count == 0){
    //     cout << num_tests <<"/" << num_tests << " eigenvector tests passed!" << endl;
    // }
    // else{
    //     cout << error_count <<"/" << num_tests << " eigenvector tests failed" << endl;
    // }

    cout << "--------------------------------------------------------------------------" << endl;
}
else{
    cout << "********************************************************************" << endl;
    cout << "Add 'test' on command line when executing in order to perform tests." << endl;
    cout << "********************************************************************" << endl;
}
}