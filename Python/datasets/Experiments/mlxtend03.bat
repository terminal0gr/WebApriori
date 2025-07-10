@echo off

::$before = Get-Process -Name "python" | Measure-Object WorkingSet -Sum
::call python mlxtendTest.py "T40I10D100K.dat" "0.09328" " " 
::$after = Get-Process -Name "python" | Measure-Object WorkingSet -Sum
::$memUsed = ($after.Sum - $before.Sum) / 1MB
::Write-Output "Approximate memory used: $memUsed MB"

set PYCOMMAND=python mlxtendTest.py "T10I4D100K.dat" "0.02614" " "

powershell -Command ^
    "$before = Get-Process -Name python -ErrorAction SilentlyContinue | Measure-Object WorkingSet -Sum; ^
    Start-Process -NoNewWindow -FilePath python -ArgumentList 'mlxtendTest.py', 'T10I4D100K.dat', '0.02614', ' ' -Wait; ^
    Start-Sleep -Seconds 1; ^
    $after = Get-Process -Name python -ErrorAction SilentlyContinue | Measure-Object WorkingSet -Sum; ^
    if ($after.Count -eq 0) { Write-Host 'Python process not found. Script may have finished too quickly.' } ^
    else { $memUsed = ($after.Sum - $before.Sum) / 1MB; Write-Host ('Approximate memory used: {0:N2} MB' -f $memUsed) }"