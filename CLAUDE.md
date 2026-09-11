Este arquivo orienta o Claude Code (claude.ai/code) ao trabalhar neste repositório.

## Visão geral do projeto

Calculadora de terminal em Python, criada como material de estudo educacional
(dicionários, loops, tratamento de erros). Um único arquivo de produção
(`main.py`), sem dependências de runtime — só biblioteca padrão. Gerenciado
com `uv`.

## Comandos comuns

```bash
# Instalar dependências de desenvolvimento e criar o .venv
uv sync

# Rodar a calculadora
uv run main.py

# Portão de qualidade completo, nesta ordem
uv run ruff check --fix .   # lint + organiza imports (altera arquivos)
uv run black .               # formatação (altera arquivos)
uv run mypy main.py tests    # checagem de tipos (só reporta)
uv run pytest                # testes

# Rodar um único teste
uv run pytest tests/test_main.py::test_realizar_calculo_divisao_por_zero_levanta_erro
```

## Arquitetura

```
main.py                       # único módulo de produção
  limpar_tela()                # detecta o SO (os.name) e roda cls/clear
  exibir_menu(lista_nomes)     # imprime o menu numerado
  operacoes                    # dict símbolo -> nome; fonte única de verdade
  realizar_calculo(...)        # motor de cálculo puro; levanta exceção no erro
  calculadora()                # loop principal (I/O, validação, replay/saída)
tests/test_main.py             # suíte pytest (ver "Qualidade e automação")
pyproject.toml                 # manifesto uv (deps de dev, ruff/black/mypy/pytest)
uv.lock                        # lockfile — commitado
docs/stack.md                  # mapa da stack: o que é, por que, o que estudar
specs/001-calculadora-simples/ # spec por engenharia reversa do comportamento atual
iniciar_calculadora.bat        # atalho Windows (uv run main.py)
iniciar.calculadora.sh         # atalho Linux/macOS (uv run main.py)
```

`operacoes` é a peça central: menu e motor de cálculo leem do mesmo
dicionário, então adicionar uma operação nova (ex.: `%`, `√` — sugerido como
exercício no README) não exige tocar em mais nenhum lugar além de
`realizar_calculo`.

> ⚠️ NÃO regredir: `limpar_tela()` precisa continuar usando `os.name == "nt"`,
> não `platform.system()`. `platform.system()` retorna `"Windows"`, nunca
> `"nt"` — usar a função errada faz a checagem sempre falhar silenciosamente
> (o programa "funciona", só não limpa a tela no Windows). Ver ADR-1 em
> `specs/001-calculadora-simples/design.md`.

> Cuidado: o console padrão do Windows abre `stdout` em `cp1252`. Sem o
> `sys.stdout.reconfigure(encoding="utf-8")` no início de `calculadora()`,
> acentos saem corrompidos e o emoji da mensagem de saída derruba o programa
> com `UnicodeEncodeError`. Ver ADR-2 em `specs/001-calculadora-simples/design.md`.

## Convenções

Idioma do código: português (projeto educacional PT-BR) — ver `/idioma`.
Formatação, docstrings, type hints e comentários seguem `/estilo-arquivos`
(seções `.py`, `.toml`, `.yaml`, `.md`); não repetido aqui.

## Qualidade e automação

Sequência: `ruff check --fix` → `black` → `mypy` → `pytest` (skill
`/qualidade-python`). CI (`.github/workflows/ci.yml`) roda a mesma sequência
em Python 3.13 e 3.14 a cada push/PR. Sem hooks locais configurados.

Estratégia de teste de `calculadora()` (loop interativo): `limpar_tela` é
sempre mockada via `monkeypatch` (evita `os.system` real); `builtins.input` é
substituído por um gerador que devolve respostas simuladas na ordem em que o
loop as consome; saída verificada via `capsys`. Ver a docstring de
`tests/test_main.py` para o detalhamento.

## Spec-driven development

Specs em `specs/NNN-nome/` (`requirements.md` + `design.md` + `tasks.md`,
frontmatter idêntico nos três). Ver `specs/README.md` para convenções e
índice completo. `specs/001-calculadora-simples/` documenta por engenharia
reversa o comportamento atual e os ADRs das correções feitas na
modernização — é a spec-ouro de formato para as próximas.

Ao fim de uma sessão que mudou comportamento ou documentação: `/atualizar-docs`
e depois `/fechar-sessao`.

## Gestão de dependências

`uv` gerencia tudo — commite `pyproject.toml` **e** `uv.lock`. O projeto não
tem dependências de runtime (`dependencies = []`); só o grupo `dev`
(ruff, black, mypy, pytest). `[tool.uv] package = false`: é um script, não
uma biblioteca instalável — não crie `src/` nem um `[build-system]` para ele.
Dependabot (`.github/dependabot.yml`) abre PRs semanais de atualização; revise
com a skill `/revisar-dependabot`.
