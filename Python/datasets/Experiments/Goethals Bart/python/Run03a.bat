@echo off

echo webdocs
rem call python EclatGoethalsTest.py "..\..\datasets\webdocs.dat" "0.327204591739643" " "  
rem call python EclatGoethalsTest.py "..\..\datasets\webdocs.dat" "0.216111866918979" " " 
rem call python EclatGoethalsTest.py "..\..\datasets\webdocs.dat" "0.150844344423024" " " 

echo 100
rem call python EclatGoethalsTest.py "..\..\datasets\TH2FIM.dat" "0.040876420392091" " "  
rem call python EclatGoethalsTest.py "..\..\datasets\Susy.txt" "0.8708096" " "  
rem call python EclatGoethalsTest.py "..\..\datasets\T80I100D1M.dat" "0.798902" " "  

echo 1000
rem call python EclatGoethalsTest.py "..\..\datasets\TH2FIM.dat" "0.01379891680626" " " 
rem call python EclatGoethalsTest.py "..\..\datasets\Susy.txt" "0.728718" " " 
rem call python EclatGoethalsTest.py "..\..\datasets\T80I100D1M.dat" "0.642858" " " 

echo 10000
rem call python EclatGoethalsTest.py "..\..\datasets\TH2FIM.dat" "0.005116043936883" " " 
call python EclatGoethalsTest.py "..\..\datasets\Susy.txt" "0.1515528" " " 
call python EclatGoethalsTest.py "..\..\datasets\T80I100D1M.dat" "0.518797" " " 

pause
pause