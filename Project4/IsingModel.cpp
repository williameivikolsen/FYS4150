#include "IsingModel.hpp"
using namespace std;
ofstream ofile;

void IsingModel::Initialize(int L, double temp, int cycles, bool random_config, double cutoff_fraction, bool E_distribution_bool, int seed_shift){
    m_L = L;
    m_temp = temp;
    m_cycles = cycles;
    m_N = m_L*m_L;
    m_cutoff_fraction = cutoff_fraction;
    m_spin = new int[m_N];
    m_E_distribution_bool = E_distribution_bool;
    m_E_distribution = new double[int ((1-m_cutoff_fraction)*m_cycles)];

    // random_device rand_nb;
    mt19937 gen(clock()+100*seed_shift);
    uniform_int_distribution<int> zero_one_int_dist(0, 1);

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
        for (int i = 0; i < m_L; i++) {
            for (int j = 0; j < m_L; j++) {
                m_spin[i*m_L + j] = zero_one_int_dist(gen)*2-1;
                m_M += m_spin[i*m_L + j];
            }
        }
    }

    // Calculated energy with periodic boundary conditions
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
    m_BoltzmannFactor[0] = exp(8/m_temp);
    m_BoltzmannFactor[4] = exp(4/m_temp);
    m_BoltzmannFactor[8] = exp(0);
    m_BoltzmannFactor[12] = exp(-4/m_temp);
    m_BoltzmannFactor[16] = exp(-8/m_temp);
}

int IsingModel::Periodic(int i, int add){
    return (i + m_L + add) % m_L;
}

void IsingModel::Metropolis(){
    int x, y;               // Random positions to perform spin flip
    int dE, dM;             // Changes in energy and magnetization

    uniform_real_distribution<double> zero_one_real_dist(0, 1.0);
    uniform_int_distribution<int> zero_L_dist(0, m_L-1);

    // Go through all elements and perform random spin flip each time
    for (int i = 0; i <=m_N; i++) {
        // Generate random numbers x and y in range [0, L-1]
        x = zero_L_dist(gen);
        y = zero_L_dist(gen);
        dE = 2*m_spin[x*m_L + y]*
        (m_spin[Periodic(x, 1)*m_L + y] +
        m_spin[Periodic(x, -1)*m_L + y] +
        m_spin[x*m_L + Periodic(y, 1)] +
        m_spin[x*m_L + Periodic(y, -1)]);
        if (dE <= 0) {
            m_spin[x*m_L + y] *= -1;
            m_E += dE;
            m_M += 2*m_spin[x*m_L + y];
            m_acceptancerate++;
        }
        else if(zero_one_real_dist(gen) < m_BoltzmannFactor[dE+8]){
            m_spin[x*m_L + y] *= -1;
            m_E += dE;
            m_M += 2*m_spin[x*m_L + y];
            m_acceptancerate++;
        }
    }
}

void IsingModel::MonteCarlo() {
    double normalize = 1/((1.0-m_cutoff_fraction)*m_cycles*m_N);    // Used to find values per spin and cycle
    m_Eavg = 0.0;
    m_Mavg = 0.0;
    m_Esqavg = 0.0;
    m_Msqavg = 0.0;
    m_acceptancerate = 0.0; // Initialize acceptance rate to zero

    for (int i = 0; i < m_cycles*m_cutoff_fraction; i++){
        Metropolis();
    }
    for (int i = 0; i < (1-m_cutoff_fraction)*m_cycles; i++) {
        Metropolis();
        m_Eavg += m_E;
        m_Mavg += abs(m_M);
        m_Esqavg += m_E*m_E;
        m_Msqavg += m_M*m_M;
        if(m_E_distribution_bool == 1) m_E_distribution[i] = m_E;
 
    }
    m_Eavg *= normalize;
    m_Mavg *= normalize;
    m_Esqavg *= normalize;
    m_Msqavg *= normalize;
    m_acceptancerate /= (m_cycles*m_N);  // Note: Acceptance rate ignores cut-off fraction!
}

void IsingModel::WriteSpins(){
    string filename = "spins.txt";
    ofile.open(filename, ios_base::app);
    for (int i = 0; i < m_L; i++){
        for (int j= 0; j < m_L; j++){
            ofile << m_spin[i*m_L+j] << " ";
        }
        ofile << endl;
    }
    ofile.close();
}

void IsingModel::WriteEnergies(){
    string filename = "energies.txt";
    ofile.open(filename, ios_base::app);
    for (int i = 0; i < int ((1-m_cutoff_fraction)*m_cycles); i++){
        ofile << m_E_distribution[i] << endl;
    }
    ofile.close();
}

void IsingModel::WriteToFile(double time_used){

    string filename = "results.txt";
    double E_varians = m_Esqavg*m_N - m_Eavg*m_Eavg*(m_N*m_N);
    double M_varians = m_Msqavg*m_N - m_Mavg*m_Mavg*(m_N*m_N);
    double C_v = E_varians/(m_temp*m_temp*m_N);
    double chi = M_varians/(m_temp*m_N);

    ofile.open(filename, ios_base::app);
    ofile << setw(15) << setprecision(8) << m_L;
    ofile << setw(15) << setprecision(8) << m_temp;
    ofile << setw(15) << setprecision(8) << m_cycles;
    ofile << setw(15) << setprecision(8) << m_Eavg;
    ofile << setw(15) << setprecision(8) << m_Mavg;
    ofile << setw(15) << setprecision(8) << C_v;
    ofile << setw(15) << setprecision(8) << chi;
    ofile << setw(15) << setprecision(8) << "1";                // Number threads
    ofile << setw(15) << setprecision(8) << time_used;
    ofile << setw(15) << setprecision(8) << m_acceptancerate << endl;
    ofile.close();
}

void IsingModel::WriteToFileParallelized(double global_Eavg, double global_Mavg, double global_C_v, double global_chi, int cycles, int threads, double time_used, double global_acceptancerate){
    string filename = "results.txt";
    ofile.open(filename, ios_base::app);
    ofile << setw(15) << setprecision(8) << m_L;
    ofile << setw(15) << setprecision(8) << m_temp;
    ofile << setw(15) << setprecision(8) << cycles;
    ofile << setw(15) << setprecision(8) << global_Eavg;
    ofile << setw(15) << setprecision(8) << global_Mavg;
    ofile << setw(15) << setprecision(8) << global_C_v;
    ofile << setw(15) << setprecision(8) << global_chi;
    ofile << setw(15) << setprecision(8) << threads;                // Number threads
    ofile << setw(15) << setprecision(8) << time_used;
    ofile << setw(15) << setprecision(8) << global_acceptancerate << endl;
    ofile.close();
}

IsingModel::~IsingModel(){
    delete[] m_spin;
    delete[] m_BoltzmannFactor;
    delete[] m_E_distribution;
}