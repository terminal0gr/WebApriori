/*----------------------------------------------------------------------
  File    : Data.h
  Contents: data set management
  Author  : Bart Goethals
  Update  : 13/5/2005
----------------------------------------------------------------------*/

#include <stdio.h>

class Transaction
{
public:
	
	Transaction(int l) : length(l) {t = new int[l];}
	Transaction(const Transaction &tr);
	~Transaction(){delete t;}
	
	int length;
	int *t;
};

class Data
{
 public:
	
	Data(char *filename);
	~Data();
	
	Transaction *getNext();

 private:
	
	FILE *in;
	char *fn;
};
