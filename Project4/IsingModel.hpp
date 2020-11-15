#ifndef IsingModel_HPP
#define IsingModel_HPP
#include <iostream>
#include <cmath>
#include <fstream>      // Write to file
#include <iomanip>      // Text formatting
#include <cstdlib>
#include <ctime>

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
public:
  void Initialize(int L, double T);
  void Metropolis();    // Solving using the Metropolis algorithm
  void Write_to_file(); // Write results to file
};

#endif
