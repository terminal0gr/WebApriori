/*----------------------------------------------------------------------
  File    : data.cpp
  Contents: data set management
  Author  : Bart Goethals
  Update  : 13/5/2005
  ----------------------------------------------------------------------*/

#include <vector>
using namespace std;
#include "data.h"

Transaction::Transaction(const Transaction &tr)
{
  length = tr.length;
  t = new int[tr.length];
  for(int i=0; i< length; i++) t[i] = tr.t[i];
}

Data::Data(char *filename)
{
  fn = filename;
  in = fopen(fn,"rt");
}

Data::~Data()
{
  if(in) fclose(in);
}


Transaction *Data::getNext()
{
  vector<int> list;
  char c;

  // read list of items
  do {
    int item=0, pos=0;
    c = getc(in);
    while((c >= '0') && (c <= '9')) {
      item *=10;
      item += int(c)-int('0');
      c = getc(in);
      pos++;
    }
    if(pos) list.push_back(item);
  }while(c != '\n' && !feof(in));
  
  if(feof(in)) return 0;
  // Note, also last transaction must end with newline, 
  // else, it will be ignored
  
  // put items in Transaction structure
  Transaction *t = new Transaction(list.size());
  for(int i=0; i<int(list.size()); i++)
    t->t[i] = list[i];

  return t;
}
