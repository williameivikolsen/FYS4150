#include "jacobi.hpp"
#include <iostream>
#include <cmath>

using namespace std;

void Jacobi::Initialize(int n, double epsilon) {
    m_n = n;
    m_h = 1/n;
    m_d = 2/(m_h*m_h);
    m_a = -1/(m_h*m_h);
    m_epsilon = epsilon;
    **m_A = m_A[n][n];
    for (int i = 0; i < n-1; i++) {
        m_A[i][i] = m_a;
        m_A[i+1][i] = m_d;
        m_A[i][i+1] = m_d;
    }
    m_A[n-1][n-1] = m_a;
}

void Jacobi::Loop() {
    // We define the squared maximim off-diagonal element of A
    // to be a value known to be larger than epsilon to begin with:
    double max_sq = 1;
    while (max_sq > m_epsilon) {
        max_sq = Rotate();
    }
}

double Jacobi::Rotate() {
    // Variables to be used in calculations
    int k, l;
    double tau, t, c, s;
    double akl = 0;     // Max off-diagonal element of A

    // We find the maximum off-diagonal element of A.
    // Note: We only go through the upper triangle of the matrix (why?),
    // so we do not need to check that i!=j as the algorithm requires.
    for (int i = 0; i < m_n; i++) {
        for (int j = i+1; j < m_n; j++) {
            if (fabs(m_A[i][j]) > akl) {
                akl = fabs(m_A[i][j]);
                l = i;
                k = j;
            }
        }
    }

    // Now we calculate tau, tan, cos and sin:
    if (m_A[k][l] != 0.0) {
        tau = (m_A[l][l] - m_A[k][k])/(2*m_A[k][l]);
        if (tau > 0) {
            t = 1.0/(tau + sqrt(1.0 + tau*tau));
        }
        else {
            t = -1.0/(-tau - sqrt(1.0 + tau*tau));
        }
        double c = 1/sqrt(1 + t*t);
        double s = t*c;
    }
    else {
        c = 1.0;
        s = 0.0;
    }

    // Now we compute the updated matrix:
    for (int i = 0; i < m_n; i++)
    {
        if (i != k && i != l)
        {
            m_A[i][k] = m_A[i][k] * c - m_A[i][l] * s;
            m_A[i][l] = m_A[i][l] * c + m_A[i][k] * s;
        }
        m_A[k][k] = m_A[k][k]*c*c - 2*m_A[k][l] *c*s + m_A[l][l]*s*s;
        m_A[l][l] = m_A[l][l]*c*c + 2*m_A[k][l]*c*s + m_A[k][k]*s*s;
        m_A[k][l] = 0.0;
        m_A[l][k] = 0.0;
    }
    return akl*akl;
}