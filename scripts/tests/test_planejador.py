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
    capacidade_de_garrafais,
    checar_capacidade_de_garrafais,
    checar_oferta_do_plano,
    checar_ponte_do_plano,
    checar_vizinhos_sem_insert,
    derivar_forma_de_papeis,
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


# ---------------------------------------------------------------------------
# Blocos vizinhos sem insert somando acima do teto (mesmo limiar do gate,
# retencao.avatar_sozinho_max_s = 6,0s), item 2 da correção de gaps.
# ---------------------------------------------------------------------------

VIZINHOS_TIPOS = ["L", "L", "I", "A", "I", "A", "I", "C"]
VIZINHOS_PALAVRAS_ACUSA = [13, 13, 15, 13, 16, 11, 18, 15]
VIZINHOS_PALAVRAS_NAO_ACUSA = [13, 12, 15, 13, 16, 11, 18, 15]


def test_vizinhos_sem_insert_acima_do_teto_acusa_blocos_1_e_2():
    resultado = planejar(VIZINHOS_TIPOS, pps=2.9, aceleracao=1.45, palavras=VIZINHOS_PALAVRAS_ACUSA)
    avisos = resultado["avisos_vizinhos"]
    assert len(avisos) == 1
    assert "blocos 1 e 2" in avisos[0]
    assert "sem insert somam" in avisos[0]
    assert "teto 6.0s" in avisos[0]
    assert "Faça: intercale um insert ou encurte um deles" in avisos[0]


def test_vizinhos_sem_insert_dentro_do_teto_nao_acusa():
    resultado = planejar(VIZINHOS_TIPOS, pps=2.9, aceleracao=1.45, palavras=VIZINHOS_PALAVRAS_NAO_ACUSA)
    assert resultado["avisos_vizinhos"] == []


def test_checar_vizinhos_sem_insert_ignora_par_com_insert():
    resultado = planejar(AGENDA_CHEIA_V3_TIPOS, pps=2.9, aceleracao=1.45, palavras=AGENDA_CHEIA_V3_PALAVRAS)
    assert resultado["avisos_vizinhos"] == []


def test_planejar_sem_palavras_tambem_calcula_avisos_vizinhos_min_e_medio():
    resultado = planejar(VIZINHOS_TIPOS, pps=2.9, aceleracao=1.45)
    assert "avisos_vizinhos" in resultado
    assert "avisos_vizinhos_minimo" in resultado
    assert isinstance(resultado["avisos_vizinhos"], list)
    assert isinstance(resultado["avisos_vizinhos_minimo"], list)


def test_cli_mostra_aviso_de_vizinhos_sem_insert():
    resultado = subprocess.run(
        [
            sys.executable, PLANEJAR_PATH,
            "--modo", "pago", "--campanha", "frio",
            "--blocos", ",".join(VIZINHOS_TIPOS),
            "--palavras", ",".join(str(p) for p in VIZINHOS_PALAVRAS_ACUSA),
        ],
        capture_output=True,
        text=True,
    )
    assert resultado.returncode == 0
    assert "blocos 1 e 2" in resultado.stdout
    assert "AVISOS (blocos vizinhos sem insert)" in resultado.stdout


def test_cli_tipo_invalido_retorna_erro():
    resultado = subprocess.run(
        [sys.executable, PLANEJAR_PATH, "--blocos", "I,Z"],
        capture_output=True,
        text=True,
    )
    assert resultado.returncode == 2
    assert "Faça:" in resultado.stderr


# ---------------------------------------------------------------------------
# Capacidade de garrafais da forma (item E da correção de gaps): bloco 1 +
# blocos A/P sem KEY; aviso quando menor que 2.
# ---------------------------------------------------------------------------


def test_capacidade_de_garrafais_conta_bloco_1_mais_a_e_p():
    # bloco 1 (gancho) + bloco 4 (A) + bloco 6 (P) = 3
    assert capacidade_de_garrafais(["L", "I", "I", "A", "I", "P", "C"]) == 3


def test_capacidade_de_garrafais_sem_a_ou_p_conta_so_o_bloco_1():
    assert capacidade_de_garrafais(["I", "I", "C"]) == 1


def test_capacidade_de_garrafais_lista_vazia_e_zero():
    assert capacidade_de_garrafais([]) == 0


def test_checar_capacidade_de_garrafais_avisa_abaixo_de_2():
    avisos = checar_capacidade_de_garrafais(["I", "I", "C"])
    assert len(avisos) == 1
    assert "1 bloco" in avisos[0]
    assert "Faça:" in avisos[0]


def test_checar_capacidade_de_garrafais_nao_avisa_com_2_ou_mais():
    assert checar_capacidade_de_garrafais(["L", "I", "A", "I", "C"]) == []


def test_planejar_devolve_capacidade_de_garrafais():
    resultado = planejar(["L", "I", "I", "C"], pps=2.9, aceleracao=1.45)
    assert resultado["capacidade_garrafais"] == 1
    assert resultado["avisos_garrafais"]


def test_cli_mostra_capacidade_de_garrafais():
    resultado = subprocess.run(
        [
            sys.executable, PLANEJAR_PATH,
            "--modo", "pago", "--campanha", "frio",
            "--blocos", "L,I,I,C",
        ],
        capture_output=True,
        text=True,
    )
    assert resultado.returncode == 0
    assert "CAPACIDADE DE GARRAFAIS" in resultado.stdout
    assert "AVISO" in resultado.stdout


# ---------------------------------------------------------------------------
# --papeis (item A da correção de gaps): deriva a forma a partir da fila de
# PAPÉIS e imprime a forma derivada antes do relatório.
# ---------------------------------------------------------------------------


def test_cli_papeis_deriva_forma_e_imprime_antes_do_relatorio():
    resultado = subprocess.run(
        [
            sys.executable, PLANEJAR_PATH,
            "--modo", "pago", "--campanha", "frio",
            "--papeis", "H,D,P,I,P,M,P+T,O,C",
        ],
        capture_output=True,
        text=True,
    )
    assert resultado.returncode == 0
    esperado = ",".join(derivar_forma_de_papeis(["H", "D", "P", "I", "P", "M", "P+T", "O", "C"]))
    assert esperado in resultado.stdout
    indice_forma = resultado.stdout.index(esperado)
    indice_plano = resultado.stdout.index("PLANO POR BLOCO:")
    assert indice_forma < indice_plano


def test_cli_papeis_e_blocos_juntos_e_erro():
    resultado = subprocess.run(
        [
            sys.executable, PLANEJAR_PATH,
            "--blocos", "I,C", "--papeis", "P,C",
        ],
        capture_output=True,
        text=True,
    )
    assert resultado.returncode == 2


def test_cli_sem_blocos_nem_papeis_e_erro():
    resultado = subprocess.run(
        [sys.executable, PLANEJAR_PATH],
        capture_output=True,
        text=True,
    )
    assert resultado.returncode == 2


def test_cli_papeis_com_papel_invalido_retorna_erro():
    resultado = subprocess.run(
        [sys.executable, PLANEJAR_PATH, "--papeis", "H,Z,C"],
        capture_output=True,
        text=True,
    )
    assert resultado.returncode == 2
    assert "Faça:" in resultado.stderr


def test_cli_papeis_sem_oferta_antes_do_cta_avisa():
    resultado = subprocess.run(
        [
            sys.executable, PLANEJAR_PATH,
            "--modo", "pago", "--campanha", "frio",
            "--papeis", "H,D,P,M,T,C",
        ],
        capture_output=True,
        text=True,
    )
    assert resultado.returncode == 0
    assert "plano sem bloco O de oferta antes do CTA" in resultado.stdout


# ---------------------------------------------------------------------------
# --formato completo|curto (pedido do coordenador, references/modelo-mestre.md):
# define o alvo (62s ou 28s) e avisa quando o plano completo tem menos de 9
# blocos.
# ---------------------------------------------------------------------------


def test_cli_formato_completo_define_alvo_62s():
    resultado = subprocess.run(
        [
            sys.executable, PLANEJAR_PATH,
            "--modo", "pago", "--campanha", "frio",
            "--papeis", "H,D,P,I,P,M,P+T,O,C", "--formato", "completo",
        ],
        capture_output=True,
        text=True,
    )
    assert resultado.returncode == 0
    assert "formato: completo (alvo 62s finais" in resultado.stdout
    assert "ALVO: 62.00s" in resultado.stdout


def test_cli_formato_curto_define_alvo_28s():
    resultado = subprocess.run(
        [
            sys.executable, PLANEJAR_PATH,
            "--modo", "pago", "--campanha", "frio",
            "--papeis", "H,P,O+T,C", "--formato", "curto",
        ],
        capture_output=True,
        text=True,
    )
    assert resultado.returncode == 0
    assert "formato: curto (alvo 28s finais" in resultado.stdout
    assert "ALVO: 28.00s" in resultado.stdout


def test_cli_formato_completo_avisa_com_menos_de_9_blocos():
    resultado = subprocess.run(
        [
            sys.executable, PLANEJAR_PATH,
            "--modo", "pago", "--campanha", "frio",
            "--papeis", "H,P,O+T,C", "--formato", "completo",
        ],
        capture_output=True,
        text=True,
    )
    assert resultado.returncode == 0
    assert "abaixo de 9" in resultado.stdout


def test_cli_formato_completo_nao_avisa_com_9_blocos_ou_mais():
    resultado = subprocess.run(
        [
            sys.executable, PLANEJAR_PATH,
            "--modo", "pago", "--campanha", "frio",
            "--papeis", "H,D,P,I,P,M,P+T,O,C", "--formato", "completo",
        ],
        capture_output=True,
        text=True,
    )
    assert resultado.returncode == 0
    assert "abaixo de 9" not in resultado.stdout


def test_cli_alvo_s_explicito_tem_prioridade_sobre_formato():
    resultado = subprocess.run(
        [
            sys.executable, PLANEJAR_PATH,
            "--modo", "pago", "--campanha", "frio",
            "--papeis", "H,D,P,I,P,M,P+T,O,C", "--formato", "completo", "--alvo-s", "40",
        ],
        capture_output=True,
        text=True,
    )
    assert resultado.returncode == 0
    assert "ALVO: 40.00s" in resultado.stdout


def test_cli_papeis_com_oferta_antes_do_cta_nao_avisa_oferta():
    resultado = subprocess.run(
        [
            sys.executable, PLANEJAR_PATH,
            "--modo", "pago", "--campanha", "frio",
            "--papeis", "H,D,P,M,T,O,C",
        ],
        capture_output=True,
        text=True,
    )
    assert resultado.returncode == 0
    assert "plano sem bloco O de oferta antes do CTA" not in resultado.stdout


# ---------------------------------------------------------------------------
# Planejador x gate na oferta/ponte (item 5 da correção): `checar_oferta_do_plano`
# aceita "O" em qualquer um dos 3 papéis antes do "C" (igual à janela do gate
# em `regras.cta.checar_oferta`), e `checar_ponte_do_plano` aceita a ponte em
# "T", "P+T", "I", "O+T" ou "O" imediatamente antes do "C" (a ponte pode ser a
# última frase da própria oferta).
# ---------------------------------------------------------------------------


def test_sequencia_real_casa_medida_sem_aviso_de_oferta_nem_ponte():
    """H,D,P,I,P,M,P,O,P+T,C (a sequência real do pacote Casa Medida): o
    "O" está no bloco 8, com "P+T" (a ponte) entre ele e o "C" no bloco 10.
    Antes da correção, `checar_oferta_do_plano` só olhava o papel
    IMEDIATAMENTE anterior ao "C" (aqui, "P+T", sem "O") e avisava à toa."""
    papeis = ["H", "D", "P", "I", "P", "M", "P", "O", "P+T", "C"]
    assert checar_oferta_do_plano(papeis) == []

    tipos = derivar_forma_de_papeis(papeis)
    assert checar_ponte_do_plano(tipos) == []


def test_checar_oferta_do_plano_aceita_o_ate_3_blocos_antes_do_c():
    """"O" dois blocos antes do "C" (dentro da janela de 3) não avisa."""
    assert checar_oferta_do_plano(["H", "O", "T", "C"]) == []


def test_checar_oferta_do_plano_o_fora_da_janela_de_3_avisa():
    """"O" quatro blocos antes do "C" (fora da janela de 3) ainda avisa."""
    avisos = checar_oferta_do_plano(["H", "O", "D", "M", "T", "C"])
    assert len(avisos) == 1
    assert "plano sem bloco O de oferta antes do CTA" in avisos[0]


def test_checar_oferta_do_plano_sem_o_na_janela_avisa():
    avisos = checar_oferta_do_plano(["H", "D", "P", "M", "T", "C"])
    assert len(avisos) == 1
    assert "plano sem bloco O de oferta antes do CTA" in avisos[0]
    assert "Faça:" in avisos[0]


def test_checar_ponte_do_plano_aceita_papel_t_imediatamente_antes_do_c():
    assert checar_ponte_do_plano(["H", "D", "P", "T", "C"]) == []


def test_checar_ponte_do_plano_aceita_papel_o_imediatamente_antes_do_c():
    """A ponte pode ser a última frase da própria oferta: um "O" sozinho
    imediatamente antes do "C" também conta como ponte."""
    assert checar_ponte_do_plano(["H", "D", "P", "O", "C"]) == []


def test_checar_ponte_do_plano_aceita_o_mais_t_combinado_antes_do_c():
    assert checar_ponte_do_plano(["H", "D", "P", "O+T", "C"]) == []


def test_checar_ponte_do_plano_forma_continua_igual_antes_da_correcao():
    """As chamadas antigas (alfabeto de FORMA: I/L/LC/A/P/C) continuam
    exatamente com o mesmo resultado: "T" e "O" nunca aparecem nesse
    alfabeto, então a expansão não muda nada aqui."""
    assert checar_ponte_do_plano(["L", "L", "I", "P", "C"]) == []
    assert checar_ponte_do_plano(["L", "L", "I", "C"]) == []
    avisos = checar_ponte_do_plano(["L", "L", "A", "C"])
    assert len(avisos) == 1
    assert "plano sem ponte antes do CTA" in avisos[0]
