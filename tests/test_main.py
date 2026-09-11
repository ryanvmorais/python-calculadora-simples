"""Testes para main.py.

Estratégia de isolamento: `limpar_tela` é sempre mockada nos testes do loop
principal para evitar a chamada real a `os.system` (limpeza de tela não tem
efeito observável fora do terminal interativo, e travaria a suíte tentando
manipular o console do CI). As entradas do usuário são simuladas via
`monkeypatch` sobre `builtins.input`, na ordem em que `calculadora()` as
consome.
"""

from __future__ import annotations

from collections.abc import Iterator

import pytest

import main

# ---------------------------------------------------------------------------
# realizar_calculo
# ---------------------------------------------------------------------------


def test_realizar_calculo_soma() -> None:
    assert main.realizar_calculo(2, 3, "+") == 5


def test_realizar_calculo_subtracao() -> None:
    assert main.realizar_calculo(5, 3, "-") == 2


def test_realizar_calculo_multiplicacao() -> None:
    assert main.realizar_calculo(4, 3, "*") == 12


def test_realizar_calculo_divisao() -> None:
    assert main.realizar_calculo(9, 2, "/") == 4.5


def test_realizar_calculo_exponenciacao() -> None:
    assert main.realizar_calculo(2, 5, "^") == 32


def test_realizar_calculo_divisao_por_zero_levanta_erro() -> None:
    """Divisão por zero deve levantar ZeroDivisionError, não retornar string."""
    with pytest.raises(ZeroDivisionError):
        main.realizar_calculo(1, 0, "/")


def test_realizar_calculo_simbolo_desconhecido_levanta_erro() -> None:
    with pytest.raises(ValueError):
        main.realizar_calculo(1, 2, "%")


# ---------------------------------------------------------------------------
# exibir_menu
# ---------------------------------------------------------------------------


def test_exibir_menu_numera_a_partir_de_1(capsys: pytest.CaptureFixture[str]) -> None:
    main.exibir_menu(["Soma", "Subtração"])
    saida = capsys.readouterr().out
    assert "1 : Soma" in saida
    assert "2 : Subtração" in saida


# ---------------------------------------------------------------------------
# calculadora (loop principal)
# ---------------------------------------------------------------------------


def _entradas(valores: list[str]) -> Iterator[str]:
    """Gera as respostas de `input()` na ordem fornecida.

    Args:
        valores (list[str]): Sequência de respostas simuladas do usuário.

    Yields:
        str: A próxima resposta simulada.
    """
    yield from valores


@pytest.fixture(autouse=True)
def _sem_limpeza_de_tela(monkeypatch: pytest.MonkeyPatch) -> None:
    """Substitui limpar_tela por um no-op em todo o módulo de teste.

    Evita a chamada real a `os.system("cls"/"clear")`, que não tem efeito
    observável fora de um terminal interativo.
    """
    monkeypatch.setattr(main, "limpar_tela", lambda: None)


def test_calculadora_realiza_soma_e_sai(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Fluxo feliz: escolhe Soma, calcula 5 + 3 e sai na primeira rodada."""
    respostas = _entradas(["1", "5", "3", "1"])
    monkeypatch.setattr("builtins.input", lambda _prompt="": next(respostas))

    main.calculadora()

    saida = capsys.readouterr().out
    assert "RESULTADO: 5.0 + 3.0 = 8.0" in saida
    assert "Calculadora encerrada." in saida


def test_calculadora_trata_divisao_por_zero_sem_travar(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Divisão por zero mostra o aviso e permite continuar até sair."""
    respostas = _entradas(["4", "5", "0", "", "1", "5", "3", "1"])
    monkeypatch.setattr("builtins.input", lambda _prompt="": next(respostas))

    main.calculadora()

    saida = capsys.readouterr().out
    assert "Erro: Divisão por zero!" in saida
    assert "Calculadora encerrada." in saida


def test_calculadora_trata_entrada_nao_numerica_sem_travar(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Digitar letras no lugar de um número mostra o aviso e não derruba o loop."""
    respostas = _entradas(["1", "abc", "", "1", "5", "3", "1"])
    monkeypatch.setattr("builtins.input", lambda _prompt="": next(respostas))

    main.calculadora()

    saida = capsys.readouterr().out
    assert "Erro: Por favor, digite apenas números." in saida
    assert "Calculadora encerrada." in saida


def test_calculadora_opcao_invalida_pede_nova_escolha(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Escolher um número fora do intervalo do menu pede nova tentativa."""
    respostas = _entradas(["9", "", "1", "5", "3", "1"])
    monkeypatch.setattr("builtins.input", lambda _prompt="": next(respostas))

    main.calculadora()

    saida = capsys.readouterr().out
    assert "Opção inválida!" in saida
    assert "Calculadora encerrada." in saida
