/*----------------------------------------------------------------------
  File    : fptree.cpp
  Contents: fpgrowth algorithm for finding frequent sets
  Author  : Bart Goethals
  Update  : 08/04/2003 - single prefix path bug fixed (Thanks to Xiaonan Wang)
  ----------------------------------------------------------------------*/

#include <iostream>
#include <stdio.h>
#include <set>
using namespace std;
#include "data.h"
#include "item.h"
#include "fptree.h"

int *FPtree::remap = 0;
set<Element> *FPtree::relist = 0;

FPtree::FPtree()
{
  root = new set<Item>;
  nodes = 0;
  singlepath=true;
}

FPtree::~FPtree()
{
  set<Item>::iterator it;

  for(it = root->begin(); it != root->end(); it++)
    it->removeChildren();
  delete root;
}

int FPtree::processItems(Transaction *t, int times)
{
  set<Item>::iterator head;
  int added=0;

  for(int depth=0; depth < t->length; depth++) {
    head = header.find(Item(t->t[depth], 0));
    if(head == header.end()) {
      head = header.insert(Item(t->t[depth], 0)).first;
      added++;
    }
    head->Increment(times);
  }

  return added;
}

int FPtree::processTransaction(Transaction *t, int times)
{
  set<Item>::iterator it, head;
  set<Item>* items = root;
  Item_ *current = 0;
  int added=0;
	
  for(int depth=0; depth < t->length; depth++) {
    head = header.find(Item(t->t[depth], 0));
    if(head != header.end()) {
      it = items->find(Item(t->t[depth], 0));

      if(it == items->end()) {
	it = items->insert(Item(t->t[depth], current)).first;
	it->setNext(head->getNext());
	head->setNext(it->getItem());
	nodes++;
	added++;
	if(singlepath && (items->size()>1)) singlepath=false; 		
      }

      it->Increment(times);
      current = it->getItem();
      items = it->makeChildren();
    }
  }

  return added;
}

int FPtree::grow(int *current, int depth)
{
  int added=0, factor=1;
  if(header.size() == 0) return 0;

  if(singlepath) { 
    int *comb = new int[header.size()];
    int cl=0;
    for(set<Item>::iterator it=header.begin(); it != header.end(); it++) {
      current[depth-1] = it->getId(); 
      print(current,depth,comb,cl,it->getSupport());
      comb[cl++] = it->getId();
      added += factor;
      factor *= 2;
    }
    delete [] comb;
  }
  else {
    for(set<Item>::iterator it=header.begin(); it != header.end(); it++) {
      Item_ *i;
      current[depth-1] = it->getId(); 
      FPtree *cfpt = new FPtree();
      cfpt->setMinsup(minsup);
      cfpt->setOutput(out);

      int *tmp = new int[header.size()];
      for(i = it->getNext(); i; i = i->nodelink) {
	int l=0;
	for(Item_ *p=i->parent; p; p = p->parent) tmp[l++] = p->id;
	Transaction *t = new Transaction(l);
	for(int j=0; j<l; j++) t->t[j] = tmp[l-j-1];
	cfpt->processItems(t,i->supp);
	delete t;
      }
      cfpt->Prune();
      for(i = it->getNext(); i; i = i->nodelink) {
	int l=0;
	for(Item_ *p=i->parent; p; p = p->parent) tmp[l++] = p->id;
	Transaction *t = new Transaction(l);
	for(int j=0; j<l; j++) t->t[j] = tmp[l-j-1];
	cfpt->processTransaction(t,i->supp);
	delete t;
      }
      delete [] tmp;
      print(current,depth,0,0,it->getSupport());
      added ++;
      added += cfpt->grow(current,depth+1);
      delete cfpt;
    }
  }
  return added;
}

int FPtree::Prune()
{
  int left=0;
	
  for(set<Item>::iterator it = header.begin();it != header.end(); ) {
    if(it->getSupport() < minsup) {
      set<Item>::iterator tmp = it++;
      header.erase(tmp);
    }
    else {
      left++;
      it++;
    }
  }
  return left;
}

void FPtree::ReOrder()
{
  set<Item>::iterator itI;
  multiset<Element>::iterator itE;
  multiset<Element> list;
	
  for(itI = header.begin(); itI != header.end(); itI++)
    list.insert(Element(itI->getSupport(), itI->getId()));
	
  remap = new int[list.size()+1];
  relist = new set<Element>;
  header.clear();
  int i=1;
  for(itE=list.begin(); itE!=list.end(); itE++) {
    if(itE->support >= minsup) {
      remap[i] = itE->id;
      relist->insert(Element(itE->id,i));
      Item a(i,0);
      itI = header.insert(a).first;
      itI->Increment(itE->support);
      i++;
    }
  }
}

void FPtree::print(int *itemset, int il, int *comb, int cl, int support, int spos, int depth, int *current)
{
  if(current==0) {
    if(out) {
      set<int> outset;
      for(int j=0; j<il; j++) outset.insert(remap[itemset[j]]); 
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
      for(int i=0; i<depth; i++) outset.insert(remap[current[i]]); 
      for(int j=0; j<il; j++) outset.insert(remap[itemset[j]]); 
      for(set<int>::iterator k=outset.begin(); k!=outset.end(); k++) fprintf(out, "%d ", *k);
      fprintf(out, "(%d)\n", support);
      print(itemset, il, comb, cl, support, spos+1, depth+1, current);
    }
  }
}
