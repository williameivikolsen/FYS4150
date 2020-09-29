#include "jacobi.hpp"

void One_electron_HO::Init(int n, double epsilon, int maxit, vec V) {
    // Initialiserer variabler fra Jacobi:
    Initialize(n, epsilon, maxit);
    // Genererer matrise:
    for (int i = 0; i < m_n - 1; i++) {
        m_A(i, i) = m_d + V(i);
        m_A(i + 1, i) = m_a;
        m_A(i, i + 1) = m_a;
    }
    m_A(m_n - 1, m_n - 1) = m_d;
}