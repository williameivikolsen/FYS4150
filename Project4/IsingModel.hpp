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
  int m_L;                     // Length of sides (number of spins along side)
  int m_cycles;                // Number of Monte Carlo cycles
  double m_temp;               // Temperature of system [kb/J]
  double m_cutoff_fraction;    // Fraction of cycles to be disgarded before computing expectation values
  int m_N;                     // Total number of spins
  int *m_spin;                 // Spin matrix, flattened 2D array
  double m_E;                  // Energy of system
  double m_M;                  // Magnetization of system
  double *m_BoltzmannFactor;   // Array containing Boltmann factors related to energy changes

  bool m_E_distribution_bool;  // Bool variable set to "1" when system energies are to be printed 
  double *m_E_distribution;    // Array containing system energy value after every cycle (used to make distribution of energies)

  int Periodic(int i, int add); // Function that takes care of periodic boundary conditions
  void Metropolis();            // Solving using the Metropolis algorithm

  // std random number generators
  mt19937 gen;
  uniform_real_distribution<> zero_one_int_dist;
  uniform_real_distribution<> zero_one_real_dist;
  uniform_int_distribution<> zero_L_dist;

public:
  void Initialize(int L, double T, int cycles, bool random_config, double cutoff_fraction, bool E_distribution_bool, int seed_shift = 0);
  void MonteCarlo();
  void WriteSpins();            // Writes last spin config to file
  void WriteEnergies();         // Writes all energy values to file
  void WriteToFile(double time_used);
  void WriteToFileParallelized(double global_Eavg, double global_Mavg, double global_Esqavg, double global_Msqavg, int cycles, int threads, double time_used, double global_acceptancerate);
  ~IsingModel(); // Destructor

  // Følgende må være public for å kunne parallelliseres
  double m_Eavg;                // Gjennomsnittlig energi
  double m_Mavg;                // Gjennomsnittlig magnetisering (absoluttverdi!)
  double m_Esqavg;              // Gjennomsnittlig energi kvadrert
  double m_Msqavg;              // Gjennomsnittlig magentisering kvadrert
  double m_acceptancerate;      // Rate of suggested spin flips accepted
};

#endif
