@echo off

rem kosarak
::call python mlxtendTest.py "kosarak.dat" "0.0226928834487203" " " 
::call python mlxtendTest.py "kosarak.dat" "0.00634443162741085" " " 
::call python mlxtendTest.py "kosarak.dat" "0.002392924" " " 

::echo retail
::call python mlxtendTest.py "retail.dat" "0.0135319071708899" " " 
::call python mlxtendTest.py "retail.dat" "0.00364102447766611" " " 
::call python mlxtendTest.py "retail.dat" "0.000816678387513894" " " 

::rem L-0023
::call python mlxtendTest.py "L-0023.csv" "0.0326177864510733" ";" 
::call python mlxtendTest.py "L-0023.csv" "0.0122665179816002" ";" 
::call python mlxtendTest.py "L-0023.csv" "0.00529690549205464" ";" 

echo T10I4D100K
call python mlxtendTest.py "T10I4D100K.dat" "0.02614" " " 
call python mlxtendTest.py "T10I4D100K.dat" "0.00522" " " 
call python mlxtendTest.py "T10I4D100K.dat" "0.00227" " " 

echo pumsb_star
call python mlxtendTest.py "pumsb_star.dat" "0.6310810259756148" " " 
call python mlxtendTest.py "pumsb_star.dat" "0.479243975" " " 
call python mlxtendTest.py "pumsb_star.dat" "0.424805284834645" " " 

echo pumsb
call python mlxtendTest.py "pumsb.dat" "0.957713167" " " 
call python mlxtendTest.py "pumsb.dat" "0.920299310851037" " " 
call python mlxtendTest.py "pumsb.dat" "0.867879133874322" " " 

echo T40I10D100K
call python mlxtendTest.py "T40I10D100K.dat" "0.09328" " " 
call python mlxtendTest.py "T40I10D100K.dat" "0.02693" " " 
call python mlxtendTest.py "T40I10D100K.dat" "0.01303" " " 

echo accidents
call python mlxtendTest.py "accidents.dat" "0.819699985" " " 
call python mlxtendTest.py "accidents.dat" "0.656411402" " " 
call python mlxtendTest.py "accidents.dat" "0.482793084898422" " " 

echo mushroom
call python mlxtendTest.py "mushroom.dat" "0.549483013" " " 
call python mlxtendTest.py "mushroom.dat" "0.364352535696701" " " 
call python mlxtendTest.py "mushroom.dat" "0.226489414" " " 

echo connect
call python mlxtendTest.py "connect.dat" "0.983510220998564" " " 
call python mlxtendTest.py "connect.dat" "0.960596237251506" " " 
call python mlxtendTest.py "connect.dat" "0.922702310641384" " " 

echo chess
call python mlxtendTest.py "chess.dat" "0.945244055068836" " " 
call python mlxtendTest.py "chess.dat" "0.886420525657071" " " 
call python mlxtendTest.py "chess.dat" "0.78973717146433" " " 

echo T16IT20D100K
call python mlxtendTest.py "T16IT20D100K.dat" "0.65513" " " 
call python mlxtendTest.py "T16IT20D100K.dat" "0.53743" " " 
call python mlxtendTest.py "T16IT20D100K.dat" "0.37865" " " 

echo webdocs
call python mlxtendTest.py "webdocs.dat" "0.327204591739643" " "  
call python mlxtendTest.py "webdocs.dat" "0.216111866918979" " " 
call python mlxtendTest.py "webdocs.dat" "0.150844344423024" " " 


pause
pause