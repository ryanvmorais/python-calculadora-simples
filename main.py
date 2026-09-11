"""
Calculadora de terminal — exercício educacional de lógica, dicionários e
tratamento de erros.

ESTRUTURA DO CÓDIGO:
1. CONFIGURAÇÃO E INTERFACE: Funções para limpeza de tela e gerenciamento do
   terminal.
2. MAPEAMENTO DE DADOS: Onde as operações matemáticas são estruturadas.
3. LÓGICA DE PROCESSAMENTO: O motor de cálculo que valida e executa as
   operações.
4. LOOP PRINCIPAL (CORE): O controle do fluxo de uso e opção de saída.
"""

from __future__ import annotations

import io
import os
import sys

# --- Funcoes de Configuracao e Interface ---


def limpar_tela() -> None:
    """Detecta o SO e executa o comando correto de limpeza do terminal."""
    # 'nt' é o identificador interno do Windows em os.name (platform.system()
    # retorna "Windows", não "nt" — usar a função errada nunca limpava a tela)
    comando = "cls" if os.name == "nt" else "clear"
    os.system(comando)


def exibir_menu(lista_nomes: list[str]) -> None:
    """Percorre a lista de operações e gera o menu numerado para o usuário.

    Args:
        lista_nomes (list[str]): Nomes das operações, na ordem de exibição.
    """
    print("======== CALCULADORA SIMPLIFICADA ========")
    for indice, nome in enumerate(lista_nomes, start=1):
        print(f"{indice} : {nome}")


# --- Mapeamento de Dados ---

# Dicionário que serve como 'banco de dados' das operações disponíveis
operacoes = {
    "+": "Soma",
    "-": "Subtração",
    "*": "Multiplicação",
    "/": "Divisão",
    "^": "Exponenciação",
}

# --- Lógica de Processamento e Cálculos ---


def realizar_calculo(num1: float, num2: float, simbolo: str) -> float:
    """Recebe os valores e o símbolo para processar a conta matemática.

    Args:
        num1 (float): Primeiro operando.
        num2 (float): Segundo operando.
        simbolo (str): Símbolo da operação, uma chave de ``operacoes``.

    Returns:
        float: Resultado da operação.

    Raises:
        ZeroDivisionError: Se ``simbolo`` for ``"/"`` e ``num2`` for zero.
        ValueError: Se ``simbolo`` não for uma chave conhecida.
    """
    if simbolo == "+":
        return num1 + num2
    elif simbolo == "-":
        return num1 - num2
    elif simbolo == "*":
        return num1 * num2
    elif simbolo == "/":
        return num1 / num2
    elif simbolo == "^":
        return float(num1**num2)
    raise ValueError(f"Símbolo de operação desconhecido: {simbolo!r}")


# --- Loop Principal (Core) ---


def calculadora() -> None:
    """Executa o loop interativo da calculadora até o usuário optar por sair."""
    # Recodifica stdout para UTF-8: o console do Windows abre em cp1252 por
    # padrão, o que corrompe acentos e quebra a impressão de emoji. O guard de
    # tipo evita reconfigure() em stdout redirecionado para algo que não seja
    # um TextIOWrapper real (ex.: capsys do pytest).
    if isinstance(sys.stdout, io.TextIOWrapper):
        sys.stdout.reconfigure(encoding="utf-8")

    # Transformamos as chaves e valores em listas para facilitar o acesso via índice
    lista_simbolos = list(operacoes.keys())
    lista_nomes = list(operacoes.values())

    while True:
        limpar_tela()
        exibir_menu(lista_nomes)

        try:
            print("\nEscolha a operação que deseja realizar:")
            escolha = int(input(f"Digite o número (1-{len(lista_simbolos)}): ")) - 1

            # Validação do intervalo da escolha
            if escolha < 0 or escolha >= len(lista_simbolos):
                print("⚠️ Opção inválida! Tente novamente.")
                input("Pressione Enter...")
                continue

            simbolo_atual = lista_simbolos[escolha]
            nome_da_op = lista_nomes[escolha]

            print(f"\nOperação escolhida: {nome_da_op}")

            valor1 = float(input("Digite o primeiro valor: "))
            valor2 = float(input("Digite o segundo valor: "))

            # Processa o cálculo chamando a função lógica
            resultado = realizar_calculo(valor1, valor2, simbolo_atual)

            print(f"\nRESULTADO: {valor1} {simbolo_atual} {valor2} = {resultado}")
            print("==========================================")

        except ZeroDivisionError:
            print("⚠️ Erro: Divisão por zero!")
            input("Pressione Enter para continuar...")
            continue
        except ValueError:
            print("⚠️ Erro: Por favor, digite apenas números.")
            input("Pressione Enter para continuar...")
            continue

        # Opção de Replay / Sair
        print("\nDeseja realizar outra operação?")
        print("(Digite 1 para SAIR ou qualquer outra tecla para CONTINUAR)")

        comando_saida = input("Sua escolha: ")
        if comando_saida == "1":
            print("\nCalculadora encerrada. Até logo! 👋")
            break


if __name__ == "__main__":
    calculadora()
