rem arguments:
rem 1 -> dataset name. Must be found in ../dataset file
rem 2 -> K parameter for the TopK frequent pattern mining
rem 3 -> item separation/delimiter in each dataset transaction
rem 4 -> Memory Save mode. If True, more efficient memory use but a little slower runtime
rem 5 -> runtimeThreshold in seconds (CommitTimeout)

rem kosarak
call python HTKnegFINTest.py "kosarak.dat" "100" " " "False" "1000"
call python HTKnegFINTest.py "kosarak.dat" "1000" " " "False" "1000"
call python HTKnegFINTest.py "kosarak.dat" "10000" " " "False" "1000"

rem retail
call python HTKnegFINTest.py "retail.dat" "100" " " "False" "1000"
call python HTKnegFINTest.py "retail.dat" "1000" " " "False" "1000"
call python HTKnegFINTest.py "retail.dat" "10000" " " "False" "1000"

rem L-0023
call python HTKnegFINTest.py "L-0023.csv" "100" ";" "False" "1000"
call python HTKnegFINTest.py "L-0023.csv" "1000" ";" "False" "1000"
call python HTKnegFINTest.py "L-0023.csv" "10000" ";" "False" "1000"

rem T10I4D100K
call python HTKnegFINTest.py "T10I4D100K.dat" "100" " " "False" "1000"
call python HTKnegFINTest.py "T10I4D100K.dat" "1000" " " "False" "1000"
call python HTKnegFINTest.py "T10I4D100K.dat" "10000" " " "False" "1000"

rem pumsb_star
call python HTKnegFINTest.py "pumsb_star.dat" "100" " " "False" "1000"
call python HTKnegFINTest.py "pumsb_star.dat" "1000" " " "False" "1000"
call python HTKnegFINTest.py "pumsb_star.dat" "10000" " " "False" "1000"

rem pumsb
call python HTKnegFINTest.py "pumsb.dat" "100" " " "False" "1000"
call python HTKnegFINTest.py "pumsb.dat" "1000" " " "False" "1000"
call python HTKnegFINTest.py "pumsb.dat" "10000" " " "False" "1000"

rem T40I10D100K
call python HTKnegFINTest.py "T40I10D100K.dat" "100" " " "False" "1000"
call python HTKnegFINTest.py "T40I10D100K.dat" "1000" " " "False" "1000"
call python HTKnegFINTest.py "T40I10D100K.dat" "10000" " " "False" "1000"

rem accidents
call python HTKnegFINTest.py "accidents.dat" "100" " " "False" "1000"
call python HTKnegFINTest.py "accidents.dat" "1000" " " "False" "1000"
call python HTKnegFINTest.py "accidents.dat" "10000" " " "False" "1000"

rem mushroom
call python HTKnegFINTest.py "mushroom.dat" "100" " " "False" "1000"
call python HTKnegFINTest.py "mushroom.dat" "1000" " " "False" "1000"
call python HTKnegFINTest.py "mushroom.dat" "10000" " " "False" "1000"

rem connect
call python HTKnegFINTest.py "connect.dat" "100" " " "False" "1000"
call python HTKnegFINTest.py "connect.dat" "1000" " " "False" "1000"
call python HTKnegFINTest.py "connect.dat" "10000" " " "False" "1000"

rem chess
call python HTKnegFINTest.py "chess.dat" "100" " " "False" "1000"
call python HTKnegFINTest.py "chess.dat" "1000" " " "False" "1000"
call python HTKnegFINTest.py "chess.dat" "10000" " " "False" "1000"

rem T16IT20D100K
call python HTKnegFINTest.py "T16IT20D100K.dat" "100" " " "False" "1000"
call python HTKnegFINTest.py "T16IT20D100K.dat" "1000" " " "False" "1000"
call python HTKnegFINTest.py "T16IT20D100K.dat" "10000" " " "False" "1000"

rem webdocs
call python HTKnegFINTest.py "webdocs.dat" "100" " " "False" "1000" "1000"
call python HTKnegFINTest.py "webdocs.dat" "1000" " " "False" "1000" "1000"
call python HTKnegFINTest.py "webdocs.dat" "1000" " " "False" "1000" "2000"

pause
pause
