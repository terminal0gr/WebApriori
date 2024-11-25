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
	void setOutput(char *of){out = fopen(of, "wt");}
	
	double mine();
		
protected:
	
	double grow(multiset<Item> *items, unsigned supp, int *itemset, int depth, int *comb, int cl);
	void print(int *itemset, int il, int *comb, int cl, int support, int spos = 0, int depth = 0, int *current = 0);	

	unsigned minsup;
	Data *data;	
	FILE *out;
};
