@echo off

echo ===================================================================
echo kosarak.dat
echo 100
call python pyfimMall.py -s02.26928834487203   ..\..\..\datasets\kosarak.dat
echo 1000
call python pyfimMall.py -s00.634443162741085  ..\..\..\datasets\kosarak.dat
echo 10000
call python pyfimMall.py -s00.2392924          ..\..\..\datasets\kosarak.dat
echo/

echo ===================================================================
echo retail.dat
echo 100
call python pyfimMall.py -s01.35319071708899   ..\..\..\datasets\retail.dat
echo 1000
call python pyfimMall.py -s00.364102447766611  ..\..\..\datasets\retail.dat
echo 10000
call python pyfimMall.py -s00.0816678387513894 ..\..\..\datasets\retail.dat
echo/

echo ===================================================================
echo L-0023.csv
echo 100
rem call python pyfimMall.py -s03.26177864510733  ..\..\..\datasets\L-0023.csv
echo 1000
rem call python pyfimMall.py -s01.22665179816002  ..\..\..\datasets\L-0023.csv
echo 10000
rem call python pyfimMall.py -s00.529690549205464 ..\..\..\datasets\L-0023.csv
echo/

echo ===================================================================
echo T10I4D100K.dat
echo 100
call python pyfimMall.py -s02.614              ..\..\..\datasets\T10I4D100K.dat
echo 1000
call python pyfimMall.py -s00.522              ..\..\..\datasets\T10I4D100K.dat
echo 10000
call python pyfimMall.py -s00.227              ..\..\..\datasets\T10I4D100K.dat
echo/

echo ===================================================================
echo pumsb_star.dat
echo 100
call python pyfimMall.py -s63.1081025975614    ..\..\..\datasets\pumsb_star.dat
echo 1000
call python pyfimMall.py -s47.9243975          ..\..\..\datasets\pumsb_star.dat
echo 10000
call python pyfimMall.py -s42.4805284834645    ..\..\..\datasets\pumsb_star.dat
echo/

echo ===================================================================
echo pumsb.dat
echo 100
call python pyfimMall.py -s95.7713167          ..\..\..\datasets\pumsb.dat
echo 1000
call python pyfimMall.py -s92.0299310851037    ..\..\..\datasets\pumsb.dat
echo 10000
call python pyfimMall.py -s86.7879133874322    ..\..\..\datasets\pumsb.dat
echo/

echo ===================================================================
echo T40I10D100K.dat
echo 100
call python pyfimMall.py -s09.328              ..\..\..\datasets\T40I10D100K.dat
echo 1000
call python pyfimMall.py -s02.693              ..\..\..\datasets\T40I10D100K.dat
echo 10000
call python pyfimMall.py -s01.303              ..\..\..\datasets\T40I10D100K.dat
echo/

echo ===================================================================
echo accidents.dat
echo 100
call python pyfimMall.py -s81.9699985          ..\..\..\datasets\accidents.dat
echo 1000
call python pyfimMall.py -s65.6411402          ..\..\..\datasets\accidents.dat
echo 10000
call python pyfimMall.py -s48.2793084898422    ..\..\..\datasets\accidents.dat
echo/

echo ===================================================================
echo mushroom.dat
echo 100
call python pyfimMall.py -s54.9483013          ..\..\..\datasets\mushroom.dat
echo 1000
call python pyfimMall.py -s36.43525356967012   ..\..\..\datasets\mushroom.dat
echo 10000
call python pyfimMall.py -s22.6489414          ..\..\..\datasets\mushroom.dat
echo/

echo ===================================================================
echo connect.dat
echo 100
call python pyfimMall.py -s98.3510220998564    ..\..\..\datasets\connect.dat
echo 1000
call python pyfimMall.py -s96.0596237251506    ..\..\..\datasets\connect.dat
echo 10000
call python pyfimMall.py -s92.2702310641384    ..\..\..\datasets\connect.dat
echo/

echo ===================================================================
echo chess.dat
echo 100
call python pyfimMall.py -s94.5244055068836    ..\..\..\datasets\chess.dat
echo 1000
call python pyfimMall.py -s88.6420525657071    ..\..\..\datasets\chess.dat
echo 10000
call python pyfimMall.py -s78.973717146433     ..\..\..\datasets\chess.dat
echo/

echo ===================================================================
echo T16IT20D100K.dat
echo 100
call python pyfimMall.py -s65.513              ..\..\..\datasets\T16IT20D100K.dat
echo 1000
call python pyfimMall.py -s53.743              ..\..\..\datasets\T16IT20D100K.dat
echo 10000
call python pyfimMall.py -s37.865              ..\..\..\datasets\T16IT20D100K.dat
echo/

echo ===================================================================
echo webdocs.dat
echo 1000
call python pyfimMall.py -s32.7204591739643    ..\..\..\datasets\webdocs.dat
echo 1000
call python pyfimMall.py -s21.6111866918979    ..\..\..\datasets\webdocs.dat
echo 10000
call python pyfimMall.py -s15.0844344423024    ..\..\..\datasets\webdocs.dat
echo/


pause