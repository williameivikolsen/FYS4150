#include "jacobi.hpp"
#include <iostream>
#include <cmath>

using namespace std;

int main() {
    int n = 10;
    double epsilon = 1e-8;

    Jacobi my_solver;
    my_solver.Initialize(n, epsilon);
    my_solver.Loop();
    return 0;
}