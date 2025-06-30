@echo off

echo ===================================================================
echo T10I4D100K.dat
echo 100
powershell -command "$exe = 'fpgrowth.exe'; $args = '-s02.614              ..\..\..\datasets\T10I4D100K.dat'; $timer = [System.Diagnostics.Stopwatch]::StartNew(); $process = Start-Process -FilePath $exe -ArgumentList $args -PassThru -NoNewWindow; $peakMem = 0; try { while (!$process.HasExited) { try { $currentMem = (Get-Process -Id $process.Id -ErrorAction Stop).PeakWorkingSet64 / 1MB; if ($currentMem -gt $peakMem) { $peakMem = $currentMem } } catch { break }; Start-Sleep -Milliseconds 100 } } finally { $timer.Stop() ; Write-Output '======= Performance Metrics ======='; Write-Output 'Peak Memory Usage (MB): '; $peakMem; Write-Output 'Execution Time: '; $($timer.Elapsed.ToString('hh\:mm\:ss\.fff'))"}"
echo 1000
powershell -command "$exe = 'fpgrowth.exe'; $args = '-s00.522              ..\..\..\datasets\T10I4D100K.dat'; $timer = [System.Diagnostics.Stopwatch]::StartNew(); $process = Start-Process -FilePath $exe -ArgumentList $args -PassThru -NoNewWindow; $peakMem = 0; try { while (!$process.HasExited) { try { $currentMem = (Get-Process -Id $process.Id -ErrorAction Stop).PeakWorkingSet64 / 1MB; if ($currentMem -gt $peakMem) { $peakMem = $currentMem } } catch { break }; Start-Sleep -Milliseconds 100 } } finally { $timer.Stop() ; Write-Output '======= Performance Metrics ======='; Write-Output 'Peak Memory Usage (MB): '; $peakMem; Write-Output 'Execution Time: '; $($timer.Elapsed.ToString('hh\:mm\:ss\.fff'))"}"
echo 10000
powershell -command "$exe = 'fpgrowth.exe'; $args = '-s00.227              ..\..\..\datasets\T10I4D100K.dat'; $timer = [System.Diagnostics.Stopwatch]::StartNew(); $process = Start-Process -FilePath $exe -ArgumentList $args -PassThru -NoNewWindow; $peakMem = 0; try { while (!$process.HasExited) { try { $currentMem = (Get-Process -Id $process.Id -ErrorAction Stop).PeakWorkingSet64 / 1MB; if ($currentMem -gt $peakMem) { $peakMem = $currentMem } } catch { break }; Start-Sleep -Milliseconds 100 } } finally { $timer.Stop() ; Write-Output '======= Performance Metrics ======='; Write-Output 'Peak Memory Usage (MB): '; $peakMem; Write-Output 'Execution Time: '; $($timer.Elapsed.ToString('hh\:mm\:ss\.fff'))"}"
echo/


rem fpgrowth.exe -s94.5244055068836  ..\..\..\datasets\chess.dat   output\chess_0.945244055068836_FpGrowth_borgelt.fim
rem fpgrowth.exe -s02.26928834487203 ..\..\..\datasets\kosarak.dat output\kosarak_0.0226928834487203_FpGrowth_borgelt.fim
rem fpgrowth.exe -s32.7204591739643  ..\..\..\datasets\webdocs.dat output\webdocs_0.327204591739643_FpGrowth_borgelt.fim


pause
