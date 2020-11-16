#ifndef IsingModel_HPP
#define IsingModel_HPP
#include <iostream>
#include <cmath>
#include <fstream>      // Write to file
#include <iomanip>      // Text formatting
#include <cstdlib>
#include <ctime>
#include <string>

using namespace std;

class IsingModel{
protected:
  int m_L;
  double m_temp;
  int m_N;
  double *m_spin;
  double m_E;
  double m_M;
  double *m_BoltzmannFactor;
  int m_J;
  int Periodic(int i, int add);
  void Metropolis();    // Solving using the Metropolis algorithm
  double m_Eavg;        // Gjennomsnittlig energi
  double m_Mavg;        // Gjennomsnittlig magnetisering (absoluttverdi!)
  double m_CV;
  double m_chi;

public:
  void Initialize(int L, double T);
  void MonteCarlo(int cycles);
  void Write_to_file(); // Write results to file
};

#endif
