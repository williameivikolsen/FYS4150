#include "IsingModel.hpp"

using namespace std;
ofstream ofile;

void IsingModel::Initialize(int L, double temp){
    m_L = L;
    m_temp = temp;
    m_N = m_L*m_L;
    m_spin = new double[m_N];
    m_J = 1; // Antar J = 1

    // Initialiserer systemet til å starte med alle spinn opp
    for (int i = 0; i < m_L; i++) {
        for (int j = 0; j < m_L; j++) {
            m_spin[i*m_L + j] = 1;
        }
    }
    m_M = m_N;
    // Beregner energien med periodic boundary conditions
    m_E = 0;
    int jm = m_N;
    for (int j = 1; j <= m_N; j++) {
        m_E -= m_J*m_spin[j]*m_spin[jm];
        jm = j;
    }

    // Setter opp mulige Boltzmann-faktorer:
    m_BoltzmannFactor = new double[5];
    m_BoltzmannFactor[0] = exp(-8*m_J);
    m_BoltzmannFactor[1] = exp(-4*m_J);
    m_BoltzmannFactor[2] = exp(0);
    m_BoltzmannFactor[3] = exp(4*m_J);
    m_BoltzmannFactor[4] = exp(8*m_J);
}

int IsingModel::Periodic(int i, int add){
    return (m_L + i + add) % m_L;
}

void IsingModel::Metropolis(){
    int x; int y;           // Random positions to perform spin flip
    double dE; double dM;   // Changes in energy and magnetization
    double w;               // Boltzmann factor
    double r;               // Random number
    srand(time(0));
    // Go through all elements and perform random spin flip each time
    for (int i = 0; i <=m_L; i++) {
        for (int j = 0; j < m_L; j++) {
            // Generate random numbers x and y in range [0, L]
            x = rand()%m_L;
            y = rand()%m_L;
            m_spin[x*m_L + y] = -m_spin[x*m_L + y];
            dE = -2*m_J*m_spin[x*m_L + y]*
            (m_spin[Periodic(x, 1)*m_L + y] + 
            m_spin[Periodic(x, -1)*m_L + y] +
            m_spin[x*m_L + Periodic(y, 1)] +
            m_spin[x*m_L + Periodic(y, -1)]);
            if (dE <= 0) {
                m_E += dE;
                m_M += 2*m_spin[x*m_L + y];
            }
            else {
                w = m_BoltzmannFactor[(int) (dE + 8*m_J)/(4*m_J)];
                r = rand()*1./RAND_MAX;
                if (r <= w) {
                    m_E += dE;
                    m_M += 2*m_spin[x*m_L + y];
                }
            }
        }
    }
    // cout << m_E << endl;
    // cout << m_M << endl;
    // cout << m_spin[0] << " " << m_spin[1] << endl;
    // cout << m_spin[2] << " " << m_spin[3] << endl;
}

void IsingModel::Write_to_file(){
}
