/*----------------------------------------------------------------------
  File    : fpgrowth.cpp
  Contents: fpgrowth algorithm for finding frequent sets
  Author  : Bart Goethals
  Update  : 04/04/2003
  16/04/2003 support of {} also sent to output
  ----------------------------------------------------------------------*/

#include <iostream>
#include <stdio.h>
#include <vector>
#include <algorithm>
#include <cmath>   // For std::ceil
using namespace std;
#include <time.h>
#include "data.h"
#include "item.h"
#include "fptree.h"
#include "fpgrowth.h"

FPgrowth::FPgrowth() : data(0), out(0)
{
  fpt = new FPtree();
}

FPgrowth::~FPgrowth()
{
  if(data) delete data;
  if(fpt) delete fpt;
}

void FPgrowth::setOutput(char *of)
{
  out = fopen(of, "wt");
}

int FPgrowth::mine()
{
  int added=0;
  clock_t start;

  fpt->setOutput(out);

  start = clock();
  int tmin=1000000, tmax=0, ttotal=0, tnr=0;
  while(Transaction *t = data->getNext()) {
    if(t->length) {
      fpt->processItems(t);
      ttotal += t->length;
      if(t->length < tmin) tmin = t->length;
      if(t->length > tmax) tmax = t->length;
    }
    delete t;
    tnr++;
  }

  //Malliaridis 26/11/2024 transform minsupp from percentage to actual number
  minsup=static_cast<int>(std::ceil(minsup0_1 * tnr));
  cout << "minSupp perc: " << minsup0_1 << endl;
  cout << "transactions: " << tnr << endl;
  cout << "Actual minSup: " << minsup << endl;

  fpt->setMinsup(minsup);


  cout << "items read [" << (clock()-start)/double(CLOCKS_PER_SEC) << "s]" << endl;

  start = clock();
  fpt->ReOrder();
  fpt->Prune();
  cout << "items reordered and pruned [" << (clock()-start)/double(CLOCKS_PER_SEC) << "s]" << endl;

  start = clock();
  while(Transaction *t = data->getNext()) {
    int i;
    vector<int> list;
    for(i=0; i<t->length; i++) {
      set<Element>::iterator it = fpt->relist->find(Element(t->t[i],0));
      if(it!=fpt->relist->end()) list.push_back(it->id);
    }
    int size=list.size();
    sort(list.begin(), list.end());
    delete t;

    t = new Transaction(size);
    for(i=0; i<size; i++) t->t[i] = list[i];
    if(t->length) fpt->processTransaction(t);
    delete t;
  }
  cout << "FPtree constructed [" << (clock()-start)/double(CLOCKS_PER_SEC) << "s]" << endl;

  if(out) fprintf(out,"(%d)\n", tnr);

  start = clock();
  int *tmp  = new int[100];
  added = fpt->grow(tmp,1);
  delete [] tmp;
  delete [] FPtree::remap;
  delete FPtree::relist;
  cout << "Frequent sets generated [" << (clock()-start)/double(CLOCKS_PER_SEC) << "s]" << endl;

  return added;
}
