/*----------------------------------------------------------------------
  File    : eclat.h
  Contents: eclat algorithm for finding frequent sets
  Author  : Bart Goethals
  Update  : 13/5/2005
----------------------------------------------------------------------*/

#include <set>
using namespace std;

class Eclat
{
public:
	
	Eclat();
	~Eclat();
	
	void setData(char *file){data = new Data(file);}
	void setMinsup(unsigned ms){minsup = ms;}
	void setMinsup0_1(double ms){minsup0_1=ms;}
	double getMinsup0_1(){return minsup0_1;}
	void setOutput(char *of){out = fopen(of, "wt");}
	int printInfo(double elapsed, double threshold, char* filename, char* algorithm, char* creator, char* language);	
	
	unsigned mine();
		
protected:
	
	double grow(multiset<Item> *items, unsigned supp, int *itemset, int depth, int *comb, int cl);
	void print(int *itemset, int il, int *comb, int cl, int support, int spos = 0, int depth = 0, int *current = 0);	
  	unsigned getfrequentItemsetsCount(){return frequentItemsetsCount;}	

	unsigned minsup=0;
	double minsup0_1=0;
    unsigned frequentItemsetsCount=0;

	Data *data;	
	FILE *out;
};
