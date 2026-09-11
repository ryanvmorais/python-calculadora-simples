---
feature: Calculadora de terminal
status: concluído
date: 2026-09-11
related: []
origin: engenharia reversa
---

# 001 — Calculadora de terminal — design

## Visão geral da abordagem

Programa de arquivo único (`main.py`), sem estado persistente entre execuções.
Um dicionário (`operacoes`) mapeia símbolo → nome legível e serve de única
fonte de verdade tanto para o menu quanto para o motor de cálculo — adicionar
uma operação nova não exige tocar em mais nenhum lugar do código (é, aliás,
uma das atividades sugeridas no README para o leitor praticar).

## Layout de módulos / componentes

- `main.py` — único módulo de produção.
- `tests/test_main.py` — suíte de testes (adicionada na modernização).
- `pyproject.toml` / `uv.lock` — configuração de projeto e dependências de
  desenvolvimento (adicionados na modernização).

## Modelo de dados

- `operacoes: dict[str, str]` — símbolo (`"+"`, `"-"`, `"*"`, `"/"`, `"^"`) →
  nome da operação em português. Convertido em duas listas paralelas
  (`lista_simbolos`, `lista_nomes`) dentro de `calculadora()` para permitir
  acesso por índice numérico (o menu é 1-based; o índice de lista é 0-based).

## Componentes

### `limpar_tela()`

Detecta o SO via `os.name` (`"nt"` no Windows) e executa `cls` ou `clear` via
`os.system`.

### `exibir_menu(lista_nomes)`

Imprime o cabeçalho e a lista numerada de operações.

### `realizar_calculo(num1, num2, simbolo)`

Motor de cálculo puro — sem I/O. Recebe os dois operandos e o símbolo,
devolve o resultado como `float`. Levanta `ZeroDivisionError` (divisão por
zero) ou `ValueError` (símbolo desconhecido) em vez de retornar um valor
sentinela — ver ADR-3.

### `calculadora()`

Loop principal: limpa a tela, exibe o menu, lê e valida a escolha, lê os dois
operandos, chama `realizar_calculo`, imprime o resultado, e pergunta se o
usuário quer continuar. Reconfigura `sys.stdout` para UTF-8 uma vez, no
início — ver ADR-2.

## Interfaces

Nenhuma — programa de terminal, sem API externa, sem I/O de arquivo/rede.

## ADRs

### ADR-1 — Detectar o Windows via `os.name`, não `platform.system()`

**Decisão.** `limpar_tela()` usa `os.name == "nt"` para decidir entre `cls` e
`clear`.

**Alternativas.** (a) manter `platform.system() == "nt"`, como estava
originalmente.

**Porquê.** `platform.system()` retorna `"Windows"`, `"Linux"` ou `"Darwin"`
— nunca `"nt"`. A comparação original era sempre falsa, então o programa
sempre executava `clear` no Windows, que silenciosamente não limpa nada no
`cmd.exe`/PowerShell padrão. `os.name` é o identificador correto para essa
comparação (é literalmente `"nt"` no Windows). Bug encontrado rodando o
programa manualmente durante a modernização, não coberto por teste algum
antes.

**Trade-off.** Nenhum — é a correção da checagem para o identificador certo,
sem mudança de comportamento pretendido.

### ADR-2 — Recodificar `sys.stdout` para UTF-8 no início de `calculadora()`

**Decisão.** `calculadora()` chama
`sys.stdout.reconfigure(encoding="utf-8")` logo no início, protegida por um
`isinstance(sys.stdout, io.TextIOWrapper)` (mypy trata `sys.stdout` como
`TextIO`, que não expõe `reconfigure` — o guard também evita a chamada
quando stdout foi substituído por outra coisa, como o `capsys` do pytest).

**Alternativas.** (a) não mexer e aceitar mojibake/crash; (b) rodar
`chcp 65001` externamente antes de iniciar o Python; (c) usar
`PYTHONUTF8=1` como variável de ambiente documentada no README.

**Porquê.** O console padrão do Windows abre `stdout` em `cp1252`. Rodando o
programa original manualmente: acentos apareciam corrompidos
(`Divis?o`) e a mensagem final com emoji (`👋`) derrubava o programa com
`UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f44b'`.
`sys.stdout.reconfigure` corrige na origem, sem depender de o usuário
configurar nada fora do programa — essencial num programa educacional cujo
público não deve precisar mexer em `codepage` do Windows.

**Trade-off.** Só funciona quando `stdout` já é um `TextIOWrapper` real (é o
caso do console interativo, que é o alvo); em ambientes já redirecionados o
guard simplesmente pula a chamada — comportamento seguro no pior caso.

### ADR-3 — `realizar_calculo` levanta exceção em vez de retornar `str` de erro

**Decisão.** Divisão por zero levanta `ZeroDivisionError`; símbolo
desconhecido levanta `ValueError`. `realizar_calculo` sempre retorna `float`.

**Alternativas.** (a) manter o retorno original,
`"Erro: Divisão por zero!"` (uma `str` misturada com o `float` normal); (b)
retornar `float("nan")`.

**Porquê.** O retorno misto (`float | str`) obrigava quem chama a testar o
tipo do resultado antes de usá-lo, e permitia formatar um "erro" como se
fosse um número em qualquer chamador futuro que esquecesse a checagem.
Levantar a exceção padrão da própria operação (`ZeroDivisionError` é o que
`num1 / num2` já levantaria naturalmente) mantém a assinatura de tipo
simples (`-> float`) e torna o caso de erro testável diretamente com
`pytest.raises`, sem precisar inspecionar string.

**Trade-off.** O chamador (`calculadora()`) precisa de um bloco
`except ZeroDivisionError` a mais — trivial, e já existia um padrão
`except ValueError` para a mesma finalidade.

### ADR-4 — `os.system`, não `subprocess.run(..., shell=True)`

**Decisão.** `limpar_tela()` usa `os.system(comando)`.

**Alternativas.** manter `subprocess.run(comando, shell=True)`, como estava.

**Porquê.** Para um comando fixo e sem entrada do usuário (`"cls"` ou
`"clear"`), `os.system` faz exatamente o mesmo com menos código e sem
carregar a API mais pesada do `subprocess` (pensada para capturar
saída/erro, controlar pipes, etc. — nada disso é usado aqui).

**Trade-off.** `os.system` também passa pelo shell, então a ressalva de
segurança é a mesma de antes; como o comando é uma constante do próprio
código (nunca vem do usuário), não há risco de injeção em nenhum dos dois.

### ADR-5 — `pythonpath = ["."]` no `pytest` em vez de empacotar o projeto

**Decisão.** `tests/test_main.py` importa `main` diretamente; `pyproject.toml`
declara `pythonpath = ["."]` em `[tool.pytest.ini_options]`.

**Alternativas.** (a) mover `main.py` para dentro de um pacote (`src/` ou
similar) e instalar o projeto; (b) `sys.path.insert` manual num
`conftest.py`.

**Porquê.** O projeto é um script de arquivo único, não uma biblioteca —
`[tool.uv] package = false` já reflete isso. Criar uma estrutura de pacote só
para permitir `import main` seria desproporcional ao tamanho real do
projeto. A opção nativa do pytest (`pythonpath`) resolve o import sem exigir
instalação nem manipulação manual de `sys.path`.

**Trade-off.** Nenhum relevante neste tamanho de projeto.

## Impacto no código existente

Todas as mudanças acima tocam só `main.py` (mesma API pública: `limpar_tela`,
`exibir_menu`, `operacoes`, `realizar_calculo`, `calculadora`). Nenhuma
quebra de compatibilidade externa — não há nenhuma, o programa não é
importado por nada fora dele mesmo.

## Estratégia de testes

Testes de unidade puros com `pytest`:

- `realizar_calculo`: um teste por operação + um por tipo de exceção — sem
  mocks, é uma função pura.
- `exibir_menu`: verificado via `capsys`.
- `calculadora`: `limpar_tela` é sempre mockada (`monkeypatch.setattr`) para
  não depender de um console real; `builtins.input` é mockado com um gerador
  que devolve as respostas simuladas na ordem em que o loop as consome;
  saída verificada via `capsys`. `sys.stdout.reconfigure` não precisa de mock
  — o guard de tipo do ADR-2 já o torna inofensivo sob `capsys`.
