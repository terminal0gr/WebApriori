rem arguments:
rem 1 -> dataset name. Must be found in ../dataset file
rem 2 -> K parameter for the TopK frequent pattern mining
rem 3 -> item separation/delimiter in each dataset transaction
rem 4 -> Memory Save mode. If True, more efficient memory use but a little slower runtime
rem 5 -> runtimeThreshold in seconds (CommitTimeout)

rem kosarak
rem call python HTKnegFINTest.py "kosarak.dat" "100" " " "False" "1000"
rem call python HTKnegFINTest.py "kosarak.dat" "1000" " " "False" "1000"

rem L-0023
rem call python HTKnegFINTest.py "L-0023.csv" "100" ";" "False" "1000"
rem call python HTKnegFINTest.py "L-0023.csv" "1000" ";" "False" "1000"
rem not!!! call python HTKnegFINTest.py "L-0023.csv" "10000" ";" "False" "1000"

rem call python HTKnegFINTest.py "accidents.dat" "100" " " "False" "1000"
rem call python HTKnegFINTest.py "connect.dat" "100" " " "False" "1000"
rem call python HTKnegFINTest.py "T16IT20D100K.dat" "100" " " "False" "1000"
rem call python HTKnegFINTest.py "T16IT20D100K.dat" "1000" " " "False" "1000"
rem call python HTKnegFINTest.py "T16IT20D100K.dat" "10000" " " "False" "1000"

call python HTKnegFINTest.py "accidents.dat" "1000" " " "False" "1000"
call python HTKnegFINTest.py "connect.dat" "1000" " " "False" "1000"

pause
pause
