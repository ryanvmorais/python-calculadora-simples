@echo off
title Calculadora Simples em Python
cls

echo ===========================================
echo   VERIFICANDO AMBIENTE PYTHON...
echo ===========================================

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRO] Python não encontrado! 
    echo Por favor, instale o Python em: https://python.org
    pause
    exit
)

echo [OK] Python detectado. Abrindo calculadora...
python main.py
pause
