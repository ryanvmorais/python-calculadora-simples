"""
🧮 PROJETO: CALCULADORA SIMPLIFICADA
🎯 Objetivo: Educacional - Prática de Lógica, Dicionários e Tratamento de Erros.

ESTRUTURA DO CÓDIGO:
1. CONFIGURAÇÃO E INTERFACE: Funções para limpeza de tela e gerenciamento do terminal.
2. MAPEAMENTO DE DADOS: Onde as operações matemáticas são estruturadas.
3. LÓGICA DE PROCESSAMENTO: O motor de cálculo que valida e executa as operações.
4. LOOP PRINCIPAL (CORE): O controle do fluxo de uso e opção de saída.
"""

import subprocess
import platform

# --- Funções de Configuração e Interface ---

def limpar_tela():
    """ Detecta o SO e executa o comando correto de limpeza do terminal. """
     # 'nt' é o identificador interno para Windows
    comando = "cls" if platform.system() == "nt" else "clear"
    subprocess.run(comando, shell=True)

def exibir_menu(lista_nomes):
    """ Percorre a lista de operações e gera o menu numerado para o usuário. """
    print('======== CALCULADORA SIMPLIFICADA ========')
    for indice, nome in enumerate(lista_nomes, start=1):
        print(f'{indice} : {nome}')

# --- Mapeamento de Dados ---

# Dicionário que serve como 'banco de dados' das operações disponíveis
operacoes = {
    '+': 'Soma',
    '-': 'Subtração',
    '*': 'Multiplicação',
    '/': 'Divisão',
    '^': 'Exponenciação'
}

# --- Lógica de Processamento e Cálculos ---

def realizar_calculo(num1, num2, simbolo):
    """ Recebe os valores e o símbolo para processar a conta matemática. """
    if simbolo == '+':
        return num1 + num2
    elif simbolo == '-':
        return num1 - num2
    elif simbolo == '*':
        return num1 * num2
    elif simbolo == '/':
        if num2 == 0:
            return "Erro: Divisão por zero!"
        return num1 / num2
    elif simbolo == '^':
        return num1 ** num2
    return None

# --- Loop Principal (Core) ---

def calculadora():
    # Transformamos as chaves e valores em listas para facilitar o acesso via índice
    lista_simbolos = list(operacoes.keys())
    lista_nomes = list(operacoes.values())

    while True:
        limpar_tela()
        exibir_menu(lista_nomes)
        
        try:
            print('\nEscolha a operação que deseja realizar:')
            escolha = int(input("Digite o número (1-5): ")) - 1
            
            # Validação do intervalo da escolha
            if escolha < 0 or escolha >= len(lista_simbolos):
                print("⚠️ Opção inválida! Tente novamente.")
                input("Pressione Enter...")
                continue

            simbolo_atual = lista_simbolos[escolha]
            nome_da_op = lista_nomes[escolha]

            print(f'\nOperação escolhida: {nome_da_op}')
            
            valor1 = float(input('Digite o primeiro valor: '))
            valor2 = float(input('Digite o segundo valor: '))

            # Processa o cálculo chamando a função lógica
            resultado = realizar_calculo(valor1, valor2, simbolo_atual)

            print(f'\nRESULTADO: {valor1} {simbolo_atual} {valor2} = {resultado}')
            print('==========================================')

        except ValueError:
            print("⚠️ Erro: Por favor, digite apenas números.")
            input("Pressione Enter para continuar...")
            continue

        # Opção de Replay / Sair
        print('\nDeseja realizar outra operação?')
        print('(Digite 1 para SAIR ou qualquer outra tecla para CONTINUAR)')
        
        comando_saida = input("Sua escolha: ")
        if comando_saida == '1':
            print("\nCalculadora encerrada. Até logo! 👋")
            break

if __name__ == '__main__':
    calculadora()




