/*----------------------------------------------------------------------
  File    : item.h
  Contents: itemset management
  Author  : Bart Goethals
  Update  : 13/5/2005
----------------------------------------------------------------------*/

#include <vector>
using namespace std;

class Item
{
 public:

  Item(unsigned i, unsigned s = 0) : id(i), support(s) {}

  bool operator< (const Item &i) const {return support < i.support;}

  mutable vector<unsigned> transactions;
  unsigned id;
  unsigned support;
};
