/*----------------------------------------------------------------------
  File    : testeclat.cpp
  Contents: eclat algorithm for finding frequent sets
  Author  : Bart Goethals
  Update  : 13/5/2005
----------------------------------------------------------------------*/

#include <iostream>
using namespace std;
#include <stdlib.h>
#include <stdio.h>
#include <cmath>
#include "data.h"
#include "item.h"
#include "eclat.h"

int main(int argc, char *argv[])
{
  if(argc < 3) {
    cerr << "usage: " << argv[0] << " datafile minsup [output]" << endl;
    return 1;
  }
  else {
    Eclat eclat;
    
    eclat.setData(argv[1]);
    // Malliaridis read minSup with both Absolute Minimum Support and Relative Minimum Support [0...1]
    double ms = std::atof(argv[2]); //reads string argument as double
    if (ms>1) {
      eclat.setMinsup(static_cast<int>(std::floor(ms)));
    } else {
      eclat.setMinsup0_1(ms);
    }
    //eclat.setMinsup(atoi(argv[2]));



    if(argc==4) eclat.setOutput(argv[3]);
    
    clock_t start = clock();
    eclat.mine();
    double elapsed=(clock()-start)/double(CLOCKS_PER_SEC);

    eclat.printInfo(elapsed,eclat.getMinsup0_1(),argv[1], "Eclat", "Goethal", "cpp");

    printf("C++ Goethals Eclat Done!");

    return 0;
  }
}
