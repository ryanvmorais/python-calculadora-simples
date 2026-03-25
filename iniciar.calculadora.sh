#!/bin/bash

# Limpa o terminal antes de iniciar
clear

echo "==========================================="
echo "   INICIANDO CALCULADORA EM PYTHON..."
echo "==========================================="

# Verifica se o comando python3 existe
if ! command -v python3 &> /dev/null
then
    echo "[ERRO] Python 3 não encontrado!"
    echo "Por favor, instale o Python via gerenciador de pacotes."
    exit
fi

echo "[OK] Python 3 detectado. Iniciando..."
python3 main.py
