#include "jacobi.hpp"

using namespace std;
using namespace arma;
ofstream ofile;

void Jacobi::Initialize(int n, double epsilon, int maxit, int num_tests, string filename, bool test_bool) {
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

    while (m_maxsq > m_epsilon and it < m_maxit) {
        Rotate();
        it++;
    }
    

    // Fill m_v with eigenvalues
    for (int i = 0; i < m_n; i++){
        m_v(i) = m_A(i,i);
    }
    
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
    cout << "--------------------------------------------------------------------------" << endl;
}
else{
    cout << "********************************************************************" << endl;
    cout << "Add 'test' on command line when executing in order to perform tests." << endl;
    cout << "********************************************************************" << endl;
}
}

void Jacobi::Test_results_orthogonality(){
    // If in testing mode: check orthogonality m_num_test times in final matrixes m_A and m_R
    if(m_test_bool == true){
        int freq_check = m_n/(m_num_tests-1);           // Frequency of testing
        ivec checked_idx = zeros<ivec>(m_num_tests);     // Integer vector

        int j = 0;                                  // Index of checked_idx
        for(int i = 0; i < m_n; i++){
            if(i % freq_check == 0 || i == m_n-1){      // Check only for select eigenvectors
                checked_idx(j) = i;
                j++;
            }
        }
        int err_count = 0;
        int checked_row_i;  // Index needed for below loop
        int checked_row_j;  // Index needed for below loop

        for(int i = 0; i < m_num_tests; i++){
            checked_row_i = checked_idx(i);
            for(int j = i; j < m_num_tests; j++){
                checked_row_j = checked_idx(j);
                if(i == j){
                    if(abs(as_scalar(dot(m_R.row(checked_row_i), m_R.row(checked_row_j)))) - 1 > m_epsilon){
                        cout << "m_R: Inner product not equal to 1 for i,j=" << checked_row_i << endl;
                        cout << "     Abs. inner product minus 1 should be lower than tolerence " << m_epsilon;
                        cout << ", but is acually " << abs(as_scalar(dot(m_R.row(checked_row_i), m_R.row(checked_row_j)))) - 1 << endl;
                        err_count++;
                    }
                }
                else{
                    if(abs(as_scalar(dot(m_R.row(checked_row_i), m_R.row(checked_row_j)))) > m_epsilon){
                        cout << "m_R: Inner product not equal to 0 for i=" << checked_row_i << ", j=" << checked_row_j<< endl;
                        cout << "     Abs. inner product should be lower than tolerence " << m_epsilon;
                        cout << ", but is acually " << abs(as_scalar(dot(m_R.row(checked_row_i), m_R.row(checked_row_j)))) << endl;
                        err_count++;
                    }
            }
            
        }
    }
    cout << "********************************************" << endl;
    cout << "In total: " << err_count << " errors" << endl;
    cout << "********************************************" << endl;
    }
}

void Jacobi::Print_to_file(){
    ofile.open(m_filename);
    ofile << "Top row: Eigenvealues." << endl;
    ofile << "Corresponding eigenvectors in columns below each eigenvalue." << endl;
    for (int i = 0; i < m_n; i++) {
        ofile << m_A(i, i) << setw(14);
    }
    ofile << endl;
    for (int i = 0; i < m_n; i++) {
        for (int j = 0; j < m_n; j++) {
            ofile << m_R(j, i) << setw(14);
        }
        ofile << endl;
    }
    ofile.close();
}