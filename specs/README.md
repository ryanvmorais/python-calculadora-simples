# Specs

Este projeto usa spec-driven development: cada funcionalidade é documentada em
`specs/NNN-nome/`, com três arquivos — `requirements.md` (o quê e porquê),
`design.md` (como) e `tasks.md` (quebra executável). O formato é Markdown
agnóstico de ferramenta; a skill `/spec` conduz o fluxo de escrita e os
portões de aprovação, mas os documentos valem por si, mesmo fora do Claude Code.

## Convenções

- **Numeração**: `NNN` sequencial de 3 dígitos, maior número existente + 1.
- **Frontmatter idêntico** nos três arquivos de uma spec:
  ```yaml
  ---
  feature: <título legível de uma linha>
  status: rascunho | aprovado | em andamento | concluído
  date: AAAA-MM-DD
  related:
    - NNN-outra/requirements.md
  origin: concepção | engenharia reversa
  ---
  ```
- **Critério de aceite**: Given/When/Then, um `### RF-NN` (heading) por
  requisito — aparece no outline e é linkável.
- **Rastreabilidade**: toda tarefa em `tasks.md` cita o(s) requisito(s) e/ou
  ADR que satisfaz (`— RF-01, ADR-2`).
- **Idioma**: português, seguindo a convenção do projeto (ver `CLAUDE.md`).

## Workflow

Fluxo normal (concepção): `requirements → design → tasks → implementação`,
cada fase com aprovação humana antes de avançar. Engenharia reversa é a
exceção — usada só para documentar retroativamente um projeto já finalizado
(como este, na modernização inicial); nesse caso tudo nasce com
`status: concluído` e as tarefas já marcadas `[x]`.

| Comando | Fase |
|---|---|
| `/spec nova <nome>` | Abre `requirements.md` em rascunho |
| `/spec design` | Escreve `design.md` |
| `/spec tasks` | Escreve `tasks.md` |
| `/spec implementar` | Executa as tarefas, uma a uma |
| `/spec status` | Panorama de todas as specs |

## Índice

| Spec | Escopo | Status |
|---|---|---|
| [001-calculadora-simples](001-calculadora-simples/requirements.md) | Calculadora de terminal — menu de operações, cálculo, tratamento de erros | concluído |

## Notas de manutenção

- Nenhuma landmine conhecida entre specs ainda (projeto de uma spec só).

## Padrão-ouro de formato

Use `001-calculadora-simples/` como referência de formato para as próximas
specs deste projeto.
