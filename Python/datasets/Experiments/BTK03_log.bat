
set LOGFILE=BTK02.log

type nul > %LOGFILE%

rem T10I4D100K
powershell -Command "python BTK_Test.py 'T10I4D100K.dat' '98' ' ' '300' | tee -Append '%LOGFILE%'"
powershell -Command "python BTK_Test.py 'T10I4D100K.dat' '660' ' ' '300' | tee -Append '%LOGFILE%'"
powershell -Command "python BTK_Test.py 'T10I4D100K.dat' '953' ' ' '300' | tee -Append '%LOGFILE%'"

rem T40I10D100K
powershell -Command "python BTK_Test.py 'T40I10D100K.dat' '97' ' ' '300' | tee -Append '%LOGFILE%'"
powershell -Command "python BTK_Test.py 'T40I10D100K.dat' '865' ' ' '300' | tee -Append '%LOGFILE%'"
powershell -Command "python BTK_Test.py 'T40I10D100K.dat' '2117' ' ' '300' | tee -Append '%LOGFILE%'"

rem L-0023.csv
powershell -Command "python BTK_Test.py 'L-0023.csv' '69' ';' '300' | tee -Append '%LOGFILE%'"
powershell -Command "python BTK_Test.py 'L-0023.csv' '143' ';' '300' | tee -Append '%LOGFILE%'"
powershell -Command "python BTK_Test.py 'L-0023.csv' '168' ';' '300' | tee -Append '%LOGFILE%'"


rem T16IT20D100K
powershell -Command "python BTK_Test.py 'T16IT20D100K.dat' '91' ' ' '300' | tee -Append '%LOGFILE%'"
powershell -Command "python BTK_Test.py 'T16IT20D100K.dat' '523' ' ' '300' | tee -Append '%LOGFILE%'"
powershell -Command "python BTK_Test.py 'T16IT20D100K.dat' '1581' ' ' '300' | tee -Append '%LOGFILE%'"

pause