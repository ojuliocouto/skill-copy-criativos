"""TDD do planejador de blocos (`gate_copy.planejador` e o CLI
`planejar_blocos.py`): recebe o PLANO da peça antes da copy existir e diz
quantas palavras cada bloco pode ter.

Roda com: /usr/bin/python3 -m pytest ~/.claude/skills/copy-criativos/scripts/tests -q
"""

from __future__ import annotations

import os
import subprocess
import sys

import pytest

SCRIPTS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, SCRIPTS_DIR)

from gate_copy.planejador import (  # noqa: E402
    calcular_densidade,
    checar_ponte_do_plano,
    max_palavras_do_tipo,
    medio_palavras_do_tipo,
    min_palavras_do_tipo,
    planejar,
    validar_tipos,
)

PLANEJAR_PATH = os.path.join(SCRIPTS_DIR, "planejar_blocos.py")


def test_tipo_invalido_levanta_erro_acionavel():
    with pytest.raises(ValueError) as erro:
        validar_tipos(["I", "X"])
    assert "Faça:" in str(erro.value)


def test_palavras_min_max_batem_com_limiares_padrao():
    # insert_min_s=3.5, pps=2.9, aceleracao=1.45 -> ceil(3.5*2.9*1.45) = 15
    assert min_palavras_do_tipo("I", 2.9, 1.45) == 15
    # lettering placa: 2800ms -> ceil(2.8*2.9*1.45) = 12
    assert min_palavras_do_tipo("L", 2.9, 1.45) == 12
    # coluna/carimbo: 3500ms -> igual ao insert = 15
    assert min_palavras_do_tipo("LC", 2.9, 1.45) == 15
    # cta_min_s=3.0 -> ceil(3.0*2.9*1.45) = 13
    assert min_palavras_do_tipo("C", 2.9, 1.45) == 13
    # "A" nao tem minimo de DURACAO proprio, mas tem piso de PALAVRAS
    # (uma frase curta), pra simulacao no minimo nao sair com "0.00s"
    assert min_palavras_do_tipo("A", 2.9, 1.45) == 6
    # teto de frase (20) e o teto padrao pra quem nao tem duracao maxima
    assert max_palavras_do_tipo("I", 2.9, 1.45) == 20
    assert max_palavras_do_tipo("L", 2.9, 1.45) == 20


# ---------------------------------------------------------------------------
# Reproduz o pacote de exemplo agenda_cheia (L,L,I,L,I,A,C), palavras
# 13,12,17,15,24,4,17: mesma densidade e duracao que o gate mede no pacote.
# ---------------------------------------------------------------------------

AGENDA_CHEIA_TIPOS = ["L", "L", "I", "L", "I", "A", "C"]
AGENDA_CHEIA_PALAVRAS = [13, 12, 17, 15, 24, 4, 17]


def test_agenda_cheia_reproduz_duracao_e_densidade_do_gate():
    resultado = planejar(AGENDA_CHEIA_TIPOS, pps=2.9, aceleracao=1.45, palavras=AGENDA_CHEIA_PALAVRAS)

    # Duração total final: soma de palavras/pps/aceleracao bloco a bloco,
    # a MESMA conta que `leitura.ler_roteiro` faz pro gate.
    esperado_s = sum(p / 2.9 / 1.45 for p in AGENDA_CHEIA_PALAVRAS)
    assert resultado["total_final_s"] == pytest.approx(esperado_s, abs=0.01)

    densidade = resultado["densidade"]
    assert "corpo" in densidade
    assert 0.45 <= densidade["corpo"]["fracao"] <= 0.55
    assert "sugestao" not in densidade["corpo"]


def test_plano_iii_acusa_densidade_de_insert_acima_de_55_no_corpo():
    resultado = planejar(["I", "I", "I"], pps=2.9, aceleracao=1.45)
    densidade = resultado["densidade"]
    assert "corpo" in densidade
    assert densidade["corpo"]["fracao"] > 0.55
    assert "sugestao" in densidade["corpo"]
    assert "insert" in densidade["corpo"]["sugestao"]
    assert "corpo" in densidade["corpo"]["sugestao"]


def test_alvo_que_nao_cabe_reporta_nao_cabe():
    resultado = planejar(["I", "I"], pps=2.9, aceleracao=1.45, alvo_s=1.0)
    assert resultado["alvo_cabe"] is False


def test_alvo_que_cabe_reporta_cabe():
    resultado = planejar(AGENDA_CHEIA_TIPOS, pps=2.9, aceleracao=1.45, alvo_s=24.0)
    assert resultado["soma_min_s"] <= 24.0 <= resultado["soma_max_s"]
    assert resultado["alvo_cabe"] is True


def test_quantidade_de_palavras_diferente_da_quantidade_de_blocos_levanta_erro():
    with pytest.raises(ValueError) as erro:
        planejar(["I", "I"], palavras=[10])
    assert "Faça:" in str(erro.value)


# ---------------------------------------------------------------------------
# CLI (subprocess)
# ---------------------------------------------------------------------------


def test_cli_planejar_blocos_agenda_cheia_roda_e_mostra_densidade():
    resultado = subprocess.run(
        [
            sys.executable, PLANEJAR_PATH,
            "--modo", "pago", "--campanha", "frio",
            "--blocos", "L,L,I,L,I,A,C",
            "--palavras", "13,12,17,15,24,4,17",
        ],
        capture_output=True,
        text=True,
    )
    assert resultado.returncode == 0
    assert "DENSIDADE DE INSERT POR JANELA" in resultado.stdout
    assert "corpo" in resultado.stdout


# ---------------------------------------------------------------------------
# Ponte no plano (símbolo "P", regra do dono da metodologia)
# ---------------------------------------------------------------------------


def test_plano_com_p_antes_do_c_nao_avisa():
    assert checar_ponte_do_plano(["L", "L", "I", "P", "C"]) == []


def test_plano_com_insert_antes_do_c_nao_avisa():
    assert checar_ponte_do_plano(["L", "L", "I", "C"]) == []


def test_plano_sem_ponte_nem_insert_antes_do_c_avisa():
    avisos = checar_ponte_do_plano(["L", "L", "A", "C"])
    assert len(avisos) == 1
    assert "plano sem ponte antes do CTA" in avisos[0]
    assert "Faça:" in avisos[0]


def test_plano_agenda_cheia_v1_bloco_a_antes_do_c_avisa():
    # L,L,I,L,I,A,C (o plano real do pacote agenda_cheia v1, reprovado pelo
    # dono da metodologia por falta de ponte): o bloco imediatamente antes
    # do C e um "A" comum, que NAO conta como ponte -> avisa.
    avisos = checar_ponte_do_plano(AGENDA_CHEIA_TIPOS)
    assert len(avisos) == 1
    assert "plano sem ponte antes do CTA" in avisos[0]


def test_plano_e_incluido_no_resultado_de_planejar():
    resultado = planejar(["A", "C"], pps=2.9, aceleracao=1.45)
    assert len(resultado["avisos_plano"]) == 1
    assert "plano sem ponte antes do CTA" in resultado["avisos_plano"][0]


def test_p_tem_mesmos_limites_de_a():
    assert min_palavras_do_tipo("P", 2.9, 1.45) == min_palavras_do_tipo("A", 2.9, 1.45)
    assert max_palavras_do_tipo("P", 2.9, 1.45) == max_palavras_do_tipo("A", 2.9, 1.45)


# ---------------------------------------------------------------------------
# Piso de palavras do "A"/"P" (bloco de apresentador sozinho, sem insert e
# sem KEY) e o ponto médio como recomendação final (sem isso a simulação no
# mínimo saía com 0 palavras e "duração 0.00s", distorcendo a densidade).
# ---------------------------------------------------------------------------

AGENDA_CHEIA_V3_TIPOS = ["L", "L", "I", "A", "I", "I", "A", "I", "C"]
AGENDA_CHEIA_V3_PALAVRAS = [13, 12, 15, 11, 15, 15, 14, 16, 15]


def test_agenda_cheia_v3_com_palavras_reproduz_densidade_medida_pelo_gate():
    # Mesmo plano e mesma contagem de palavras do exemplo versionado
    # exemplos/agenda-cheia: rodando o gate nesse pacote real dá zero
    # reprovações e zero avisos, ou seja, corpo e fecho já caem dentro da
    # faixa 45% a 55% de densidade de insert.
    resultado = planejar(AGENDA_CHEIA_V3_TIPOS, pps=2.9, aceleracao=1.45, palavras=AGENDA_CHEIA_V3_PALAVRAS)
    densidade = resultado["densidade"]
    assert "corpo" in densidade
    assert 0.45 <= densidade["corpo"]["fracao"] <= 0.55
    assert "sugestao" not in densidade["corpo"]
    assert "fecho" in densidade
    assert 0.45 <= densidade["fecho"]["fracao"] <= 0.55
    assert "sugestao" not in densidade["fecho"]


def test_medio_palavras_de_a_e_p_usa_meio_do_minimo_ao_maximo():
    min_p = min_palavras_do_tipo("A", 2.9, 1.45)
    max_p = max_palavras_do_tipo("A", 2.9, 1.45)
    assert medio_palavras_do_tipo("A", min_p, max_p) == round((min_p + max_p) / 2)


def test_medio_palavras_de_bloco_sem_maximo_proprio_usa_minimo_mais_seis():
    min_p = min_palavras_do_tipo("I", 2.9, 1.45)
    assert medio_palavras_do_tipo("I", min_p, max_palavras_do_tipo("I", 2.9, 1.45)) == min_p + 6


def test_plano_sem_palavras_nao_tem_nenhum_bloco_com_zero_palavras():
    resultado = planejar(AGENDA_CHEIA_V3_TIPOS, pps=2.9, aceleracao=1.45)
    assert all(l.palavras > 0 for l in resultado["linhas"])
    assert all(b.palavras > 0 for b in resultado["blocos_simulados"])
    assert all(b.duracao_final > 0 for b in resultado["blocos_simulados"])
    # a recomendação final é o ponto médio, não o mínimo
    assert resultado["blocos_simulados"] != resultado["blocos_simulados_minimo"]


def test_cli_plano_agenda_cheia_v3_sem_palavras_nao_imprime_bloco_com_zero():
    resultado = subprocess.run(
        [
            sys.executable, PLANEJAR_PATH,
            "--modo", "pago", "--campanha", "frio",
            "--blocos", "L,L,I,A,I,I,A,I,C",
        ],
        capture_output=True,
        text=True,
    )
    assert resultado.returncode == 0
    assert "duração 0.00s (0 palavras)" not in resultado.stdout
    assert "(0 palavras)" not in resultado.stdout
    assert "PONTO MÉDIO" in resultado.stdout


def test_cli_tipo_invalido_retorna_erro():
    resultado = subprocess.run(
        [sys.executable, PLANEJAR_PATH, "--blocos", "I,Z"],
        capture_output=True,
        text=True,
    )
    assert resultado.returncode == 2
    assert "Faça:" in resultado.stderr
