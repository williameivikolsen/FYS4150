#include <iostream>
#include <cmath>
// use namespace for output and input
using namespace std;

int main(int argc, char *argv[]){
    // Read output file name and number of grid points
    int n;
    string filename;
    if( argc <= 1 ){
          cout << "Bad Usage: " << argv[0] <<
              " needs file name and number of grid points when executed" << endl;
          exit(1);
    }
        else{
        filename = argv[1]; // first command line argument after name of program
        n = atoi(argv[2]);
    }
    int i;
    for (i = 1; i < n; i++) {
        cout << "Hei" << "\n";
    }
}