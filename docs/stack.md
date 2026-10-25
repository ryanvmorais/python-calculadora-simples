# Stack

Mapa de cada tecnologia que sustenta este projeto: o que faz, por que foi
escolhida em vez da alternativa mais óbvia, e o que estudar primeiro para
mexer nela com confiança. Não é exaustivo — o grafo de dependências completo
está no `uv.lock`; o porquê de cada decisão não óbvia está detalhado nos
`### ADR-N` de [`specs/001-calculadora-simples/design.md`](../specs/001-calculadora-simples/design.md).

O projeto é um único script de terminal (`main.py`) sem dependências de
runtime — tudo abaixo, fora o próprio Python, é ferramental de desenvolvimento
(lint, formatação, tipos, testes), que roda só na sua máquina e no CI, nunca
junto do programa quando alguém executa `uv run main.py`.

## Linguagem e runtime

### Python

O que é/faz: linguagem em que o projeto inteiro é escrito. A calculadora usa
só a biblioteca padrão (`os`, `sys`, `io`) — nenhum pacote externo é
necessário para rodar o programa.

Por que esta: é a linguagem do exercício desde a concepção do repositório —
o objetivo educacional é praticar dicionários, loops e tratamento de erros em
Python, não comparar linguagens.

O que estudar:
- Dicionários e a conversão `dict.keys()`/`dict.values()` em listas.
- `try/except` com múltiplos tipos de exceção.
- `f-strings` e `input()`/`print()`.
- Type hints modernos (`list[str]`, `X | None`) e `from __future__ import annotations`.

Docs: https://docs.python.org/3/

## Gerenciador de dependências

### uv

O que é/faz: gerenciador de projetos Python — cria e mantém o ambiente
virtual (`.venv`), resolve e fixa versões (`uv.lock`), e roda comandos dentro
do ambiente certo sem precisar ativá-lo manualmente (`uv run`).

Por que esta: substitui `pip` + `venv` manuais (o que o projeto usava antes,
via `requirements.txt`) por um fluxo único, rápido e reprodutível — o mesmo
padrão já adotado nos outros projetos Python do Ryan (site-ryan-morais,
webvigil).

O que estudar:
- `uv sync` (instala exatamente o que está no lock) vs `uv lock` (recalcula o lock).
- `uv run <comando>` — roda dentro do `.venv` sem ativá-lo.
- `[dependency-groups] dev` — dependências que não fazem parte do programa
  distribuído, só do fluxo de desenvolvimento.
- `[tool.uv] package = false` — por que este projeto é tratado como script,
  não como biblioteca instalável.

Docs: https://docs.astral.sh/uv/

## Ferramental de qualidade (dev)

### ruff

O que é/faz: lint e organização de imports num binário só (substitui
flake8 + isort + várias outras ferramentas de uma vez).

Por que esta: é o linter Python mais rápido hoje e já é o padrão nos outros
projetos do Ryan — mesma regra (`select = ["E", "F", "I", "UP", "B", "SIM", "C4", "RUF"]`)
que webvigil e site-ryan-morais usam.

O que estudar:
- `uv run ruff check --fix .` — como o autofix decide o que mudar sozinho.
- O significado dos códigos de regra (`E`/`F` = pycodestyle/pyflakes, `I` =
  isort, `UP` = pyupgrade, `B` = bugbear, `SIM` = simplify).

Docs: https://docs.astral.sh/ruff/

### black

O que é/faz: formatador de código — decide indentação, aspas, quebras de
linha, sem opção de configuração além do `line-length`.

Por que esta: é o formatador Python de-facto (não há o que discutir sobre
estilo — o black decide, e todo mundo segue), e a "briga zero" é o ponto:
nunca se reformata manualmente contra ele.

O que estudar:
- `uv run black .` — não tenta entender a saída, só confie nela.
- `target-version` — por que este projeto trava em `py312` (o piso de
  `requires-python`), mesmo rodando localmente em Python 3.14.

Docs: https://black.readthedocs.io/

### mypy

O que é/faz: checador de tipos estático — lê as anotações (`-> float`,
`list[str]`, etc.) e aponta inconsistências antes de rodar o programa.

Por que esta: é o type checker de referência do ecossistema Python (o próprio
CPython e o typeshed são mantidos em conjunto com ele); `strict = true` pega
o máximo de erro possível num projeto pequeno onde isso não pesa no fluxo.

O que estudar:
- A diferença entre um erro de tipo real e um "o mypy não consegue provar" —
  ex.: o guard `isinstance(sys.stdout, io.TextIOWrapper)` em `main.py` existe
  porque `reconfigure()` não faz parte do protocolo `TextIO` que o typeshed
  declara para `sys.stdout`.
- `# type: ignore[código]` como último recurso, sempre com o código do erro.

Docs: https://mypy.readthedocs.io/

### pytest

O que é/faz: framework de testes — descobre funções `test_*`, roda cada uma
como um caso isolado, e fornece fixtures prontas (`capsys` para capturar
saída, `monkeypatch` para substituir `input()` e funções por versões falsas).

Por que esta: é o framework de testes padrão do ecossistema Python hoje —
sintaxe simples (`assert` puro, sem `self.assertEqual`), e as fixtures
`capsys`/`monkeypatch` resolvem exatamente o que este projeto precisa: testar
um loop interativo sem um terminal de verdade.

O que estudar:
- `monkeypatch.setattr("builtins.input", ...)` — como simular respostas do
  usuário numa ordem fixa.
- `capsys.readouterr()` — como capturar o que o programa imprimiu.
- `pytest.raises(...)` — como afirmar que uma função levanta a exceção certa.
- `pythonpath = ["."]` em `pyproject.toml` — por que isso permite
  `import main` em `tests/test_main.py` sem transformar o projeto num pacote
  instalável.

Docs: https://docs.pytest.org/

## CI e supply chain

Roda no GitHub, fora da sua máquina: confere o código a cada mudança e vigia
as dependências. Os arquivos ficam em `.github/`.

### GitHub Actions

O que é/faz: serviço de automação do GitHub. O `ci.yml` roda `ruff`, `black
--check`, `mypy` e `pytest` a cada push e PR, em Python 3.12 (o piso), 3.14 e
3.15, para provar que o código funciona em todas as versões que o projeto diz
suportar.

Por que esta: é grátis para repositório público e já vive junto do código e
dos PRs — não há servidor de CI separado para manter. As Actions são fixadas
pelo SHA do commit (a versão vai no comentário), porque uma tag pode ser
movida depois de publicada e o SHA não; o runner tem rótulo fixo
(`ubuntu-26.04`), não `ubuntu-latest`, para a imagem não trocar sozinha.

O que estudar:
- A matriz (`strategy.matrix.python-version`) — como um job vira três.
- `uv sync --frozen` — instala exatamente o `uv.lock`, sem recalcular.
- Por que pinar Action por SHA em vez de por tag.

Docs: https://docs.github.com/actions

### CodeQL

O que é/faz: analisador estático de segurança do GitHub. Lê o código Python à
procura de padrões de vulnerabilidade (injeção, uso inseguro de `os.system`
com entrada externa etc.) e mostra os achados na aba Security.

Por que esta: roda como Action oficial, sem conta nem serviço extra. Também
roda uma vez por semana, para as consultas novas do CodeQL valerem sem
mudança no repositório.

O que estudar:
- A aba Security → Code scanning — onde os alertas aparecem.
- O gatilho `schedule` (cron) do `codeql.yml`.
- O que é um alerta de code scanning (formato SARIF) e como dispensar um falso positivo.

Docs: https://codeql.github.com/docs/

### pip-audit

O que é/faz: confere as versões do `uv.lock` contra a base pública de
vulnerabilidades conhecidas (CVEs). O `pip-audit.yml` roda toda segunda às
09:00 de São Paulo e à mão (`workflow_dispatch`).

Por que esta: o CI só roda em PR e o Dependabot nem sempre abre PR de
correção, então uma CVE publicada depois do último PR passaria despercebida.
Contra as alternativas: os Dependabot alerts só avisam e dependem do Dependabot
funcionar; o Safety depende de uma base própria da empresa; o OSV-Scanner serviria,
mas o `pip-audit` é mantido pela PyPA e lê direto o formato de requirements
que o `uv export` gera. Run vermelho significa vulnerabilidade conhecida no lock; a resposta é
atualizar as dependências.

O que estudar:
- `uv export` — como o lock vira um `requirements` para o auditor.
- `--no-deps` — por que o auditor não pode resolver o grafo de novo.
- O que é uma CVE/advisory e como o PyPI registra avisos de segurança.

Docs: https://pypi.org/project/pip-audit/

### Dependabot

O que é/faz: robô do GitHub que abre PRs de atualização de dependências
(`uv` e `github-actions`), aos domingos, agrupados por ecossistema; um major
vem em PR próprio. Uma versão nova espera 7 dias (cooldown) antes de virar PR.

Por que esta: manter ruff, black, mypy, pytest e as Actions em dia sem
lembrar de olhar. Contra o Renovate: mais configurável, mas exige instalar
um app à parte; o Dependabot já vem no GitHub e cobre `uv` e Actions. O cooldown evita adotar uma release recém-saída que pode
quebrar no dia da publicação; as security updates ignoram o cooldown.

O que estudar:
- `.github/dependabot.yml` — `groups`, `cooldown` e `schedule`.
- Como ler o PR agrupado: o que é minor/patch e por que o major vem separado.
- `open-pull-requests-limit` — como limitar quantos PRs ficam abertos ao mesmo tempo.

Docs: https://docs.github.com/code-security/dependabot

## O que deliberadamente não está na stack

- **Framework de CLI (`argparse`/`click`/`typer`)** — o programa só tem um
  fluxo interativo simples (`input()`/`print()`); não há flags nem subcomandos
  a analisar.
- **`colorama`** — sugerido no README como *exercício* para o leitor
  praticar (feedback visual colorido), não faz parte da implementação atual.
- **Framework web, banco de dados, fila, cache** — é um script de terminal
  sem persistência nem rede; nada disso tem papel aqui.
- **`requests`/`httpx`** — o programa não faz nenhuma chamada de rede.
