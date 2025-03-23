
rem 1_L-0023
call python HTKMiner_Test.py "L-0023.csv" "100" ";" False False
call python HTKMiner_Test.py "L-0023.csv" "100" ";" "False" "True"
call python HTKMiner_Test.py "L-0023.csv" "100" ";" "True" "False"
call python HTKMiner_Test.py "L-0023.csv" "100" ";" "True" "True"
call python HTKMiner_Test.py "L-0023.csv" "1000" ";" "False" "False"
call python HTKMiner_Test.py "L-0023.csv" "1000" ";" "False" "True"
call python HTKMiner_Test.py "L-0023.csv" "1000" ";" "True" "False"
call python HTKMiner_Test.py "L-0023.csv" "1000" ";" "True" "True"
call python HTKMiner_Test.py "L-0023.csv" "10000" ";" False False
call python HTKMiner_Test.py "L-0023.csv" "10000" ";" "False" "True"
call python HTKMiner_Test.py "L-0023.csv" "10000" ";" "True" "False"
call python HTKMiner_Test.py "L-0023.csv" "10000" ";" "True" "True"

pause
pause