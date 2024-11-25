/*----------------------------------------------------------------------
  File    : eclat.cpp
  Contents: eclat algorithm for finding frequent sets
  Author  : Bart Goethals
  Update  : 13/5/2005
  ----------------------------------------------------------------------*/

#include <iostream>
#include <algorithm>
using namespace std;
#include <stdio.h>
#include "data.h"
#include "item.h"
#include "eclat.h"

Eclat::Eclat() : data(0), out(0) {}

Eclat::~Eclat() 
{
  if(data) delete data;
  if(out) fclose(out);
}

double Eclat::mine() 
{
  unsigned tnr = 0;
  set<Item> root;
  multiset<Item> *allitems = new multiset<Item>;  
  set<Item>::iterator it;
	
  // read all transactions
  while(Transaction *t = data->getNext()) {
    for(int i=0; i<t->length;i++) {
      it = root.find(Item(t->t[i],t->t[i]));
      if(it == root.end()) it = root.insert(Item(t->t[i],t->t[i])).first;
      it->transactions.push_back(tnr);
    }
    tnr++;
    delete t;
  }

  // remove infrequent items and put items in support ascending order
  while((it = root.begin()) != root.end()) {
    if(it->transactions.size() >= minsup) {
      Item item(it->id, it->transactions.size());
      item.transactions = it->transactions;
      allitems->insert(item);
    }
    root.erase(it);
  }
  if(out) fprintf(out,"(%d)\n",tnr);

  // finding all itemsets
  int *itemset = new int[allitems->size()];
  int *comb = new int[allitems->size()];
  double added = grow(allitems, tnr, itemset, 1, comb, 0);
  delete [] comb;
  delete [] itemset;
  delete allitems;

  return added+1;
}

double Eclat::grow(multiset<Item> *items, unsigned supp, int *itemset, int depth, int *comb, int cl)
{
  double added = 0;
  const int sw = 2;
  
  while(!items->empty()) {
    int factor = 1, cbl = cl;
    multiset<Item> *children = new multiset<Item>;    
    multiset<Item>::iterator it2, it = items->begin();
    itemset[depth-1] = it->id;

    for(it2 = it, it2++; it2 != items->end(); it2++) {
      Item item(it2->id);
      insert_iterator< vector<unsigned> > res_ins(item.transactions, item.transactions.begin());
      
      if(depth < sw) { // make tidlists
	set_intersection(it->transactions.begin(), it->transactions.end(), it2->transactions.begin(), it2->transactions.end(), res_ins);
	item.support = item.transactions.size();
      } else { // make diffsets
	if(depth == sw) set_difference(it->transactions.begin(), it->transactions.end(), it2->transactions.begin(), it2->transactions.end(), res_ins);
	else set_difference(it2->transactions.begin(), it2->transactions.end(), it->transactions.begin(), it->transactions.end(), res_ins);
	item.support = it->support - item.transactions.size();
      }

      if(item.support == it->support) {
	factor *= 2;
        comb[cbl++] = item.id;
      } else if(item.support >= minsup) children->insert(item); 
    }
    print(itemset, depth, comb, cbl, it->support);
    added += factor + (factor * grow(children, it->support, itemset, depth+1, comb, cbl)); 
    delete children;
    items->erase(it);
  }

  return added;
}

void Eclat::print(int *itemset, int il, int *comb, int cl, int support, int spos, int depth, int *current)
{
  if(current==0) {
    if(out) {
      set<int> outset;
      for(int j=0; j<il; j++) outset.insert(itemset[j]); 
      for(set<int>::iterator k=outset.begin(); k!=outset.end(); k++) fprintf(out, "%d ", *k);
      fprintf(out, "(%d)\n", support);
      if(cl) {
        current = new int[cl];
        print(itemset,il,comb,cl,support,0,1,current);
        delete [] current;
      }
    }
  }
  else {
    int loper = spos;
    spos = cl;
    while(--spos >= loper) {
      set<int> outset;
      current[depth-1] = comb[spos];
      for(int i=0; i<depth; i++) outset.insert(current[i]);
      for(int j=0; j<il; j++) outset.insert(itemset[j]);
      for(set<int>::iterator k=outset.begin(); k!=outset.end(); k++) fprintf(out, "%d ", *k);
      fprintf(out, "(%d)\n", support);
      print(itemset, il, comb, cl, support, spos+1, depth+1, current);
    }
  }
}
