---
feature: Calculadora de terminal
status: concluído
date: 2026-09-11
related: []
origin: engenharia reversa
---

# 001 — Calculadora de terminal

## Contexto e problema

O repositório contém uma calculadora de terminal em Python, criada como
material de estudo (dicionários, loops, tratamento de erros) para quem está
iniciando na programação. O programa apresenta um menu numerado de operações
matemáticas, lê dois valores do usuário e imprime o resultado, repetindo até
o usuário optar por sair.

Esta spec documenta, por engenharia reversa, o comportamento real do
`main.py` após a modernização do projeto (adoção de `uv`, testes, correção de
bugs encontrados ao rodar o programa manualmente — ver `design.md`).

## Objetivos

- Oferecer um menu interativo com as cinco operações básicas
  (soma, subtração, multiplicação, divisão, exponenciação).
- Nunca encerrar abruptamente por entrada inválida do usuário.
- Funcionar corretamente em Windows, Linux e macOS, incluindo acentos e emoji
  no console do Windows.

## Não-objetivos

- Histórico de operações, novas funções matemáticas (%, raiz quadrada) ou
  feedback visual colorido — são sugeridas no README como exercícios para o
  leitor, não fazem parte do escopo atual.
- Interface gráfica ou modo não interativo (flags de linha de comando).

## Personas

- **Iniciante em Python**: usa o programa para praticar lógica e lê o
  código-fonte como material de estudo.

## Requisitos funcionais

### RF-01 — Exibir menu numerado de operações

- **Given** o programa foi iniciado
  **When** uma nova rodada do loop começa
  **Then** a tela é limpa e o menu é impresso com cada operação numerada a
  partir de 1, na ordem do dicionário `operacoes`.

### RF-02 — Validar o intervalo da escolha

- **Given** o menu está exibido com N operações
  **When** o usuário digita um número fora do intervalo `1..N`
  **Then** o programa exibe "⚠️ Opção inválida! Tente novamente." e volta ao
  início do loop, sem encerrar.
- **Given** o usuário digita um número dentro do intervalo `1..N`
  **When** a escolha é processada
  **Then** o programa segue para a operação correspondente.

### RF-03 — Realizar o cálculo

- **Given** uma operação válida foi escolhida e dois valores numéricos foram
  informados
  **When** `realizar_calculo(valor1, valor2, simbolo)` é chamada
  **Then** o resultado matemático correto é retornado como `float`, para os
  símbolos `+`, `-`, `*`, `/` e `^`.

### RF-04 — Tratar divisão por zero sem encerrar

- **Given** a operação escolhida é divisão (`/`)
  **When** o segundo valor informado é zero
  **Then** `realizar_calculo` levanta `ZeroDivisionError`, o loop principal
  captura a exceção, exibe "⚠️ Erro: Divisão por zero!" e permite continuar.

### RF-05 — Tratar entrada não numérica sem encerrar

- **Given** o programa pede um número (escolha do menu ou valor da operação)
  **When** o usuário digita algo que não converte para `int`/`float`
  **Then** o loop principal captura `ValueError`, exibe "⚠️ Erro: Por favor,
  digite apenas números." e permite continuar.

### RF-06 — Repetir ou sair

- **Given** uma operação foi concluída com sucesso
  **When** o programa pergunta se o usuário deseja continuar
  **Then** digitar `1` encerra o programa (com a mensagem de despedida);
  qualquer outra tecla reinicia o loop.

### RF-07 — Limpar a tela no comando correto do sistema operacional

- **Given** o programa está rodando no Windows
  **When** `limpar_tela()` é chamada
  **Then** o comando `cls` é executado (via `os.name == "nt"`).
- **Given** o programa está rodando em Linux/macOS
  **When** `limpar_tela()` é chamada
  **Then** o comando `clear` é executado.

### RF-08 — Exibir corretamente acentos e emoji no console do Windows

- **Given** o programa está rodando no console padrão do Windows (cp1252)
  **When** o programa imprime texto acentuado ou emoji (ex.: a mensagem de
  despedida "👋")
  **Then** a saída aparece corretamente, sem caracteres corrompidos nem
  `UnicodeEncodeError`.

## Requisitos não-funcionais

### RNF-01 — Sem dependências externas

O programa usa exclusivamente a biblioteca padrão do Python
(`os`, `sys`, `io`). Nenhum pacote de terceiros é necessário em runtime.

### RNF-02 — Portabilidade

O programa deve rodar sem alteração em Windows, Linux e macOS
(`requires-python >= 3.12`).

## Perguntas em aberto / decisões resolvidas

- **Decisão resolvida 1**: erros de cálculo (divisão por zero) são
  sinalizados por exceção (`ZeroDivisionError`), não por um valor de retorno
  do tipo `str`. Isso mantém `realizar_calculo` sempre retornando `float` e
  torna a função testável com `pytest.raises` — ver ADR-3 em `design.md`.

## Testes

- **RF-03 a RF-06** — cobertos por `tests/test_main.py`: um teste por
  operação aritmética, um teste para cada tipo de erro tratado (divisão por
  zero, entrada não numérica, opção fora do intervalo) e o fluxo feliz
  completo até a saída.
- **RF-01** — coberto por `test_exibir_menu_numera_a_partir_de_1`.
- **RF-07 e RF-08** não têm teste automatizado (dependem do console real do
  SO); foram verificados manualmente rodando `uv run main.py` no Windows
  durante a modernização — ver `design.md`.
