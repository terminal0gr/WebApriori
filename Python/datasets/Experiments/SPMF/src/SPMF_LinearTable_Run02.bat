
rem chess
rem java -Xms1g -Xmx12g -cp "bin;lib/*" ca.pfv.spmf.Mall.SPMF_LinearTable "chess.dat" "0.8864205256570713"

echo %TIME:~0,5%
java -Xms12g -Xmx12g -cp "bin;lib/*" ca.pfv.spmf.Mall.SPMF_LinearTable "TH2FIM.dat" "0.040876420392091"
echo %TIME:~0,5%
java -Xms12g -Xmx12g -cp "bin;lib/*" ca.pfv.spmf.Mall.SPMF_LinearTable "T80I100D1M.dat" "0.798902"

echo %TIME:~0,5%
java -Xms12g -Xmx12g -cp "bin;lib/*" ca.pfv.spmf.Mall.SPMF_LinearTable "TH2FIM.dat" "0.01379891680626"
echo %TIME:~0,5%
java -Xms12g -Xmx12g -cp "bin;lib/*" ca.pfv.spmf.Mall.SPMF_LinearTable "T80I100D1M.dat" "0.642858"

echo %TIME:~0,5%
java -Xms12g -Xmx12g -cp "bin;lib/*" ca.pfv.spmf.Mall.SPMF_LinearTable "TH2FIM.dat" "0.005116043936883"
echo %TIME:~0,5%
java -Xms12g -Xmx12g -cp "bin;lib/*" ca.pfv.spmf.Mall.SPMF_LinearTable "T80I100D1M.dat" "0.518797"


pause

pause