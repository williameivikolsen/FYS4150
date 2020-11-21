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
  int m_L;              // Length of sides (number of spins along side)
  int m_cycles;         // Number of Monte Carlo cycles
  double m_temp;        // Temperature of system [UNIT???]
  int m_N;              // Total number of spins
  int *m_spin;          // Spin matrix, flattened 2D array
  int m_E;              // Energy of system (per spin)
  int m_M;              // Magnetization of system (per spin)
  double *m_BoltzmannFactor;    // Array containing Boltmann factors related to energy changes
  int Periodic(int i, int add);
  void Metropolis();    // Solving using the Metropolis algorithm

  double m_CV;
  double m_chi;

public:
  void Initialize(int L, double T, int cycles, bool random_config);
  void MonteCarlo();
  void WriteToFile(double time_used);
  void WriteToFileParallelized(double global_Eavg, double global_Mavg, int cycles, int threads, double time_used);

  // Følgende må være public for å kunne parallelliseres 
  double m_Eavg;        // Gjennomsnittlig energi
  double m_Mavg;        // Gjennomsnittlig magnetisering (absoluttverdi!)
};

#endif
