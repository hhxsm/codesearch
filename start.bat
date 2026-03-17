@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ==============================================
echo           大文件搜索工具 - 启动中
echo ==============================================
echo 请不要关闭本窗口！
echo.

echo 1. 启动 Elasticsearch...
start cmd /k "cd es\bin && elasticsearch.bat"
timeout /t 15 /nobreak >nul

echo 2. 启动搜索服务...
start cmd /k "python client_core.py"

echo 3. 启动网页服务...
start cmd /k "python web_my.py"

timeout /t 3 /nobreak >nul

echo 4. 打开网页...
start http://127.0.0.1:8088

echo.
echo ==============================
echo 启动完成！
echo 浏览器已打开
echo ==============================
pause