
set LOGFILE=BTK03.log

type nul > %LOGFILE%

rem mushroom
powershell -Command "python BTK_Test.py 'mushroom.dat' '31' ' ' '300' | tee -Append '%LOGFILE%'"
call python BTK_Test.py "mushroom.dat" "164" " " "300" >> %LOGFILE% 2>&1

echo All commands executed. Results are stored in %LOGFILE%.

pause