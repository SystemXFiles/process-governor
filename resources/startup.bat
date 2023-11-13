@echo off
set "exe_path=%~1"
set "working_directory=%~dp1"
cd /d "%working_directory%"
start /B "" "%exe_path%"
exit