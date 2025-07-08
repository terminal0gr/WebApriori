@echo off

rem connect
call python PAMITest.py "connect.dat" "0.983510220998564" " " False
call python PAMITest.py "connect.dat" "0.960596237251506" " " False
call python PAMITest.py "connect.dat" "0.922702310641384" " " False

rem chess
call python PAMITest.py "chess.dat" "0.945244055068836" " " False
call python PAMITest.py "chess.dat" "0.886420525657071" " " False
call python PAMITest.py "chess.dat" "0.78973717146433" " " False

rem T16IT20D100K
call python PAMITest.py "T16IT20D100K.dat" "0.65513" " " False
call python PAMITest.py "T16IT20D100K.dat" "0.53743" " " False
call python PAMITest.py "T16IT20D100K.dat" "0.37865" " " False

pause