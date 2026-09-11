@echo off
title Calculadora Simples em Python
cls

echo ===========================================
echo   VERIFICANDO AMBIENTE (uv)...
echo ===========================================

uv --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRO] uv nao encontrado!
    echo Instale em: https://docs.astral.sh/uv/getting-started/installation/
    pause
    exit
)

echo [OK] uv detectado. Abrindo calculadora...
uv run main.py
pause
