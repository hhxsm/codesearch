@echo off
taskkill /f /im python.exe >nul 2>&1
taskkill /f /im java.exe >nul 2>&1
taskkill /f /im elasticsearch.exe >nul 2>&1
taskkill /f /im cmd.exe >nul 2>&1
echo 已停止所有服务
pause