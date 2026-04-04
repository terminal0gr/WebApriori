@echo off

echo ===================================================================
echo 100
powershell -command "$exe = 'fpgrowth.exe'; $args = '-s79.8902 ..\..\..\datasets\T80I100D1M.dat'; $timer = [System.Diagnostics.Stopwatch]::StartNew(); $process = Start-Process -FilePath $exe -ArgumentList $args -PassThru -NoNewWindow; $peakMem = 0; try { while (!$process.HasExited) { try { $currentMem = (Get-Process -Id $process.Id -ErrorAction Stop).PeakWorkingSet64 / 1MB; if ($currentMem -gt $peakMem) { $peakMem = $currentMem } } catch { break }; Start-Sleep -Milliseconds 100 } } finally { $timer.Stop() ; Write-Output '======= Performance Metrics ======='; Write-Output 'Peak Memory Usage (MB): '; $peakMem; Write-Output 'Execution Time: '; $($timer.Elapsed.ToString('hh\:mm\:ss\.fff'))"}"
echo 1000
powershell -command "$exe = 'fpgrowth.exe'; $args = '-s64.2858 ..\..\..\datasets\T80I100D1M.dat'; $timer = [System.Diagnostics.Stopwatch]::StartNew(); $process = Start-Process -FilePath $exe -ArgumentList $args -PassThru -NoNewWindow; $peakMem = 0; try { while (!$process.HasExited) { try { $currentMem = (Get-Process -Id $process.Id -ErrorAction Stop).PeakWorkingSet64 / 1MB; if ($currentMem -gt $peakMem) { $peakMem = $currentMem } } catch { break }; Start-Sleep -Milliseconds 100 } } finally { $timer.Stop() ; Write-Output '======= Performance Metrics ======='; Write-Output 'Peak Memory Usage (MB): '; $peakMem; Write-Output 'Execution Time: '; $($timer.Elapsed.ToString('hh\:mm\:ss\.fff'))"}"
echo 10000
powershell -command "$exe = 'fpgrowth.exe'; $args = '-s51.8797 ..\..\..\datasets\T80I100D1M.dat'; $timer = [System.Diagnostics.Stopwatch]::StartNew(); $process = Start-Process -FilePath $exe -ArgumentList $args -PassThru -NoNewWindow; $peakMem = 0; try { while (!$process.HasExited) { try { $currentMem = (Get-Process -Id $process.Id -ErrorAction Stop).PeakWorkingSet64 / 1MB; if ($currentMem -gt $peakMem) { $peakMem = $currentMem } } catch { break }; Start-Sleep -Milliseconds 100 } } finally { $timer.Stop() ; Write-Output '======= Performance Metrics ======='; Write-Output 'Peak Memory Usage (MB): '; $peakMem; Write-Output 'Execution Time: '; $($timer.Elapsed.ToString('hh\:mm\:ss\.fff'))"}"


echo/


rem fpgrowth.exe -s00.040885821803511  ..\..\..\datasets\TH1FIM.dat   output\result_FpGrowth_borgelt.fim

pause
pause
pause
