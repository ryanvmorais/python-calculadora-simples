---
feature: Calculadora de terminal
status: concluído
date: 2026-09-11
related: []
origin: engenharia reversa
---

# 001 — Calculadora de terminal — Tasks

## Etapa 0 — Estado original (antes da modernização)

- [x] `main.py`: menu numerado, dicionário `operacoes`, loop interativo com
  `try/except ValueError`. — RF-01, RF-02, RF-05, RF-06
- [x] `requirements.txt`, `iniciar_calculadora.bat`, `iniciar.calculadora.sh`,
  `README.md`, `CONTRIBUTING.md`, `LICENSE` já existentes (projeto sem
  gerenciador de dependências, sem testes, sem CI).

## Etapa 1 — Modernização (uv, correções, testes)

- [x] `pyproject.toml`: manifesto PEP 621 gerenciado por `uv`, sem
  dependências de runtime, grupo `dev` com ruff/black/mypy/pytest,
  `[tool.uv] package = false`. — RNF-01
- [x] `uv sync`: gera `.venv` e `uv.lock`; remove `requirements.txt`. — RNF-01
- [x] `main.py`: corrige `limpar_tela()` para usar `os.name == "nt"` em vez
  de `platform.system() == "nt"` (sempre falso). — RF-07, ADR-1
- [x] `main.py`: troca `subprocess.run(comando, shell=True)` por
  `os.system(comando)`. — ADR-4
- [x] `main.py`: adiciona `sys.stdout.reconfigure(encoding="utf-8")` guardado
  por `isinstance(..., io.TextIOWrapper)` no início de `calculadora()`,
  corrigindo mojibake de acentos e `UnicodeEncodeError` no emoji de saída no
  console do Windows. — RF-08, ADR-2
- [x] `main.py`: `realizar_calculo` passa a levantar `ZeroDivisionError` em
  vez de retornar uma `str` de erro; `calculadora()` ganha
  `except ZeroDivisionError`. — RF-03, RF-04, ADR-3
- [x] `main.py`: type hints completos, docstrings no formato
  `/estilo-arquivos`, réguas de seção, `from __future__ import annotations`.
- [x] `iniciar_calculadora.bat` / `iniciar.calculadora.sh`: trocam a checagem
  de `python`/`python3` por checagem de `uv` e passam a rodar
  `uv run main.py`.
- [x] `tests/test_main.py`: suíte cobrindo `realizar_calculo` (uma por
  operação + exceções), `exibir_menu`, e o loop `calculadora()` (fluxo feliz,
  divisão por zero, entrada não numérica, opção inválida). — RF-01, RF-03,
  RF-04, RF-05, RF-06
- [x] `pyproject.toml`: `pythonpath = ["."]` em `[tool.pytest.ini_options]`
  para permitir `import main` sem empacotar o projeto. — ADR-5
- [x] Portão de qualidade. — `ruff check --fix .` sem achados; `black .` sem
  mudanças; `mypy main.py tests` sem erros; `pytest` com 12 passed.

## Etapa 2 — Documentação e distribuição

- [x] `specs/001-calculadora-simples/`: `requirements.md`, `design.md` e
  `tasks.md` por engenharia reversa, cobrindo o comportamento real e as
  correções da Etapa 1.
- [x] `specs/README.md`: convenções + índice.
- [x] `docs/stack.md`: mapa da stack (linguagem/runtime + ferramentas de dev).
- [x] `.github/dependabot.yml`: bump semanal de `uv` (diretório `/`) e
  `github-actions`.
- [x] `.github/workflows/ci.yml`: job único espelhando o portão de qualidade,
  matriz Python 3.13/3.14.
- [x] `CLAUDE.md`: visão geral, comandos, arquitetura, convenções, qualidade,
  spec-driven development, dependências.
- [x] `README.md` / `CONTRIBUTING.md`: atualizar comandos de instalação
  (`pip` → `uv`), tabela de tecnologias e seção de testes/qualidade.
- [x] Portão final (clone limpo mental): `rm -rf .venv uv.lock && uv sync` do
  zero seguido da sequência `ruff → black → mypy → pytest` — todos verdes.
