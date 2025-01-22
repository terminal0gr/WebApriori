rem T10I4D100K
java -Xms1g -Xmx12g -cp "bin;lib/*" ca.pfv.spmf.Mall.SPMF_Apriori_TopK T10I4D100K.dat 100
java -Xms1g -Xmx12g -cp "bin;lib/*" ca.pfv.spmf.Mall.SPMF_Apriori_TopK T10I4D100K.dat 1000
java -Xms1g -Xmx12g -cp "bin;lib/*" ca.pfv.spmf.Mall.SPMF_Apriori_TopK T10I4D100K.dat 10000

pause