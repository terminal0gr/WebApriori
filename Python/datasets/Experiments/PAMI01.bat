@echo off

rem kosarak
call python PAMITest.py "kosarak.dat" "0.0226928834487203" " " False
call python PAMITest.py "kosarak.dat" "0.00634443162741085" " " False
call python PAMITest.py "kosarak.dat" "0.002392924" " " False

rem retail
call python PAMITest.py "retail.dat" "0.0135319071708899" " " False
call python PAMITest.py "retail.dat" "0.00364102447766611" " " False
call python PAMITest.py "retail.dat" "0.000816678387513894" " " False

rem L-0023
call python PAMITest.py "L-0023.csv" "0.0326177864510733" ";" False
call python PAMITest.py "L-0023.csv" "0.0122665179816002" ";" False
call python PAMITest.py "L-0023.csv" "0.00529690549205464" ";" False

rem T10I4D100K
call python PAMITest.py "T10I4D100K.dat" "0.02614" " " False
call python PAMITest.py "T10I4D100K.dat" "0.00522" " " False
call python PAMITest.py "T10I4D100K.dat" "0.00227" " " False

rem pumsb_star
call python PAMITest.py "pumsb_star.dat" "0.6310810259756148" " " False
call python PAMITest.py "pumsb_star.dat" "0.479243975" " " False
call python PAMITest.py "pumsb_star.dat" "0.424805284834645" " " False

rem pumsb
call python PAMITest.py "pumsb.dat" "0.957713167" " " False
call python PAMITest.py "pumsb.dat" "0.920299310851037" " " False
call python PAMITest.py "pumsb.dat" "0.867879133874322" " " False

rem T40I10D100K
call python PAMITest.py "T40I10D100K.dat" "0.09328" " " False
call python PAMITest.py "T40I10D100K.dat" "0.02693" " " False
call python PAMITest.py "T40I10D100K.dat" "0.01303" " " False

rem accidents
call python PAMITest.py "accidents.dat" "0.819699985" " " False
call python PAMITest.py "accidents.dat" "0.656411402" " " False
call python PAMITest.py "accidents.dat" "0.482793084898422" " " False

rem mushroom
call python PAMITest.py "mushroom.dat" "0.549483013" " " False
call python PAMITest.py "mushroom.dat" "0.364352535696701" " " False
call python PAMITest.py "mushroom.dat" "0.226489414" " " False

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

rem webdocs
call python PAMITest.py "webdocs.dat" "0.327204591739643" " " False 
call python PAMITest.py "webdocs.dat" "0.216111866918979" " " False
call python PAMITest.py "webdocs.dat" "0.150844344423024" " " False

pause