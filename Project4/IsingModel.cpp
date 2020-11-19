#include "IsingModel.hpp"

using namespace std;
ofstream ofile;

void IsingModel::Initialize(int L, double temp){
    m_L = L;
    m_temp = temp;
    m_N = m_L*m_L;
    m_spin = new int[m_N];

    // Initialiserer systemet til å starte med alle spinn opp
    // for (int i = 0; i < m_L; i++) {
    //     for (int j = 0; j < m_L; j++) {
    //         m_spin[i*m_L + j] = 1;
    //     }
    // }
    // m_M = m_N;
    // Beregner energien med periodic boundary conditions
    // m_E = 0;
    // int jm = m_N;
    // for (int j = 1; j <= m_N; j++) {
    //     m_E -= m_spin[j]*m_spin[jm];
    //     jm = j;
    // }
    // cout << m_E << endl;
    m_spin[0] = 1;
    m_spin[1] = -1;
    m_spin[2] = -1;
    m_spin[3] = 1;
    m_M = 0;
    m_E = 8;

    // Setter opp mulige Boltzmann-faktorer:
    m_BoltzmannFactor = new double[17];
    m_BoltzmannFactor[0] = exp(8);
    m_BoltzmannFactor[4] = exp(4);
    m_BoltzmannFactor[8] = exp(0);
    m_BoltzmannFactor[12] = exp(-4);
    m_BoltzmannFactor[16] = exp(-8);
}

int IsingModel::Periodic(int i, int add){
    return (i + m_L + add) % m_L;
}

void IsingModel::Metropolis(){
    int x; int y;           // Random positions to perform spin flip
    int dE; int dM;         // Changes in energy and magnetization
    double w;               // Boltzmann factor
    double r;               // Random number
    srand(time(0));
    // Go through all elements and perform random spin flip each time
    for (int i = 0; i <=m_L; i++) {
        for (int j = 0; j < m_L; j++) {
            // Generate random numbers x and y in range [0, L-1]
            x = rand()%m_L;
            y = rand()%m_L;
            dE = 2*m_spin[x*m_L + y]*
            (m_spin[Periodic(x, 1)*m_L + y] + 
            m_spin[Periodic(x, -1)*m_L + y] +
            m_spin[x*m_L + Periodic(y, 1)] +
            m_spin[x*m_L + Periodic(y, -1)]);
            if (dE <= 0) {
                m_spin[x*m_L + y] *= -1;
                m_E += dE;
                m_M += 2*m_spin[x*m_L + y];
            }
            else {
                w = m_BoltzmannFactor[dE+8];
                r = rand()*1./RAND_MAX;
                if (r <= w) {
                    m_spin[x*m_L + y] *= -1;
                    m_E += dE;
                    m_M += 2*m_spin[x*m_L + y];
                }
            }
        }
    }
}

void IsingModel::MonteCarlo(int cycles) {
    string filename = "results.txt";
    ofile.open(filename);
    for (int i = 0; i < cycles; i++) {
        Metropolis();
        ofile << setw(15) << setprecision(8) << m_E;
        ofile << setw(15) << setprecision(8) << m_M << endl;
    }
    delete[] m_BoltzmannFactor;
    delete[] m_spin;
}

void IsingModel::Write_to_file(){

}
