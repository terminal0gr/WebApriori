@echo off
:: Run fpgrowth.exe and measure peak memory usage (error-proof)
powershell -command "$exe = 'fpgrowth.exe'; $args = '-s94.5244055068836  ..\..\..\datasets\chess.dat   output\chess_0.945244055068836_FpGrowth_borgelt.fim'; $process = Start-Process -FilePath $exe -ArgumentList $args -PassThru -NoNewWindow; $peakMem = 0; try { while (!$process.HasExited) { try { $currentMem = (Get-Process -Id $process.Id -ErrorAction Stop).PeakWorkingSet64 / 1MB ; if ($currentMem -gt $peakMem) { $peakMem = $currentMem } } catch { break }; Start-Sleep -Milliseconds 1 } } finally { Write-Output 'Peak Memory (MB):'; $peakMem }"
powershell -command "$exe = 'fpgrowth.exe'; $args = '-s02.26928834487203 ..\..\..\datasets\kosarak.dat output\kosarak_0.0226928834487203_FpGrowth_borgelt.fim'; $process = Start-Process -FilePath $exe -ArgumentList $args -PassThru -NoNewWindow; $peakMem = 0; try { while (!$process.HasExited) { try { $currentMem = (Get-Process -Id $process.Id -ErrorAction Stop).PeakWorkingSet64 / 1MB ; if ($currentMem -gt $peakMem) { $peakMem = $currentMem } } catch { break }; Start-Sleep -Milliseconds 100 } } finally { Write-Output 'Peak Memory (MB):'; $peakMem }"
powershell -command "$exe = 'fpgrowth.exe'; $args = '-s00.2392924         ..\..\..\datasets\kosarak.dat'; $process = Start-Process -FilePath $exe -ArgumentList $args -PassThru -NoNewWindow; $peakMem = 0; try { while (!$process.HasExited) { try { $currentMem = (Get-Process -Id $process.Id -ErrorAction Stop).PeakWorkingSet64 / 1MB ; if ($currentMem -gt $peakMem) { $peakMem = $currentMem } } catch { break }; Start-Sleep -Milliseconds 100 } } finally { Write-Output 'Peak Memory (MB):'; $peakMem }"

rem fpgrowth.exe -s94.5244055068836  ..\..\..\datasets\chess.dat   output\chess_0.945244055068836_FpGrowth_borgelt.fim
rem fpgrowth.exe -s02.26928834487203 ..\..\..\datasets\kosarak.dat output\kosarak_0.0226928834487203_FpGrowth_borgelt.fim
rem fpgrowth.exe -s32.7204591739643  ..\..\..\datasets\webdocs.dat output\webdocs_0.327204591739643_FpGrowth_borgelt.fim


pause
