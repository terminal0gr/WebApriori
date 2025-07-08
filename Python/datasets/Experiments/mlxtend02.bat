@echo off

rem mushroom
call python mlxtendTest.py "mushroom.dat" "0.549483013" " " 
call python mlxtendTest.py "mushroom.dat" "0.364352535696701" " " 
call python mlxtendTest.py "mushroom.dat" "0.226489414" " " 

rem connect
call python mlxtendTest.py "connect.dat" "0.983510220998564" " " 
call python mlxtendTest.py "connect.dat" "0.960596237251506" " " 
call python mlxtendTest.py "connect.dat" "0.922702310641384" " " 

rem chess
call python mlxtendTest.py "chess.dat" "0.945244055068836" " " 
call python mlxtendTest.py "chess.dat" "0.886420525657071" " " 
call python mlxtendTest.py "chess.dat" "0.78973717146433" " " 

rem T16IT20D100K
call python mlxtendTest.py "T16IT20D100K.dat" "0.65513" " " 
call python mlxtendTest.py "T16IT20D100K.dat" "0.53743" " " 
call python mlxtendTest.py "T16IT20D100K.dat" "0.37865" " " 


pause