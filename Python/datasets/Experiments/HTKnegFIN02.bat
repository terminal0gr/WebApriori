echo off

rem arguments:
rem 1 -> dataset name. Must be found in ../dataset file
rem 2 -> K parameter for the TopK frequent pattern mining
rem 3 -> item separation/delimiter in each dataset transaction
rem 4 -> Memory Save mode. If True, more efficient memory use but a little slower runtime
rem 5 -> runtimeThreshold in seconds (CommitTimeout)

rem kosarak
call python TK_negFINTest.py "kosarak.dat" "1000" " " "False" "1000"
call python TK_negFINTest.py "kosarak.dat" "10000" " " "False" "1000"

rem retail
call python TK_negFINTest.py "retail.dat" "1000" " " "False" "1000"
call python TK_negFINTest.py "retail.dat" "10000" " " "False" "1000"

rem accidents
call python TK_negFINTest.py "accidents.dat" "1000" " " "False" "1000"
call python TK_negFINTest.py "accidents.dat" "10000" " " "False" "1000"

rem connect
call python TK_negFINTest.py "connect.dat" "1000" " " "False" "1000"
call python TK_negFINTest.py "connect.dat" "10000" " " "False" "1000"

rem pumsb
call python TK_negFINTest.py "pumsb.dat" "1000" " " "False" "1000"
call python TK_negFINTest.py "pumsb.dat" "10000" " " "False" "1000"

rem pumsb_star
call python TK_negFINTest.py "pumsb_star.dat" "1000" " " "False" "1000"
call python TK_negFINTest.py "pumsb_star.dat" "10000" " " "False" "1000"

rem T10I4D100K
call python TK_negFINTest.py "T10I4D100K.dat" "10000" " " "False" "1000"

rem T40I10D100K
call python TK_negFINTest.py "T40I10D100K.dat" "1000" " " "False" "1000"
call python TK_negFINTest.py "T40I10D100K.dat" "10000" " " "False" "1000"

rem L-0023
call python TK_negFINTest.py "L-0023.csv" "10000" ";" "False" "1000"

pause