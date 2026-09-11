![Calculadora Simples em Python - Lógica de Programação e Dicionários](https://github.com/ryanvmorais/python-calculadora-simples/blob/main/assets/calculadora-simples-python-logica-promacacao.png?raw=true)

# 🧮 Calculadora Simples em Python | Exercício de Lógica e Dicionários

![Python](https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white)
![deps](https://img.shields.io/badge/deps-uv-DE5FE9)
[![CI](https://github.com/ryanvmorais/python-calculadora-simples/actions/workflows/ci.yml/badge.svg)](https://github.com/ryanvmorais/python-calculadora-simples/actions/workflows/ci.yml)
![Lint](https://img.shields.io/badge/lint-ruff-261230)
![Format](https://img.shields.io/badge/style-black-000000)
![Types](https://img.shields.io/badge/types-mypy%20strict-2A6DB2)
![License](https://img.shields.io/badge/license-MIT-green)

Este repositório contém uma **Calculadora Funcional** desenvolvida em Python, criada como material de estudo para quem está iniciando na programação. O foco principal é demonstrar como organizar menus interativos e **realizar operações matemáticas básicas** de forma limpa.

### 🎯 Objetivo do Projeto:
Praticar o uso de **Dicionários**, **Loops de repetição** e **Tratamento de Erros**. É o projeto ideal para entender como o Python processa entradas do usuário e entrega resultados matemáticos em tempo real.

---

### 📚 O que você vai aprender com este projeto?
Este exercício foi estruturado para consolidar conceitos essenciais de algoritmos:

*   **Dicionários (Mapping):** Como mapear símbolos matemáticos (`+`, `-`, `*`, `/`) para nomes legíveis.
*   **Tratamento de Erros (Try/Except):** Como evitar que o programa feche ao tentar dividir por zero ou digitar letras.
*   **Manipulação de Listas:** Transformar chaves de dicionários em listas para acessar opções por números (`índices`).
*   **UX no Terminal:** Uso do módulo `subprocess` para limpar a tela e criar uma interface dinâmica.

---
### 🧠 Guia de Implementação (A Lógica por trás do Código):
Para quem está começando, o maior desafio não é a sintaxe, mas a **montagem do raciocínio**. Confira o passo a passo da construção deste jogo:
1.  **Dicionário de Operações:** Em vez de usar vários `if`, guardamos as operações em um dicionário (`dict`). Isso permite que o programa "saiba" o nome de cada símbolo automaticamente.
2.  **Menu Dinâmico:** O código percorre o dicionário e cria um menu numerado. Assim, se você adicionar uma nova operação no futuro, o menu se atualiza sozinho!
3.  **Captura Segura:** Usamos o `int(input()) - 1` para converter a escolha do usuário no índice correto do Python (que sempre começa em 0).
4.  **Blindagem (Try/Except):** O código é "blindado". Se o usuário digitar algo errado, o programa avisa o erro educadamente em vez de travar.

---

### 🛠️ Tecnologias e Ferramentas:
Para garantir a melhor experiência de aprendizado e a execução correta de todos os recursos (como a limpeza de tela automática), o projeto utiliza as seguintes tecnologias:


| Ferramenta | Descrição | Badge |
| :--- | :--- | :--- |
| **Python 3** | Linguagem principal utilizada no desenvolvimento do algoritmo. | ![Linguagem Python](https://img.shields.io/badge/-Python-3776AB%3Fstyle%3Dflat%26logo%3Dpython?logo=python&logoColor=3776AB&logoSize=flat&color=F0F0F0) |
| **uv** | Gerenciador de dependências e ambiente virtual — instala tudo com um único comando. | ![uv](https://img.shields.io/badge/uv-DE5FE9?style=flat&logo=uv&logoColor=white) |
| **ruff / black / mypy** | Lint, formatação e checagem de tipos — mantêm o código no padrão antes de cada commit. | ![Ruff](https://img.shields.io/badge/Ruff-D7FF64?style=flat&logo=ruff&logoColor=black) |
| **pytest** | Framework de testes automatizados usado em `tests/test_main.py`. | ![Pytest](https://img.shields.io/badge/pytest-0A9EDC?style=flat&logo=pytest&logoColor=white) |
| **Terminal** | Interface onde o jogo é executado e processa as entradas do usuário. | ![Terminal](https://img.shields.io/badge/Terminal-241F31?style=flat&logo=gnometerminal&logoColor=241F31&color=F0F0F0) |
| **VS Code / PyCharm** | IDEs recomendadas para edição, depuração e refatoração do arquivo `main.py`. | ![PyCharm](https://img.shields.io/badge/PyCharm-pycharm?style=flat&logo=pycharm&logoColor=000000&color=F0F0F0) |

---

### ✅ Requisitos Mínimos:

Para garantir que o jogo funcione corretamente, certifique-se de ter os seguintes itens instalados:

- **Python 3.12 ou superior:** O código utiliza recursos modernos da linguagem.
- **[uv](https://docs.astral.sh/uv/getting-started/installation/):** Gerenciador de dependências e ambiente virtual — instala e roda o projeto com um único comando.
- **VS Code / PyCharm (Opcional):** Recomendado para abrir e editar o arquivo `main.py` com suporte total a refatoração e depuração.

> **Dica:** Para verificar sua versão do Python, digite `python --version`; para conferir se o `uv` está instalado, digite `uv --version`.

---

### ⚙️ Como Executar o Projeto:
1. **Clone o repositório:**
   ```bash
   git clone https://github.com/ryanvmorais/python-calculadora-simples.git
   ``` 
2. **Execute o script:**
- Navegue até a **pasta do projeto** e utilize o comando abaixo no seu terminal (CMD, PowerShell ou Terminal do VS Code/PyCharm). O `uv` cria o ambiente virtual automaticamente na primeira execução:
   ```bash
   uv run main.py
   ```
> **Nota:** O jogo detectará automaticamente se você está no `Windows`, `Linux` ou `macOS` para gerenciar a limpeza da tela.
---
### ▶️ Execução Simplificada (Atalhos):
Para facilitar o acesso de quem está começando, adicionei scripts de inicialização automática. Basta baixar o projeto e:
* **No Windows:** Dê dois cliques no arquivo `iniciar_calculadora.bat`.
* **No Linux/macOS:** Execute o arquivo `iniciar_calculadora.sh` no terminal.

*Esses scripts verificam automaticamente se você tem o `uv` instalado antes de iniciar a calculadora.*

---

### 🧪 Testes e Qualidade:

O projeto tem uma suíte de testes automatizados e um portão de qualidade —
úteis tanto para garantir que suas modificações não quebram nada quanto como
material de estudo de testes em Python.

```bash
uv sync                       # instala as dependências de desenvolvimento
uv run ruff check --fix .     # lint
uv run black .                # formatação
uv run mypy main.py tests     # checagem de tipos
uv run pytest                 # testes
```

Para entender a stack (o que cada ferramenta faz e por que foi escolhida),
veja [`docs/stack.md`](docs/stack.md). Para o comportamento esperado do
programa e o histórico de decisões, veja [`specs/`](specs/). Para orientações
de arquitetura e convenções voltadas a quem edita o código, veja
[`CLAUDE.md`](CLAUDE.md).

---
### 📋 Atividade para praticar:

Para exercitar o que aprendeu, tente modificar o código e implementar estas novas funcionalidades:

1. 🏆 Histórico de Operações (Gerenciamento de Estado):

O desafio é criar um registro que armazene todos os cálculos feitos durante a sessão.
* **O Conceito:** Aprenda a diferenciar variáveis de **valor único** de estruturas que acumulam o **histórico de dados**.
* **A Lógica:** Implemente uma lista (ex: `historico_calculos`) que armazene cada string de resultado gerada. Crie uma nova opção no menu para exibir essa lista, permitindo que o usuário veja tudo o que foi calculado sem que os dados sumam a cada limpeza de tela.
* **O Aprendizado:** Você entenderá como persistir informações em memória e como manipular listas para exibição posterior.
2. **📊 Novas Funções Matemáticas:** Expanda o dicionário de operações para incluir o **Resto da Divisão (%)** e a **Raiz Quadrada (√)**. Lembre-se de tratar os casos onde o segundo valor não é necessário.
3. **🎨 Feedback Visual:** Utilize a biblioteca `colorama` para exibir os resultados em **verde** e as mensagens de erro (como divisão por zero) em **vermelho**, melhorando a experiência do usuário.

---

### 🎮 Continue praticando

Este projeto faz parte de uma série de exercícios de lógica de programação em Python. Depois deste, experimente:

* **[Jogo da Velha em Python](https://github.com/ryanvmorais/python-jogo-da-velha):** Matrizes e Programação Orientada a Objetos.
* **[Jogo da Cobrinha em Python](https://github.com/ryanvmorais/python-jogo-da-cobrinha):** Listas dinâmicas e game loop com `curses`.
* **[Pedra, Papel e Tesoura em Python](https://github.com/ryanvmorais/python-pedra-papel-tesoura):** Dicionários e POO.

Veja todos os projetos e vídeos do canal em [aprenda-com-ryan-morais](https://github.com/ryanvmorais/aprenda-com-ryan-morais).

---

### 💡 Ficou com alguma dúvida ou tem sugestões?

Aprender algo novo tem seus desafios, mas estou aqui para caminharmos juntos! Se você encontrou algum erro, teve dificuldade em rodar o jogo ou pensou em uma funcionalidade incrível para adicionar:

*   **Abra uma [Issue](https://github.com/ryanvmorais/python-calculadora-simples/issues):** Clique no link e descreva sua dúvida ou sugestão. É a melhor forma de trocarmos conhecimento e ajudarmos outras pessoas que tenham a mesma dúvida!
*   **Me mande um E-mail:** Se preferir algo mais privado, pode me escrever em [**contato@ryanmorais.com.br**](mailto:contato@ryanmorais.com.br).

Ficarei muito feliz em ver seu progresso e receber seu feedback para melhorar cada vez mais nossos materiais de estudo! 🤝

---

### ⚖️ Licença

Este projeto está sob a **Licença MIT**. Isso significa que você pode usar, copiar e modificar o código à vontade, inclusive para seus próprios projetos. Para mais detalhes, consulte o arquivo [LICENSE](LICENSE).