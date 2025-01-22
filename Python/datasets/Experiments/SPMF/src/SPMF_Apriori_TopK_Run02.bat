rem webdocs
java -Xms1g -Xmx12g -cp "bin;lib/*" ca.pfv.spmf.Mall.SPMF_Apriori_TopK webdocs.dat 100
java -Xms1g -Xmx12g -cp "bin;lib/*" ca.pfv.spmf.Mall.SPMF_Apriori_TopK webdocs.dat 1000
java -Xms1g -Xmx12g -cp "bin;lib/*" ca.pfv.spmf.Mall.SPMF_Apriori_TopK webdocs.dat 10000

pause