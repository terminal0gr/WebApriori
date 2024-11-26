/*----------------------------------------------------------------------
  File    : fptree.h
  Contents: fpgrowth algorithm for finding frequent sets
  Author  : Bart Goethals
  Update  : 8/4/2003 - single prefix path bug fixed (Thanks to Xiaonan Wang)
  ----------------------------------------------------------------------*/

#include <set>

using namespace std;

class Element
{
 public:
  Element(int s, int i) : support(s), id(i){}
	
  int support;
  int id;
  bool operator< (const Element  &e) const {return support > e.support;}
};

class FPtree
{
 public:
	
  FPtree();
  ~FPtree();
	
  int processTransaction(Transaction *t, int times=1);
  int processItems(Transaction *t, int times=1);
  void setMinsup(int ms) {minsup = ms;}
  int grow(int *current, int depth);
  void ReOrder();
  int Prune();
  void setOutput(FILE *of) {out =of;}
  void print(int *itemset, int il, int *comb, int cl, int support, int spos=0, int depth=0, int *current=0);

  static int *remap;
  static set<Element> *relist;
	
 private:
	
  set<Item> header;
  set<Item> *root;
  int minsup;
  unsigned nodes;
  bool singlepath;

  FILE *out;
};
