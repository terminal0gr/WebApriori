@echo off

rem call python PAMITest.py "chess.dat" "0.945244055068836"  " " False
rem call python PAMITest.py "chess.dat" "0.8864205256570713" " " False
rem call python PAMITest.py "chess.dat" "0.7897371714643304" " " False
rem call python PAMITest.py "kosarak.dat" "0.002392924458738467" " " False

rem L-0023
call python PAMITest.py "L-0023.csv" "0.0326177864510733" ";" False
call python PAMITest.py "L-0023.csv" "0.0122665179816002" ";" False
call python PAMITest.py "L-0023.csv" "0.00529690549205464" ";" False

pause