@echo off

echo webdocs
call python EclatGoethalsTest.py "..\..\datasets\webdocs.dat" "0.327204591739643" " "  
call python EclatGoethalsTest.py "..\..\datasets\webdocs.dat" "0.216111866918979" " " 
call python EclatGoethalsTest.py "..\..\datasets\webdocs.dat" "0.150844344423024" " " 

echo TH2FIM
call python EclatGoethalsTest.py "..\..\datasets\TH2FIM.dat" "0.040876420392091" " "  
call python EclatGoethalsTest.py "..\..\datasets\TH2FIM.dat" "0.01379891680626" " " 
call python EclatGoethalsTest.py "..\..\datasets\TH2FIM.dat" "0.005116043936883" " " 

echo Susy
call python EclatGoethalsTest.py "..\..\datasets\Susy.txt" "0.8708096" " "  
call python EclatGoethalsTest.py "..\..\datasets\Susy.txt" "0.728718" " " 
call python EclatGoethalsTest.py "..\..\datasets\Susy.txt" "0.1515528" " " 

echo T80I100D1M
call python EclatGoethalsTest.py "..\..\datasets\T80I100D1M.txt" "0.798902" " "  
call python EclatGoethalsTest.py "..\..\datasets\T80I100D1M.txt" "0.642858" " " 
call python EclatGoethalsTest.py "..\..\datasets\T80I100D1M.txt" "0.518797" " " 

pause
παθσε