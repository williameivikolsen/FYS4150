#include "IsingModel.hpp"
using namespace std;
ofstream ofile;

void IsingModel::Initialize(int L, double temp, int cycles, bool random_config){
    m_L = L;
    m_temp = temp;
    m_cycles = cycles;
    m_N = m_L*m_L;
    m_spin = new int[m_N];

    if (random_config==false) {
        // Initialize lattice with all spins pointing the same direction (down)
        for (int i = 0; i < m_L; i++) {
            for (int j = 0; j < m_L; j++) {
                m_spin[i*m_L + j] = -1;
                m_M += m_spin[i*m_L + j];
            }
        }
    }
    else {
      // Initialize lattice with random spin configuration
      random_device rand_nb;
      mt19937_64 gen(rand_nb());
      uniform_int_distribution<int> RandIntGen(0,1);
      for (int i = 0; i < m_L; i++) {
          for (int j = 0; j < m_L; j++) {
              m_spin[i*m_L + j] = RandIntGen(gen)*2-1;
              m_M += m_spin[i*m_L + j];
          }
      }
    }

    // Beregner energien med periodic boundary conditions
    m_E = 0;
    for (int i = 0; i < m_L; i++) {
        for (int j = 0; j < m_L; j++) {
            m_E -= m_spin[i*m_L + j]*
            (m_spin[Periodic(i, 1)*m_L + j] +
            m_spin[i*m_L + Periodic(j, 1)]);
        }
    }

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

void IsingModel::MonteCarlo() {
    m_Eavg = 0.0;
    m_Mavg = 0.0;

    for (int i = 0; i < m_cycles; i++) {
        Metropolis();
        m_Eavg += m_E;
        m_Mavg += m_M;
    }
    m_Eavg /= m_cycles;
    m_Mavg /= m_cycles;
    delete[] m_BoltzmannFactor;
    delete[] m_spin;
}

void IsingModel::WriteToFile(double time_used){
    string filename = "results.txt";
    ofile.open(filename, ios_base::app);
    ofile << setw(15) << setprecision(8) << m_L;
    ofile << setw(15) << setprecision(8) << m_temp;
    ofile << setw(15) << setprecision(8) << m_cycles;
    ofile << setw(15) << setprecision(8) << m_Eavg;
    ofile << setw(15) << setprecision(8) << m_Mavg; 
    ofile << setw(15) << setprecision(8) << "1";                // Number threads
    ofile << setw(15) << setprecision(8) << time_used << endl;
    ofile.close();
}

void IsingModel::WriteToFileParallelized(double global_Eavg, double global_Mavg, int cycles, int threads, double time_used){
    string filename = "results.txt";
    ofile.open(filename, ios_base::app);
    ofile << setw(15) << setprecision(8) << m_L;
    ofile << setw(15) << setprecision(8) << m_temp;
    ofile << setw(15) << setprecision(8) << cycles;
    ofile << setw(15) << setprecision(8) << global_Eavg;
    ofile << setw(15) << setprecision(8) << global_Mavg; 
    ofile << setw(15) << setprecision(8) << threads;                // Number threads
    ofile << setw(15) << setprecision(8) << time_used << endl;
    ofile.close();
}