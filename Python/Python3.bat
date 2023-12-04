set _Tmp=
:Loop
if not '%1==' (
  set _Tmp=%_Tmp% %1
  shift
  if not '%1==' goto Loop
)
python %_Tmp%
