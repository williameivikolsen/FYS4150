#include "jacobi.hpp"

void Beam::Init(int n, double epsilon, int maxit) {
    // Initialiserer variabler fra Jacobi:
    Initialize(n, epsilon, maxit);
    // Genererer matrise:
    for (int i = 0; i < m_n - 1; i++) {
        m_A(i, i) = m_d;
        m_A(i + 1, i) = m_a;
        m_A(i, i + 1) = m_a;
    }
    m_A(m_n - 1, m_n - 1) = m_d;
    m_A0 = m_A;
}