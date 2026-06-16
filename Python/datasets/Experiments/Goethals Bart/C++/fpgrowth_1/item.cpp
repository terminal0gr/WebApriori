/*----------------------------------------------------------------------
  File    : item.cpp
  Contents: itemset management
  Author  : Bart Goethals
  Update  : 04/04/2003
  ----------------------------------------------------------------------*/

#include <stdio.h>
#include "item.h"

Item_::Item_()
{
  supp = 0;
  parent = 0;
  nodelink = 0;
  id = 0;
  children = 0;
}

Item_::~Item_()
{}

Item::Item(int s, Item_ *p)
{
  item = new Item_();
  item->id = s;
  item->parent = p;
}

Item::Item(const Item& i)
{
  Item_ *tmp = i.getItem();

  item = new Item_();
  item->id  = tmp->id;
  item->parent = tmp->parent;
  item->children = tmp->children;
  item->nodelink = tmp->nodelink;
  item->supp = tmp->supp;
}

Item::~Item()
{
  delete item;
}

set<Item> *Item::makeChildren() const
{
  if(item->children==0) item->children = new set<Item>;
  return item->children;
}


void Item::removeChildren() const
{
  set<Item> *items = item->children;
  for(set<Item>::iterator it = items->begin();it != items->end(); it++) it->removeChildren();
  delete item->children;
  item->children = 0;
}
