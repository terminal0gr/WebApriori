/*----------------------------------------------------------------------
  File     : testfpgrowth.cpp
  Contents : FP-growth algorithm for finding frequent sets
  Author   : Bart Goethals
  Update   : 04/04/2003
----------------------------------------------------------------------*/

#include <iostream>
using namespace std;
#include <stdlib.h>
#include <cmath>
#include <time.h>
#include "data.h" 
#include "item.h"
#include "fptree.h"
#include "fpgrowth.h"

int main(int argc, char *argv[])
{
  cout << "FP-growth frequent itemset mining implementation" << endl;
  cout << "by Bart Goethals, 2000-2003" << endl;
  cout << "http://www.cs.helsinki.fi/u/goethals/" << endl << endl;
  
  if(argc < 4){
    cerr << "usage: " << argv[0] << " datafile datatype minsup [output]" << endl;
    cerr << "datatype = 1 for Quest datagenerator binary" << endl;
    cerr << "datatype = 2 for Quest datagenerator ascii" << endl;
    cerr << "datatype = 3 for flat, i.e. all items per transaction on a single line" << endl;
    cerr << "datatype = 4 for ascii version of Quest datagenerator binary" << endl;
  }
  else{
    FPgrowth *fpgrowth = new FPgrowth();
    
    fpgrowth->setData(argv[1],atoi(argv[2]));
    
    // Malliaridis read minSup with both Absolute Minimum Support and Relative Minimum Support [0...1]
    double ms = std::atof(argv[3]); //reads string argument as double
    if (ms>1) {
      fpgrowth->setMinsup(static_cast<int>(std::floor(ms)));
    } else {
      fpgrowth->setMinsup0_1(ms);
    }
    //fpgrowth->setMinsup(atoi(argv[3]));

    if(argc==5) fpgrowth->setOutput(argv[4]);
    
    clock_t start = clock();
    int added = fpgrowth->mine();
    double elapsed=(clock()-start)/double(CLOCKS_PER_SEC);
    cout << added << "\t[" << elapsed << "s]" << endl;
    if(argc==5) cout << "Frequent sets written to " << argv[4] << endl;
    
    fpgrowth->printInfo(elapsed,fpgrowth->getMinsup0_1(),argv[1], "FPGrowth", "Goethal", "cpp");

    delete fpgrowth;
  }
  
  return 0;
}
