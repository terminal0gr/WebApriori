
set LOGFILE=BTK02.log

type nul > %LOGFILE%

rem mushroom
powershell -Command "python BTK_Test.py 'mushroom.dat' '31' ' ' '300' | tee -Append '%LOGFILE%'"
powershell -Command "python BTK_Test.py 'mushroom.dat' '164' ' ' '300' | tee -Append '%LOGFILE%'"
powershell -Command "python BTK_Test.py 'mushroom.dat' '368' ' ' '300' | tee -Append '%LOGFILE%'"

rem pumsb
powershell -Command "python BTK_Test.py 'pumsb.dat' '64' ' ' '300' | tee -Append '%LOGFILE%'"
powershell -Command "python BTK_Test.py 'pumsb.dat' '511' ' ' '300' | tee -Append '%LOGFILE%'"
powershell -Command "python BTK_Test.py 'pumsb.dat' '2444' ' ' '300' | tee -Append '%LOGFILE%'"

rem pumsb_star
powershell -Command "python BTK_Test.py 'pumsb_star.dat' '49' ' ' '300' | tee -Append '%LOGFILE%'"
powershell -Command "python BTK_Test.py 'pumsb_star.dat' '356' ' ' '300' | tee -Append '%LOGFILE%'"
powershell -Command "python BTK_Test.py 'pumsb_star.dat' '1286' ' ' '300' | tee -Append '%LOGFILE%'"

rem retail
powershell -Command "python BTK_Test.py 'retail.dat' '98' ' ' '300' | tee -Append '%LOGFILE%'"
powershell -Command "python BTK_Test.py 'retail.dat' '509' ' ' '300' | tee -Append '%LOGFILE%'"
powershell -Command "python BTK_Test.py 'retail.dat' '758' ' ' '300' | tee -Append '%LOGFILE%'"

rem T10I4D100K
powershell -Command "python BTK_Test.py 'T10I4D100K.dat' '98' ' ' '300' | tee -Append '%LOGFILE%'"
powershell -Command "python BTK_Test.py 'T10I4D100K.dat' '660' ' ' '300' | tee -Append '%LOGFILE%'"
powershell -Command "python BTK_Test.py 'T10I4D100K.dat' '953' ' ' '300' | tee -Append '%LOGFILE%'"

rem T16IT20D100K
powershell -Command "python BTK_Test.py 'T16IT20D100K.dat' '71' ' ' '300' | tee -Append '%LOGFILE%'"
powershell -Command "python BTK_Test.py 'T16IT20D100K.dat' '247' ' ' '300' | tee -Append '%LOGFILE%'"
powershell -Command "python BTK_Test.py 'T16IT20D100K.dat' '556' ' ' '300' | tee -Append '%LOGFILE%'"

rem T40I10D100K
powershell -Command "python BTK_Test.py 'T16IT20D100K.dat' '97' ' ' '300' | tee -Append '%LOGFILE%'"
powershell -Command "python BTK_Test.py 'T16IT20D100K.dat' '865' ' ' '300' | tee -Append '%LOGFILE%'"
powershell -Command "python BTK_Test.py 'T16IT20D100K.dat' '2117' ' ' '300' | tee -Append '%LOGFILE%'"

rem L-0023.csv
powershell -Command "python BTK_Test.py 'L-0023.csv' '69' ';' '300' | tee -Append '%LOGFILE%'"
powershell -Command "python BTK_Test.py 'L-0023.csv' '143' ';' '300' | tee -Append '%LOGFILE%'"
powershell -Command "python BTK_Test.py 'L-0023.csv' '168' ';' '300' | tee -Append '%LOGFILE%'"

pause