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
    eclat.setMinsup(atoi(argv[2]));
    if(argc==4) eclat.setOutput(argv[3]);
    
    cout << eclat.mine() << endl;
    return 0;
  }
}
