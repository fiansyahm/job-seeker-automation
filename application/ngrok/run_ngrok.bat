@echo off
set ngrok_path=%~dp0ngrok.exe
set http_port=8000

echo Menjalankan ngrok di port %http_port%...

start "" "%ngrok_path%" http %http_port%