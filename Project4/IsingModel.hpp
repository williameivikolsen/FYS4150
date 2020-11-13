#ifndef IsingModel_HPP
#define IsingModel_HPP
#include <iostream>
#include <cmath>
#include <fstream>      // Write to file
#include <iomanip>      // Text formatting
#include "time.h"       // Timer

using namespace std;

class IsingModel{
public:
  void Periodic_bounds();
  void Initialize();
  void Metropolis();    // Solving using the Metropolis algorithm
  void Write_to_file(); // Write results to file
};

#endif
