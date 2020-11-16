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

    // Initialiserer forventningsverdier
    m_Eavg = 0.0;
    m_Mavg = 0.0;
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
}

void IsingModel::MonteCarlo(int cycles) {
    double avg_M = 0.0;
    double avg_E2 = 0.0;
    double avg_M2 = 0.0;
    for (int i = 0; i < cycles; i++) {
        Metropolis();
        m_Eavg += m_E;
        m_Mavg += abs(m_M);
        avg_M += m_M;
        avg_E2 += m_E*m_E;
        avg_M2 += m_M*m_M;
    }
    m_Eavg /= cycles;
    m_Mavg /= cycles;
    avg_M /= cycles;
    avg_E2 /= cycles;
    avg_M2 /= cycles;
    m_CV = 1/(m_temp*m_temp)*(avg_E2 - m_Eavg*m_Eavg);
    m_chi = 1/m_temp*(avg_M2 - avg_M*avg_M);
}

void IsingModel::Write_to_file(){
    string filename = "results.txt";
    ofile.open(filename);
    ofile << setw(15) << setprecision(8) << m_temp;
    ofile << setw(15) << setprecision(8) << m_Eavg;
    ofile << setw(15) << setprecision(8) << m_Mavg;
    ofile << setw(15) << setprecision(8) << m_CV;
    ofile << setw(15) << setprecision(8) << m_chi << endl;
}
