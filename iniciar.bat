@echo off
cd /d %~dp0
set PY=
python --version >nul 2>nul && set PY=python
if not defined PY py --version >nul 2>nul && set PY=py
if not defined PY (
  echo Python nao encontrado. Instale em python.org e marque "Add python.exe to PATH".
  pause
  exit /b
)
%PY% -c "import flask" >nul 2>nul || %PY% -m pip install flask
echo Abra http://127.0.0.1:5000 no navegador
%PY% app.py
pause