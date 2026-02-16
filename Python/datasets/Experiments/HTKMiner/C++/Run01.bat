rem webdocs
call HTK-Miner_CL.exe "..\..\datasets\webdocs.dat" "0.327204591739643" "1" 
call negFIN.exe "..\..\datasets\webdocs.dat" "0.216111866918979" "1"
call negFIN.exe "..\..\datasets\webdocs.dat" "0.150844344423024" "1"

rem kosarak
call HTK-Miner_CL.exe "..\..\datasets\kosarak.dat" "100" "1"
call HTK-Miner_CL.exe "..\..\datasets\kosarak.dat" "1000" "1"
call HTK-Miner_CL.exe "..\..\datasets\kosarak.dat" "10000" "1"

rem retail
call negFIN.exe "..\..\datasets\retail.dat" "0.013531907170890" "1"
call negFIN.exe "..\..\datasets\retail.dat" "0.003641024" "1"
call negFIN.exe "..\..\datasets\retail.dat" "0.000816678" "1"

rem L-0023
rem call negFIN.exe "..\..\datasets\L-0023.csv" "0.0326177864510733" "1"
rem call negFIN.exe "..\..\datasets\L-0023.csv" "0.0122665179816002" "1"
rem call negFIN.exe "..\..\datasets\L-0023.csv" "0.00529690549205464" "1"

rem T10I4D100K
call negFIN.exe "..\..\datasets\T10I4D100K.dat" "0.02614" "1"
call negFIN.exe "..\..\datasets\T10I4D100K.dat" "0.00522" "1"
call negFIN.exe "..\..\datasets\T10I4D100K.dat" "0.00227" "1"

rem pumsb_star
call negFIN.exe "..\..\datasets\pumsb_star.dat" "0.631081026" "1"
call negFIN.exe "..\..\datasets\pumsb_star.dat" "0.479243975" "1"
call negFIN.exe "..\..\datasets\pumsb_star.dat" "0.424805284834645" "1"

rem pumsb
call negFIN.exe "..\..\datasets\pumsb.dat" "0.957713167" "1"
call negFIN.exe "..\..\datasets\pumsb.dat" "0.920299310851037" "1"
call negFIN.exe "..\..\datasets\pumsb.dat" "0.867879134" "1"

rem T40I10D100K
call negFIN.exe "..\..\datasets\T40I10D100K.dat" "0.09328" "1"
call negFIN.exe "..\..\datasets\T40I10D100K.dat" "0.02669" "1"
call negFIN.exe "..\..\datasets\T40I10D100K.dat" "0.01303" "1"

rem accidents
call negFIN.exe "..\..\datasets\accidents.dat" "0.819699985" "1"
call negFIN.exe "..\..\datasets\accidents.dat" "0.656411402" "1"
call negFIN.exe "..\..\datasets\accidents.dat" "0.482793085" "1"

rem mushroom
call negFIN.exe "..\..\datasets\mushroom.dat" "0.549483013" "1"
call negFIN.exe "..\..\datasets\mushroom.dat" "0.364352536" "1"
call negFIN.exe "..\..\datasets\mushroom.dat" "0.226489414" "1"

rem connect
call negFIN.exe "..\..\datasets\connect.dat" "0.983510221" "1"
call negFIN.exe "..\..\datasets\connect.dat" "0.960596237" "1"
call negFIN.exe "..\..\datasets\connect.dat" "0.922702311" "1"

rem chess
call negFIN.exe "..\..\datasets\chess.dat" "0.945244055068836" "1"
call negFIN.exe "..\..\datasets\chess.dat" "0.886107634543179" "1"
call negFIN.exe "..\..\datasets\chess.dat" "0.78973717146433" "1"

rem T16IT20D100K
call negFIN.exe "..\..\datasets\T16IT20D100K.dat" "0.65513" "1"
call negFIN.exe "..\..\datasets\T16IT20D100K.dat" "0.53743" "1"
call negFIN.exe "..\..\datasets\T16IT20D100K.dat" "0.37865" "1"

pause
pause