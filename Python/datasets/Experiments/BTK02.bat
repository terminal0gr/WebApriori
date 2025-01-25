rem T40I10D100K
call python BTK_Test.py "T40I10D100K.dat" "865" " " "1000"
call python BTK_Test.py "T40I10D100K.dat" "2117" " " "1000"

rem T16IT20D100K
call python BTK_Test.py "T16IT20D100K.dat" "1581" " " "1000"

rem L-0023
call python TK_negFINTest.py "L-0023.csv" "10000" ";" "False" "1000"

pause