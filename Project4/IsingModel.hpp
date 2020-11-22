#ifndef IsingModel_HPP
#define IsingModel_HPP
#include <iostream>
#include <cmath>
#include <fstream>      // Write to file
#include <iomanip>      // Text formatting
#include <cstdlib>
#include <ctime>
#include <string>
#include <random>
#include "time.h"

using namespace std;

class IsingModel{
protected:
  int m_L;                  // Length of sides (number of spins along side)
  int m_cycles;             // Number of Monte Carlo cycles
  double m_temp;            // Temperature of system [kb/J]
  double m_cutoff_fraction; // Fraction of cycles to be disgarded before computing expectation values
  int m_N;                  // Total number of spins
  int *m_spin;              // Spin matrix, flattened 2D array
  int m_E;                  // Energy of system (per spin)
  int m_M;                  // Magnetization of system (per spin)
  double *m_BoltzmannFactor;    // Array containing Boltmann factors related to energy changes
  int Periodic(int i, int add);
  void Metropolis();        // Solving using the Metropolis algorithm

  // std random number generators
  mt19937 gen;
  uniform_real_distribution<> zero_one_int_dist;
  uniform_real_distribution<> zero_one_real_dist;
  uniform_int_distribution<> zero_L_dist;

  double m_CV;
  double m_chi;

public:
  void Initialize(int L, double T, int cycles, bool random_config, double cutoff_fraction, int seed_shift = 0);
  void MonteCarlo();
  void WriteToFile(double time_used);
  void WriteToFileParallelized(double global_Eavg, double global_Mavg, double global_Esqavg, double global_Msqavg, int cycles, int threads, double time_used);

  // Følgende må være public for å kunne parallelliseres 
  double m_Eavg;        // Gjennomsnittlig energi
  double m_Mavg;        // Gjennomsnittlig magnetisering (absoluttverdi!)
  double m_Esqavg;      // Gjennomsnittlig energi kvadrert
  double m_Msqavg;      // Gjennomsnittlig magentisering kvadrert
};

#endif
