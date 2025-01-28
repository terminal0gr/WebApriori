rem retail
java -Xms1g -Xmx12g -cp "bin;lib/*" ca.pfv.spmf.Mall.SPMF_Apriori_TopK retail.dat 1000

rem accidents
java -Xms1g -Xmx12g -cp "bin;lib/*" ca.pfv.spmf.Mall.SPMF_Apriori_TopK accidents.dat 1000

rem pumsb
java -Xms1g -Xmx12g -cp "bin;lib/*" ca.pfv.spmf.Mall.SPMF_Apriori_TopK pumsb.dat 1000

rem pumsb_star
java -Xms1g -Xmx12g -cp "bin;lib/*" ca.pfv.spmf.Mall.SPMF_Apriori_TopK pumsb_star.dat 1000
java -Xms1g -Xmx12g -cp "bin;lib/*" ca.pfv.spmf.Mall.SPMF_Apriori_TopK pumsb_star.dat 10000

rem T10I4D100K
java -Xms1g -Xmx12g -cp "bin;lib/*" ca.pfv.spmf.Mall.SPMF_Apriori_TopK T10I4D100K.dat 10000

rem T40I10D100K
java -Xms1g -Xmx12g -cp "bin;lib/*" ca.pfv.spmf.Mall.SPMF_Apriori_TopK T40I10D100K.dat 1000
java -Xms1g -Xmx12g -cp "bin;lib/*" ca.pfv.spmf.Mall.SPMF_Apriori_TopK T40I10D100K.dat 10000

pause