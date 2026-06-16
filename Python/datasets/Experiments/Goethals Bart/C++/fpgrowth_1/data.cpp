/*----------------------------------------------------------------------
  File    : data.cpp
  Contents: data set management
  Author  : Bart Goethals
  Update  : 04/04/2003
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

Data::Data(char *filename, int t)
{
  fn = filename;
  type = t;
  current=0;

  if(type>1) in = fopen(fn,"rt");
  else in = fopen(fn,"rb");
}

Data::~Data()
{
  if(in) fclose(in);
}

Transaction *Data::getNext()
{
  Transaction *t=0;

  switch(type){
  case 1: t= getNextBin(); break;
  case 2: t= getNextAs(); break;
  case 3: t= getNextAsFlat(); break;
  case 4: t= getNextAsQuest(); break;
  }

  if(t) current++;
  else {
    rewind(in);
    current=0;
  }

  return t;
}

Transaction *Data::getNextAs() 
{
  Transaction *t;
  int tid, item, i, dummy;
  vector<int> list;
  static int cur=0,prev=-1;
  static bool begin=true;
  
  if(feof(in)) {
    begin=true;
    prev=-1;
    return 0;
  }

  if(!begin) list.push_back(cur);
  else begin=false;

  while(true) {
    fscanf(in, "%d %d %d",&dummy, &tid, &item);
    if(feof(in)) {
      int size=list.size();
      t = new Transaction(size);
      for(i=0; i<size; i++) t->t[i] = list[i];
      list.clear();

      return t;
    }
    else if(prev<0)	prev=tid;
    else if(tid != prev){
      prev = tid;
      cur = item;
      int size=list.size();
      t = new Transaction(size);
      for(i=0; i<size; i++) t->t[i] = list[i];
      list.clear();
			
      return t;
    }

    list.push_back(item);
  }
}

Transaction *Data::getNextAsFlat()
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
  
  // if end of file is reached, rewind to beginning for next pass
  if(feof(in)){
    rewind(in);
    return 0;
  }
  // Note, also last transaction must end with newline, 
  // else, it will be ignored
  
  // sort list of items
  // sort(list.begin(),list.end());

  // put items in Transaction structure
  Transaction *t = new Transaction(list.size());
  for(int i=0; i<int(list.size()); i++)
    t->t[i] = list[i];

  return t;
}

Transaction *Data::getNextAsQuest()
{
  int tmptid, tid,l,i;
  Transaction *t;
	
  fscanf(in,"%d %d %d",&tmptid,&tid,&l);
  if(feof(in)) return 0;
	
  t = new Transaction(l);
  for(i=0; i<l; i++) fscanf(in,"%d",&t->t[i]);
  return t;
}

Transaction *Data::getNextBin()
{
  int tmptid, tid,l,i;
  Transaction *t;
	
  fread(&tmptid,4, 1,in);
  if(feof(in)) return 0;
	
  fread(&tid,4, 1,in);
  fread(&l,4, 1,in);
  t = new Transaction(l);
  for(i=0; i<l; i++) fread(&t->t[i],4, 1,in);

  return t;
}
