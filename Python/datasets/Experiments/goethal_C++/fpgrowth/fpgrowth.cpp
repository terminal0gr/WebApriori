/*----------------------------------------------------------------------
  File    : fpgrowth.cpp
  Contents: fpgrowth algorithm for finding frequent sets
  Author  : Bart Goethals
  Update  : 04/04/2003
  16/04/2003 support of {} also sent to output
  ----------------------------------------------------------------------*/

#include <iostream>
#include <stdio.h>
#include <windows.h>
#include <psapi.h>
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


  //Malliaridis 26/11/2024 transform Absolute Minimum Support to Relative Minimum Support [0...1] and vice versa
  if (minsup==0) {
    minsup=static_cast<int>(std::ceil(minsup0_1 * tnr));
  } else {
    minsup0_1=(double)minsup/tnr;
  }
  printf("Relative minSupp: %.3lf\n", minsup0_1);
  cout << "transactions: " << tnr << endl;
  cout << "Absolute minSup: " << minsup << endl;

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
  frequentItemsetsCount = fpt->grow(tmp,1);
  delete [] tmp;
  delete [] FPtree::remap;
  delete FPtree::relist;
  cout << "Frequent sets generated [" << (clock()-start)/double(CLOCKS_PER_SEC) << "s]" << endl;

  return frequentItemsetsCount;
}

//Malliaridis 27/11/2024
int FPgrowth::printInfo(double elapsed, double threshold, char* filename, char* algorithm, char* creator) {
	
	PROCESS_MEMORY_COUNTERS pmc;
  if (!GetProcessMemoryInfo(GetCurrentProcess(), &pmc, sizeof(pmc))) {
    printf("Failed to retrieve memory info.");
    return 0;
  }

  // Extract the base name from the full path
  char *lastSlash = strrchr(filename, '\\'); // Find the last backslash (Windows path separator)
  if (lastSlash == nullptr) {
    lastSlash = filename; // If no backslash, use the whole filename
  } else {
    lastSlash++; // Move past the backslash
  }

  // Extract the base name (without extension) from filename
  char *dot = strrchr(lastSlash, '.'); // Find the last dot
  size_t baseLength = (dot != nullptr) ? (dot - lastSlash) : strlen(lastSlash);
  char base[256];
  strncpy(base, lastSlash, baseLength);
  base[baseLength] = '\0'; // Null-terminate the base name
  // Construct the output filename
  // Buffer to hold the dynamically constructed filename
  char outFilename[256];    
  sprintf(outFilename, "../../output/%s_%.3lf_%s_%s.json", base, threshold, algorithm, creator);

  FILE *outFile = fopen(outFilename, "wt");

  fprintf(outFile, "{\n",elapsed);
	fprintf(outFile, "    \"algorithm\": \"%s\",\n",algorithm);
	fprintf(outFile, "    \"language\": \"C++\",\n");
	fprintf(outFile, "    \"library\": \"%s\",\n",creator);
	fprintf(outFile, "    \"minSup\": %.3lf,\n",threshold);
	fprintf(outFile, "    \"totalFI\": %d,\n",frequentItemsetsCount);
	fprintf(outFile, "    \"runtime\": %.3lf,\n",elapsed);
  fprintf(outFile, "    \"memory\": %d\n",pmc.PeakWorkingSetSize);
  fprintf(outFile, "}\n",elapsed);
  fclose(outFile);
  
  return 1;
}
