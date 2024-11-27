/* 
 * File:   negFIN.cpp
 * Author: Nader Aryabarzan
 *
 * Created on March 3, 2017, 9:51 PM.
 * These codes are the implemantation of negFIN algorithm, the frequent itemsets mining algorithm.
 * These codes are implemebted based on FIN algorithm.
 */

#include <cstdlib>
#include <windows.h>
#include <psapi.h>
#include<iostream>
#include <stdio.h>
#include <cmath>
#include<time.h>
#include <cstring>
#include <ctime>

using namespace std;
int dump;



//======================== NegNodeSet
int **___buffer;
int ___bf_cursor;
int ___bf_size;
int ___bf_col;
int ___bf_currentSize;



int ___numOfFItem;
int ___Min_Support;

struct ___Item {
    int index;
    int num;
};

___Item * ___item;

struct ___NodeListTreeNode {
    int label;
    ___NodeListTreeNode* firstChild;
    ___NodeListTreeNode* next;
    int support;
    int NLStartinBf;
    int NLLength;
    int NLCol;
    //LinkItem *sameItemList;
};

struct ___PPCTreeNode {
    int label;
    ___PPCTreeNode* firstChild;
    ___PPCTreeNode* rightSibling;
    ___PPCTreeNode* father;
    int count;
    //	int foreIndex;
    ///YYY ??? inserted
    __int128 code;
    ///END YYY ??? inserted
};

___PPCTreeNode *___ppcRoot;

___NodeListTreeNode ___nlRoot;
int ___nlNodeCount = 0;
int ___resultCount = 0;
long long ___nlLenSum = 0;

FILE *___out;

int *___result;
int ___resultLen = 0;
///YYY ??? inserted
__int128 * ___mask_for_item;
///END YYY ??? inserted

void ___showMemoryInfo(void) {
    HANDLE handle = GetCurrentProcess();
    PROCESS_MEMORY_COUNTERS pmc;
    //    GetProcessMemoryInfo(handle,&pmc,sizeof(pmc));
    cout << pmc.PeakWorkingSetSize / 1000 << endl;
}

int ___comp(const void *a, const void *b) {
    return (*(___Item *) b).num - (*(___Item *) a).num;
}

void ___getData(FILE * in, char *filename, double support) {
    if ((in = fopen(filename, "r")) == NULL) {
        cout << "read wrong!" << endl;
        fclose(in);
        exit(1);
    }

    char str[500];
    ___Item **tempItem = new ___Item*[10];
    tempItem[0] = new ___Item[10000];
    for (int i = 0; i < 10000; i++) {
        tempItem[0][i].index = i;
        tempItem[0][i].num = 0;
    }

    int numOfTrans = 0;
    int size = 1;
    int numOfItem = 0;
    int num = 0;
    int col = 0;
    while (fgets(str, 500, in)) {
        //???XXX Commented
        //		if(feof(in)) break;
        numOfTrans++;
        num = 0;
        for (int i = 0; i < 500 && str[i] != '\0'; i++) {
            if (str[i] != ' ') num = num * 10 + str[i] - '0';
            else {
                col = num / 10000;
                if (col >= size) {
                    for (int j = size; j <= col; j++) {
                        tempItem[j] = new ___Item[10000];
                        for (int p = 0; p < 10000; p++) {
                            tempItem[j][p].index = j * 10000 + p;
                            tempItem[j][p].num = 0;
                        }
                    }
                    size = col + 1;
                }
                if (0 == tempItem[col][num % 10000].num++) numOfItem++;
                num = 0;
            }
        }
        //XXX inserted
        if (feof(in)) break;
    }
    fclose(in);

    ___Min_Support = int(support * numOfTrans);
    ___item = new ___Item[numOfItem];
    for (int i = 0, p = 0; i < size; i++)
        for (int j = 0; j < 10000; j++)
            if (tempItem[i][j].num != 0)
                ___item[p++] = tempItem[i][j];

    for (int i = 0; i < size; i++)
        delete[] tempItem[i];
    delete[] tempItem;

    qsort(___item, numOfItem, sizeof (___Item), ___comp);
    for (___numOfFItem = 0; ___numOfFItem < numOfItem; ___numOfFItem++)
        if (___item[___numOfFItem].num < ___Min_Support)
            break;

    //YYY ??? inserted
    cout<<"num of 1-frequent item"<<___numOfFItem<<endl;
    ___mask_for_item = new __int128[___numOfFItem];
    for (int i = 0; i < ___numOfFItem; i++) {
        ___mask_for_item[i] = (__int128) pow(2, ___numOfFItem - 1 - i);

    }
}

//YYY ??? Commented
//int *itemsetCount;
//YYY ??? Commented
//int *nlistBegin;
int ___nlistCol;
//YYY ??? Commented
//int *nlistLen;
int ___firstNlistBegin;

//YYY ??? inserted
//int *_itemsetCount;
int *___nlistBegin;
int *___nlistLen;
//END YYY ??? inserted

int ___PPCNodeCount;
int *___SupportDict;
//YYY ??? inserted
__int128 *___CodeDict;
//END YYY ??? inserted
int *___sameItems;

void ___buildTree(FILE *in, char * filename) {
    if ((in = fopen(filename, "r")) == NULL) {
        cout << "read wrong!" << endl;
        fclose(in);
        exit(1);
    }

    ___PPCNodeCount = 0;
    //XXX ??? inserted

    ___ppcRoot = new ___PPCTreeNode;
    //XXX ??? commented
    //ppcRoot.label = -1;
    //XXX ??? BEGIN inserted
    ___ppcRoot->label = -1;
    ___ppcRoot->count = 0;
    ___ppcRoot->father = NULL;
    ___ppcRoot->firstChild = NULL;
    ___ppcRoot->rightSibling = NULL;
    //        _ppcRoot->foreIndex = 0;
    ___ppcRoot->code = 0;
    //XXX ??? END inserted

    //YYY ??? inserted
    //        _itemsetCount = new int[ numOfFItem ];
    ___nlistBegin = new int[ ___numOfFItem ];
    ___nlistLen = new int[ ___numOfFItem ];
    //	memset(_itemsetCount, 0, sizeof(int) *  numOfFItem);
    memset(___nlistLen, 0, sizeof (int) * ___numOfFItem);
    //End YYY ??? inserted



    char str[500];
    ___Item transaction[1000];
    for (int i = 0; i < 1000; i++) {
        transaction[i].index = 0;
        transaction[i].num = 0;
    }

    int num = 0, tLen = 0;
    while (fgets(str, 500, in)) {

        num = 0;
        tLen = 0;
        for (int i = 0; i < 500 && str[i] != '\0'; i++) {
            if (str[i] != ' ') num = num * 10 + str[i] - '0';
            else {
                for (int j = 0; j < ___numOfFItem; j++) {
                    if (num == ___item[j].index) {
                        transaction[tLen].index = num;
                        transaction[tLen].num = 0 - j;
                        tLen++;
                        break;
                    }
                }
                num = 0;
            }
        }

        qsort(transaction, tLen, sizeof (___Item), ___comp);
        int curPos = 0;
        //XXX ??? Commented
        //PPCTreeNode *curRoot =&(ppcRoot);
        //XXX ??? inserted
        ___PPCTreeNode *curRoot = ___ppcRoot;

        //        _PPCTreeNode *leftSibling = NULL;
        //        while (curPos != tLen) {
        //            _PPCTreeNode *child = curRoot->firstChild;
        //            while (child != NULL) {
        //                if (child -> label == 0 - transaction[curPos].num) {
        //                    curPos++;
        //                    child->count++;
        //                    curRoot = child;
        //                    break;
        //                }
        //                if (child -> rightSibling == NULL) {
        //                    leftSibling = child;
        //                    child = NULL;
        //                    break;
        //                }
        //                child = child -> rightSibling;
        //            }
        //            if (child == NULL) break;
        //        }
        //        for (int j = curPos; j < tLen; j++) {
        //            _PPCTreeNode *ppcNode = new _PPCTreeNode;
        //            ppcNode->label = 0 - transaction[j].num;
        //
        //            ppcNode->rightSibling = NULL;
        //            ppcNode->firstChild = NULL;
        //            ppcNode->father = curRoot;
        //            ppcNode->count = 1;
        //
        //            if (leftSibling != NULL) {
        //                if (ppcNode->label < curRoot->firstChild->label) {
        //                    ppcNode->rightSibling = curRoot->firstChild;
        //                    curRoot->firstChild = ppcNode;
        //                } else {
        //                    leftSibling = curRoot->firstChild;
        //                    do {
        //                        if (leftSibling->rightSibling == NULL) {
        //                            leftSibling->rightSibling = ppcNode;
        //                            leftSibling = NULL;
        //                            break;
        //                        } else if (ppcNode->label < leftSibling->rightSibling->label) {
        //                            ppcNode->rightSibling = leftSibling->rightSibling;
        //                            leftSibling->rightSibling = ppcNode;
        //                            leftSibling = NULL;
        //                            break;
        //                        } else {
        //                            leftSibling = leftSibling->rightSibling;
        //                        }
        //                    } while (1);
        //
        //                }
        //
        //                //                leftSibling->rightSibling = ppcNode;
        //                leftSibling = NULL;
        //            } else {
        //                curRoot->firstChild = ppcNode;
        //            }
        //
        //            curRoot = ppcNode;
        //            _PPCNodeCount++;
        //            _nlistLen[ppcNode->label]++;
        //        }


        ___PPCTreeNode *leftSibling = NULL;
        while (curPos != tLen) {
            ___PPCTreeNode *child = curRoot->firstChild;
            while (child != NULL) {
                if (child -> label == 0 - transaction[curPos].num) {
                    curPos++;
                    child->count++;
                    //                                        _itemsetCount[child -> label]++;
                    curRoot = child;
                    break;
                }
                if (child -> rightSibling == NULL) {
                    leftSibling = child;
                    child = NULL;
                    break;
                }
                child = child -> rightSibling;
            }
            if (child == NULL) break;
        }
        for (int j = curPos; j < tLen; j++) {
            ___PPCTreeNode *ppcNode = new ___PPCTreeNode;
            ppcNode->label = 0 - transaction[j].num;
            if (leftSibling != NULL) {
                leftSibling->rightSibling = ppcNode;
                leftSibling = NULL;
            } else {
                curRoot->firstChild = ppcNode;
            }
            ppcNode->rightSibling = NULL;
            ppcNode->firstChild = NULL;
            ppcNode->father = curRoot;
            ppcNode->count = 1;
            curRoot = ppcNode;
            ___PPCNodeCount++;
            //_itemsetCount[ppcNode->label]++;
            ___nlistLen[ppcNode->label]++;
        }

        if (feof(in))
            break;
    }
    fclose(in);

    //YYY ??? inserted
    //build 1-itemset nlist
    int _sum = 0;
    for (int i = 0; i < ___numOfFItem; i++) {
        ___nlistBegin[i] = _sum;
        _sum += ___nlistLen[i];
    }

    if (___bf_cursor + _sum > ___bf_currentSize * 0.85) {
        ___bf_col++;
        ___bf_cursor = 0;
        ___bf_currentSize = _sum + 1000;
        ___buffer[___bf_col] = new int[___bf_currentSize];
    }
    ___nlistCol = ___bf_col;
    ___firstNlistBegin = ___bf_cursor;
    ___bf_cursor += _sum;
    //End YYY ??? inserted

    //XXX ??? Commented
    //	PPCTreeNode *root = ppcRoot.firstChild;
    //XXX ??? inserted
    ___PPCTreeNode *root = ___ppcRoot->firstChild;
    int pre = 0;

    //YYY ??? Commented
    /*
    itemsetCount = new int[(numOfFItem-1) * numOfFItem / 2];
    nlistBegin = new int[(numOfFItem-1) * numOfFItem / 2];
    nlistLen = new int[(numOfFItem-1) * numOfFItem / 2];
    memset(itemsetCount, 0, sizeof(int) * (numOfFItem-1) * numOfFItem / 2);
    memset(nlistLen, 0, sizeof(int) * (numOfFItem-1) * numOfFItem / 2);
     */
    ___SupportDict = new int[___PPCNodeCount + 1];
    ___CodeDict = new __int128[___PPCNodeCount + 1];


    while (root != NULL) {
        //		root->foreIndex=pre;
        ___SupportDict[pre] = root->count;

        //		_PPCTreeNode *temp = root->father;
        //YYY ??? inserted
        root->code = root->father->code | ___mask_for_item[root->label];
        ___CodeDict[pre] = root->code;


        int cursor = ___nlistBegin[root->label] + ___firstNlistBegin;
        ___buffer[___nlistCol][cursor] = pre;
        ___nlistBegin[root->label]++;
        //YYY ??? inserted
        pre++;
        //End YYY ??? inserted

        //YYY ??? Commented
        /*
        while(temp->label != -1)
        {
                itemsetCount[root->label * (root->label - 1) / 2 + temp->label] += root->count;
                nlistLen[root->label * (root->label - 1) / 2 + temp->label]++;
                temp = temp->father;
        }
         */
        if (root->firstChild != NULL)
            root = root->firstChild;
        else {
            if (root->rightSibling != NULL)
                root = root->rightSibling;
            else {
                root = root->father;
                while (root != NULL) {
                    if (root->rightSibling != NULL) {
                        root = root->rightSibling;
                        break;
                    }
                    root = root->father;
                }
            }
        }
    }

    //YYY ??? inserted

    for (int i = 0; i < ___numOfFItem; i++)
        ___nlistBegin[i] = ___nlistBegin[i] - ___nlistLen[i];



    //END YYY ??? inserted

    //YYY ??? Commented
    /*
     //build 2-itemset nlist
        
     int sum = 0;
     for(int i = 0; i < (numOfFItem-1)*numOfFItem/2; i++)
             if(itemsetCount[i] >= Min_Support)
             {
                     nlistBegin[i] = sum;
                     sum += nlistLen[i];
             }
         
     if(bf_cursor + sum > bf_currentSize * 0.85)
     {
             bf_col++;
             bf_cursor = 0;
             bf_currentSize = sum + 1000;
             bf[bf_col] = new int[bf_currentSize];
     }
     nlistCol = bf_col;
     firstNlistBegin = bf_cursor;
        
        
     //XXX ??? Commented
    //	root = ppcRoot.firstChild;
     //XXX ??? inserted
     root = ppcRoot->firstChild;
        
        
     bf_cursor += sum;
     while(root != NULL)
     {

         PPCTreeNode *temp = root->father;
         printf("tree node=>label=%d,count=%d \en",temp->label,temp->count);
             while(temp->label != -1)
             {
                     if(itemsetCount[root->label * (root->label - 1) / 2 + temp->label] >= Min_Support)
                     {
                             int cursor = nlistBegin[root->label * (root->label - 1) / 2 + temp->label] + firstNlistBegin;
                             bf[nlistCol][cursor] = root->foreIndex;
                             nlistBegin[root->label * (root->label - 1) / 2 + temp->label] += 1;
                     }
                     temp = temp->father;
             }
             if(root->firstChild != NULL)
                     root = root->firstChild;
             else
             {
                     if(root->rightSibling != NULL)
                             root = root->rightSibling;
                     else
                     {
                             root = root->father;
                             while(root != NULL)
                             {	
                                     if(root->rightSibling != NULL)
                                     {
                                             root = root->rightSibling;
                                             break;
                                     }
                                     root = root->father;
                             }
                     }
             }
     }
     for(int i = 0; i < numOfFItem*(numOfFItem-1)/2; i++)
             if(itemsetCount[i] >= Min_Support)
             {
                     nlistBegin[i] = nlistBegin[i] - nlistLen[i];
             }
     */
}

void ___initializeTree() {
    ___NodeListTreeNode *lastChild = NULL;
    for (int t = ___numOfFItem - 1; t >= 0; t--) {
        ___NodeListTreeNode *nlNode = new ___NodeListTreeNode;
        nlNode->label = t;
        //YYY ??? Commented
        //		nlNode->NLStartinBf = bf_cursor;
        //		nlNode->NLLength = 0;
        //End YYY ??? Commented

        //YYY ??? Inserted
        nlNode->NLStartinBf = ___nlistBegin[t];
        nlNode->NLLength = ___nlistLen[t];
        //End YYY ??? Inserted
        nlNode->NLCol = ___bf_col;
        nlNode->firstChild = NULL;
        nlNode->next = NULL;
        nlNode->support = ___item[t].num;
        if (___nlRoot.firstChild == NULL) {
            ___nlRoot.firstChild = nlNode;
            lastChild = nlNode;
        } else {
            lastChild->next = nlNode;
            lastChild = nlNode;
        }
    }
}

___NodeListTreeNode* ___is2_itemSetValid(___NodeListTreeNode* ni, ___NodeListTreeNode* nj, int level, ___NodeListTreeNode* lastChild, int &sameCount) {

    if (___bf_cursor + ni->NLLength > ___bf_currentSize) {
        ___bf_col++;
        ___bf_cursor = 0;
        ___bf_currentSize = ___bf_size > ni->NLLength * 1000 ? ___bf_size : ni->NLLength * 1000;
        ___buffer[___bf_col] = new int[___bf_currentSize];
    }

    ___NodeListTreeNode *nlNode = new ___NodeListTreeNode;
    nlNode->support = ni->support;
    nlNode->NLStartinBf = ___bf_cursor;
    nlNode->NLCol = ___bf_col;
    nlNode->NLLength = 0;

    //YYY ??? Commneted
    /*
    int cursor_i = ni->NLStartinBf;
    int cursor_j = nj->NLStartinBf;
    int col_j = nj->NLCol;	
     */

    int col_i = ni->NLCol;



    //YYY ???? Commented
    /*
    while(cursor_i < ni->NLStartinBf + ni->NLLength && cursor_j < nj->NLStartinBf + nj->NLLength)
    {
            if(bf[col_i][cursor_i] == bf[col_j][cursor_j])
            {
                    bf[bf_col][bf_cursor++] =  bf[col_j][cursor_j];
                    nlNode->NLLength++;
                    nlNode->support += SupportDict[bf[col_i][cursor_i]];
                    cursor_i += 1;
                    cursor_j += 1;
            }
            else if(bf[col_i][cursor_i] < bf[col_j][cursor_j])
                    cursor_i += 1;
            else
                    cursor_j += 1;
    }
     */


    //YYY ???? inserted
    int nodeIndexI;
    __int128 maskForItemJ = ___mask_for_item[nj->label];
    int endBf = ni->NLStartinBf + ni->NLLength;
    for (int cursor_i = ni->NLStartinBf; cursor_i < endBf; cursor_i++) {
        nodeIndexI = ___buffer[col_i][cursor_i];
        if (!(___CodeDict[nodeIndexI] & maskForItemJ)) {
            ___buffer[___bf_col][___bf_cursor++] = nodeIndexI;
            nlNode->NLLength++;
            nlNode->support -= ___SupportDict[nodeIndexI];
            //		cursor_i += 1;
            //YYY ??? Commneted
            //		cursor_j += 1;
        }
    }

    //    if(ni->label==3 && nj->label==2){
    //   
    //            cout << "\n1label-> " << ni->label << "\t";
    //        for (int ii = ni->NLStartinBf; ii < ni->NLStartinBf + ni->NLLength; ii++) {
    //            cout << "," << _buffer[ni->NLCol][ii];
    //        }
    //        cout << "\n1label-> " << nj->label << "\t";
    //        for (int jj = nj->NLStartinBf; jj < nj->NLStartinBf + nj->NLLength; jj++) {
    //            cout << "," << _buffer[nj->NLCol][jj];
    //        }
    //
    //        cout << "\n1debug-> ";
    //        for (int kk = nlNode->NLStartinBf; kk < nlNode->NLStartinBf + nlNode->NLLength; kk++) {
    //            cout << "," << _buffer[nlNode->NLCol][kk];
    //        }
    //    }
    //END YYY ???? inserted

    if (nlNode->support >= ___Min_Support) {

        if (ni->support == nlNode->support)
            ___sameItems[sameCount++] = nj->label;
        else {
            nlNode->label = nj->label;
            nlNode->firstChild = NULL;
            nlNode->next = NULL;
            if (ni->firstChild == NULL) {
                ni->firstChild = nlNode;
                lastChild = nlNode;
            } else {
                lastChild->next = nlNode;
                lastChild = nlNode;
            }
        }
        return lastChild;
    } else {
        ___bf_cursor = nlNode->NLStartinBf;
        delete nlNode;
    }
    return lastChild;


    //	int i = ni->label;
    //	int j = nj->label;
    //	if(ni->support == itemsetCount[(i-1) * i/2 + j])
    //		sameItems[sameCount++] = nj->label;
    //	else
    //	{
    //		NodeListTreeNode *nlNode = new NodeListTreeNode;
    //		nlNode->label = j;
    //		nlNode->NLCol = nlistCol;
    //		nlNode->NLStartinBf = nlistBegin[(i-1) * i/2 + j];
    //		nlNode->NLLength = nlistLen[(i-1) * i/2 + j];
    //		nlNode->support = itemsetCount[(i-1) * i/2 + j];
    //		nlNode->firstChild = NULL;
    //		nlNode->next = NULL;
    //		if(ni->firstChild == NULL)
    //		{
    //			ni->firstChild = nlNode;
    //			lastChild = nlNode;
    //		}
    //		else
    //		{
    //			lastChild->next = nlNode;
    //			lastChild = nlNode;
    //		}
    //	}
    //	return lastChild;
}

___NodeListTreeNode *___isk_itemSetFreq(___NodeListTreeNode* ni, ___NodeListTreeNode* nj, int level, ___NodeListTreeNode *lastChild, int &sameCount) {
    if (___bf_cursor + ni->NLLength > ___bf_currentSize) {
        ___bf_col++;
        ___bf_cursor = 0;
        ___bf_currentSize = ___bf_size > ni->NLLength * 1000 ? ___bf_size : ni->NLLength * 1000;
        ___buffer[___bf_col] = new int[___bf_currentSize];
    }

    ___NodeListTreeNode *nlNode = new ___NodeListTreeNode;
    nlNode->support = ni->support;
    nlNode->NLStartinBf = ___bf_cursor;
    nlNode->NLCol = ___bf_col;
    nlNode->NLLength = 0;

    //YYY ??? Commneted
    /*
    int cursor_i = ni->NLStartinBf;
    int cursor_j = nj->NLStartinBf;
    int col_i = ni->NLCol;
	
     */
    int col_j = nj->NLCol;

    //YYY ???? Commented
    /*
    while(cursor_i < ni->NLStartinBf + ni->NLLength && cursor_j < nj->NLStartinBf + nj->NLLength)
    {
            if(bf[col_i][cursor_i] == bf[col_j][cursor_j])
            {
                    bf[bf_col][bf_cursor++] =  bf[col_j][cursor_j];
                    nlNode->NLLength++;
                    nlNode->support += SupportDict[bf[col_i][cursor_i]];
                    cursor_i += 1;
                    cursor_j += 1;
            }
            else if(bf[col_i][cursor_i] < bf[col_j][cursor_j])
                    cursor_i += 1;
            else
                    cursor_j += 1;
    }
     */


    //YYY ???? inserted
    int nodeIndexJ;
    int endBf = nj->NLStartinBf + nj->NLLength;

    if (ni->NLLength == 0) {
        for (int cursor_j = nj->NLStartinBf; cursor_j < endBf; cursor_j++) {
            nodeIndexJ = ___buffer[col_j][cursor_j];
            ___buffer[___bf_col][___bf_cursor++] = nodeIndexJ;
            nlNode->NLLength++;
            nlNode->support -= ___SupportDict[nodeIndexJ];
            //		cursor_i += 1;
            //YYY ??? Commneted
            //		cursor_j += 1;
        }
    } else {
        __int128 maskForItemI = ___mask_for_item[ni->label];
        for (int cursor_j = nj->NLStartinBf; cursor_j < endBf; cursor_j++) {
            nodeIndexJ = ___buffer[col_j][cursor_j];
            if (___CodeDict[nodeIndexJ] & maskForItemI) {
                ___buffer[___bf_col][___bf_cursor++] = nodeIndexJ;
                nlNode->NLLength++;
                nlNode->support -= ___SupportDict[nodeIndexJ];
                //		cursor_i += 1;
                //YYY ??? Commneted
                //		cursor_j += 1;
            }
        }
    }

    //END YYY ???? inserted

    //    if (ni->label == 3 && nj->label == 2 && level == 2) {
    //
    //        cout << "\nlabel-> " << nj->label << "\t";
    //        for (int jj = nj->NLStartinBf; jj < nj->NLStartinBf + nj->NLLength; jj++) {
    //            cout << "," << _buffer[nj->NLCol][jj];
    //        }
    //        
    //        cout << "\nlabel-> " << ni->label << "\t";
    //        for (int ii = ni->NLStartinBf; ii < ni->NLStartinBf + ni->NLLength; ii++) {
    //            cout << "," << _buffer[ni->NLCol][ii];
    //        }
    //
    //        cout << "\ndebug-> ";
    //        for (int kk = nlNode->NLStartinBf; kk < nlNode->NLStartinBf + nlNode->NLLength; kk++) {
    //            cout << "," << _buffer[nlNode->NLCol][kk];
    //        }
    //    }
    //    cout << "\n================\n";

    if (nlNode->support >= ___Min_Support) {

        if (ni->support == nlNode->support)
            ___sameItems[sameCount++] = nj->label;
        else {
            nlNode->label = nj->label;
            nlNode->firstChild = NULL;
            nlNode->next = NULL;
            if (ni->firstChild == NULL) {
                ni->firstChild = nlNode;
                lastChild = nlNode;
            } else {
                lastChild->next = nlNode;
                lastChild = nlNode;
            }
        }
        return lastChild;
    } else {
        ___bf_cursor = nlNode->NLStartinBf;
        delete nlNode;
    }
    return lastChild;
}

void ___traverse(___NodeListTreeNode *curNode, ___NodeListTreeNode *curRoot, int level, int sameCount) {
    ___NodeListTreeNode *sibling = curNode->next;
    ___NodeListTreeNode *lastChild = NULL;
    while (sibling != NULL) {
        //YYY ??? Commented

        if (level == 1)
            lastChild = ___is2_itemSetValid(curNode, sibling, level, lastChild, sameCount);
        else if (level > 1)
            lastChild = ___isk_itemSetFreq(curNode, sibling, level, lastChild, sameCount);

        //End YYY ??? Commented

        //YYY ??? Inserted


        //End YYY ??? Inserted

        sibling = sibling->next;
    }

    ___resultCount += pow(2.0, sameCount);
    ___nlLenSum += ((double) curNode->NLLength * pow(2.0, sameCount));

    if (dump == 1) {
        ___result[___resultLen++] = curNode->label;
        for (int i = 0; i < ___resultLen; i++)
            fprintf(___out, "%d ", ___item[___result[i]].index);
        fprintf(___out, "(%d %d)", curNode->support, curNode->NLLength);
        for (int i = 0; i < sameCount; i++)
            fprintf(___out, " %d", ___item[___sameItems[i]].index);
        fprintf(___out, "\n");
    }
    ___nlNodeCount++;

    int from_cursor = ___bf_cursor;
    int from_col = ___bf_col;
    int from_size = ___bf_currentSize;
    ___NodeListTreeNode *child = curNode->firstChild;
    ___NodeListTreeNode *next = NULL;
    while (child != NULL) {
        next = child->next;
        ___traverse(child, curNode, level + 1, sameCount);
        for (int c = ___bf_col; c > from_col; c--) {
            delete[] ___buffer[c];
        }
        ___bf_col = from_col;
        ___bf_cursor = from_cursor;
        ___bf_currentSize = from_size;
        child = next;
    }
    if (dump == 1)
        ___resultLen--;
    delete curNode;
}

void ___deleteFPTree() {
    //XXX ??? Commented
    //        PPCTreeNode *root = ppcRoot.firstChild;
    //XXX ??? inserted
    ___PPCTreeNode *root = ___ppcRoot->firstChild;



    ___PPCTreeNode *next = NULL;
    while (root != NULL) {
        if (root->firstChild != NULL)
            root = root->firstChild;
        else {
            if (root->rightSibling != NULL) {
                next = root->rightSibling;
                delete root;
                root = next;
            } else {
                next = root->father;
                delete root;
                root = next;
                while (root != NULL) {
                    if (root->rightSibling != NULL) {
                        next = root->rightSibling;
                        delete root;
                        root = next;
                        break;
                    }
                    next = root->father;
                    delete root;
                    root = next;
                }
            }
        }
    }
}

void ___deleteNLTree(___NodeListTreeNode *root) {
    ___NodeListTreeNode *cur = root->firstChild;
    ;
    ___NodeListTreeNode *next = NULL;
    while (cur != NULL) {
        next = cur->next;
        ___deleteNLTree(cur);
        cur = next;
    }
    delete root;
}

void ___run(FILE *in, char* filename) {
    if (1 == dump) {
        ___out = fopen("sdp_negNodeSet.txt", "wt");
        ___result = new int[___numOfFItem];
        ___resultLen = 0;
    }
    ___buildTree(in, filename);
    ___deleteFPTree();

    ___nlRoot.label = ___numOfFItem;
    ___nlRoot.firstChild = NULL;
    ___nlRoot.next = NULL;

    ___initializeTree();
    ___sameItems = new int[___numOfFItem];

    int from_cursor = ___bf_cursor;
    int from_col = ___bf_col;
    int from_size = ___bf_currentSize;

    ___NodeListTreeNode *curNode = ___nlRoot.firstChild;
    ___NodeListTreeNode *next = NULL;
    while (curNode != NULL) {
        next = curNode->next;
        ___traverse(curNode, &___nlRoot, 1, 0);
        for (int c = ___bf_col; c > from_col; c--) {
            delete[] ___buffer[c];
        }
        ___bf_col = from_col;
        ___bf_cursor = from_cursor;
        ___bf_currentSize = from_size;
        curNode = next;
    }

    delete[] ___SupportDict;
    delete[] ___CodeDict;
    delete[] ___sameItems;
    //YYY ??? inserted
    delete[] ___mask_for_item;
    printf("-----%d %d %lf \n", ___nlNodeCount, ___resultCount, ___nlLenSum / ((double) ___resultCount));
    if (1 == dump)
        fclose(___out);
}

//========================================


void printMemoryUsage() {
    PROCESS_MEMORY_COUNTERS pmc;
    if (GetProcessMemoryInfo(GetCurrentProcess(), &pmc, sizeof(pmc))) {
        std::cout << "Working Set Size: " << pmc.WorkingSetSize / 1024 << " KB" << std::endl;
        std::cout << "Peak Working Set Size: " << pmc.PeakWorkingSetSize / 1024 << " KB" << std::endl;
        std::cout << "Pagefile Usage: " << pmc.PagefileUsage / 1024 << " KB" << std::endl;
    } else {
        std::cerr << "Failed to retrieve memory info." << std::endl;
    }
}

int printInfo(double elapsed, double threshold, char* filename) {
	
	PROCESS_MEMORY_COUNTERS pmc;
    if (!GetProcessMemoryInfo(GetCurrentProcess(), &pmc, sizeof(pmc))) {
        printf("Failed to retrieve memory info.");
        return 0;
    }


    // Extract the base name from the full path
    char *lastSlash = strrchr(filename, '\\'); // Find the last backslash (Windows path separator)
    if (lastSlash == nullptr) {
        lastSlash = filename; // If no backslash, use the whole filename
    } else {
        lastSlash++; // Move past the backslash
    }

    // Extract the base name (without extension) from filename
    char *dot = strrchr(lastSlash, '.'); // Find the last dot
    size_t baseLength = (dot != nullptr) ? (dot - lastSlash) : strlen(lastSlash);
    char base[256];
    strncpy(base, lastSlash, baseLength);
    base[baseLength] = '\0'; // Null-terminate the base name
    // Construct the output filename
    // Buffer to hold the dynamically constructed filename
    char outFilename[256];    
    sprintf(outFilename, "../output/%s_%.3lf_%s.json", base, threshold, "negFIN_Aryabarzan");

    // Open the file
    FILE *outFile = fopen(outFilename, "wt");
	// FILE *outFile;
    // outFile = fopen("output.json", "wt");

    fprintf(outFile, "{\n",elapsed);
	fprintf(outFile, "    \"algorithm\": \"negFIN\",\n");
	fprintf(outFile, "    \"language\": \"C++\",\n");
	fprintf(outFile, "    \"library\": \"Aryabarzan\",\n");
	fprintf(outFile, "    \"minSup\": %.3lf,\n",threshold);
	fprintf(outFile, "    \"totalFI\": %d,\n",___resultCount);
	fprintf(outFile, "    \"runtime\": %.3lf,\n",elapsed);
    fprintf(outFile, "    \"memory\": %d\n",pmc.PeakWorkingSetSize);
    fprintf(outFile, "}\n",elapsed);
    fclose(outFile);
    return 1;
}

int main(int argc, char **argv) {
    //cout << "usage: negnodeset.exe <datafile> <MINSUP>(0~1)  <number_of_transactions> <ISOUT>\n";
    /*
     * <number_of_transactions> is not used here and there is for compability with
     * fp_growth and eclat implentations.
     * */
    char *filename = argv[1];
    double THRESHOLD = atof(argv[2]);
    dump = atoi(argv[4]);


    //--------------------- NegNodeSet
    cout << endl<<"negFIN"<<endl<<"\t";
    ___nlNodeCount = 0;
    ___resultCount = 0;
    ___nlLenSum = 0;
    ___resultLen = 0;
    FILE *___in = NULL;
    ___bf_size = 1000000;
    ___buffer = new int*[100000];
    ___bf_currentSize = ___bf_size * 10;
    ___buffer[0] = new int[___bf_currentSize];

    ___bf_cursor = 0;
    ___bf_col = 0;

	// Start the clock
    clock_t start = clock();

    //Read Dataset
    ___getData(___in, filename, THRESHOLD);
    ___run(___in, filename);
    
    // End the clock
    clock_t end = clock();
    // Calculate elapsed time
    double elapsed = double(end - start) / CLOCKS_PER_SEC;
    
    printInfo(elapsed,THRESHOLD, filename);
    
    std::cout << "Processing time: " << elapsed << " seconds" << std::endl;
    printMemoryUsage();
    
    return 0;
}

