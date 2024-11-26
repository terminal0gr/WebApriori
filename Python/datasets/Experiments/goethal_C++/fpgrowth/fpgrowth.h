/*----------------------------------------------------------------------
  File    : fpgrowth.h
  Contents: fpgrowth algorithm for finding frequent sets
  Author  : Bart Goethals
  Update  : 4/4/2003
  ----------------------------------------------------------------------*/

class FPgrowth
{
 private:

  unsigned minsup;
  double minsup0_1;
  Data *data;
  FPtree *fpt;
	
  FILE *out;

 public:

  FPgrowth();
  ~FPgrowth();

  void setData(char *file, int type){
    data = new Data(file,type);
  }
  void setMinsup(unsigned ms){minsup = ms;}
  //Malliaridis 26/11/2024 min Support in 0-1 (e.g. 0.1)
  void setMinsup0_1(double msp){minsup0_1 = msp;}
  
  void setOutput(char *of);
  int mine();

};
