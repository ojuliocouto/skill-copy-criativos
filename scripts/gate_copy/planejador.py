#!/usr/bin/env python3
"""Planejador de blocos: recebe o PLANO da peça (a sequência de tipos de
bloco) antes de a copy existir, e devolve quantas palavras cada bloco pode
ter, usando os mesmos `LIMIARES` que o gate de copy mede depois.

Tipos de bloco aceitos (seção 9 do contrato, mesma tabela do gate):
- "I": bloco com inserção de vídeo (mínimo `insert_min_s`).
- "L": bloco só com lettering em placa (mínimo da categoria "placa").
- "LC": bloco com lettering em coluna ou carimbo (mínimo dessas categorias).
- "A": apresentador sozinho, sem KEY (máximo `retencao_avatar_sozinho_max_s`,
  sem mínimo próprio).
- "P": bloco de ponte, apresentador sozinho ligando o corpo ao CTA (mesmos
  limites de "A"). O plano avisa quando o bloco logo antes do "C" não é
  "P" nem "I" (regra do dono da metodologia: CTA sem ponte).
- "C": bloco de CTA (mínimo `cta_min_s`, teto de aviso `cta_max_s`).

Duas formas de uso:
1. `planejar(tipos, pps, aceleracao)`: monta a peça com o MÍNIMO de
   palavras de cada bloco (o pior caso mais compacto) e simula a linha do
   tempo e a densidade de insert por janela nesse mínimo.
2. `planejar(tipos, pps, aceleracao, palavras=[...])`: simula um roteiro
   JÁ CONTADO (sem escrever o pacote inteiro), pros mesmos números que o
   gate mediria depois.

Reaproveita `leitura.Bloco` e a mesma função de sobreposição de janela do
gate (`regras.roteiro._tempo_de_insert_na_janela`), pra dar exatamente o
número que o gate mede depois, não uma reimplementação paralela que possa
divergir.

Compatibilidade: Python 3.9 (sem `X | None`; `from __future__ import
annotations` mais `Optional[X]`).
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence, Tuple

from .leitura import Bloco
from .limiares import LIMIARES
from .regras.roteiro import _tempo_de_insert_na_janela

TIPOS_VALIDOS = ("I", "L", "LC", "A", "P", "C")

_NOMES_TIPO = {
    "I": "insert",
    "L": "lettering em placa",
    "LC": "lettering em coluna/carimbo",
    "A": "apresentador sozinho (sem KEY)",
    "P": "ponte (apresentador sozinho, liga o corpo ao CTA)",
    "C": "CTA",
}

# Tipos que valem como "tem ponte" imediatamente antes do "C": um bloco de
# ponte propriamente dito, ou um insert (a fala da ponte pode vir junto com
# o insert, como em agenda_cheia_v2 bloco 5).
_TIPOS_QUE_CONTAM_COMO_PONTE = ("P", "I")


def validar_tipos(tipos: Sequence[str]) -> List[str]:
    """Levanta `ValueError` (mensagem em PT-BR, acionável) se algum tipo
    não estiver em `TIPOS_VALIDOS`."""
    invalidos = [t for t in tipos if t not in TIPOS_VALIDOS]
    if invalidos:
        raise ValueError(
            "tipo de bloco invalido: " + ", ".join(sorted(set(invalidos)))
            + ". Faça: use só I, L, LC, A, P ou C em --blocos"
        )
    return list(tipos)


def checar_ponte_do_plano(tipos: Sequence[str]) -> List[str]:
    """Avisa quando o bloco logo antes de um "C" não é "P" nem "I" (regra
    do dono da metodologia: CTA sem ponte)."""
    avisos: List[str] = []
    for i, tipo in enumerate(tipos):
        if tipo != "C":
            continue
        anterior = tipos[i - 1] if i > 0 else None
        if anterior not in _TIPOS_QUE_CONTAM_COMO_PONTE:
            avisos.append(
                "plano sem ponte antes do CTA (bloco " + str(i + 1) + "). Faça: use P "
                "(bloco de ponte) ou I (insert com a fala da ponte) imediatamente antes do C"
            )
    return avisos


def _minimo_segundos(tipo: str, limiares: Dict[str, Any]) -> float:
    if tipo == "I":
        return float(limiares["insert_min_s"])
    if tipo == "L":
        return limiares["lettering_permanencia_min_ms"]["placa"] / 1000.0
    if tipo == "LC":
        perm = limiares["lettering_permanencia_min_ms"]
        return max(perm["coluna"], perm["carimbo"]) / 1000.0
    if tipo == "C":
        return float(limiares["cta_min_s"])
    return 0.0  # "A"/"P": sem minimo proprio


def _maximo_segundos(tipo: str, limiares: Dict[str, Any]) -> Optional[float]:
    if tipo in ("A", "P"):
        return float(limiares["retencao_avatar_sozinho_max_s"])
    if tipo == "C":
        return float(limiares["cta_max_s"])  # teto de aviso, nao reprovacao
    return None


def min_palavras_do_tipo(tipo: str, pps: float, aceleracao: float, limiares: Dict[str, Any] = LIMIARES) -> int:
    segundos = _minimo_segundos(tipo, limiares)
    if segundos <= 0:
        return 0
    return math.ceil(segundos * pps * aceleracao)


def max_palavras_do_tipo(tipo: str, pps: float, aceleracao: float, limiares: Dict[str, Any] = LIMIARES) -> int:
    teto_frase = int(limiares["frase_max_palavras"])
    segundos = _maximo_segundos(tipo, limiares)
    if segundos is None:
        return teto_frase
    return min(teto_frase, math.floor(segundos * pps * aceleracao))


@dataclass
class LinhaPlano:
    indice: int
    tipo: str
    min_palavras: int
    max_palavras: int
    palavras: int
    min_s: float
    max_s: Optional[float]


def _simular(tipos: Sequence[str], palavras: Sequence[int], pps: float, aceleracao: float) -> List[Bloco]:
    blocos: List[Bloco] = []
    inicio = 0.0
    for i, (tipo, n_palavras) in enumerate(zip(tipos, palavras), start=1):
        natural = n_palavras / pps if pps else 0.0
        final = natural / aceleracao if aceleracao else 0.0
        blocos.append(
            Bloco(
                numero=i,
                linha_original="",
                direcao="",
                fala="",
                ancora=("insert planejado bloco " + str(i)) if tipo == "I" else None,
                lead=None,
                chave="KEY PLANEJADO" if tipo in ("L", "LC", "C") else None,
                palavras=n_palavras,
                duracao_natural=natural,
                duracao_final=final,
                inicio_final=inicio,
            )
        )
        inicio += final
    return blocos


def calcular_densidade(blocos: Sequence[Bloco], limiares: Dict[str, Any] = LIMIARES) -> Dict[str, Dict[str, Any]]:
    """Densidade de insert por janela (mesma conta de
    `regras.roteiro.checar_densidade_insert`): fração de tempo com insert
    nas janelas 'corpo' e 'fecho', mais a sugestão quando sai da faixa."""
    total_final = sum(b.duracao_final for b in blocos)
    minimo = limiares["retencao_densidade_insert_min"]
    maximo = limiares["retencao_densidade_insert_max"]
    corpo_ini = limiares["retencao_janela_corpo_ini_s"]
    corpo_fim = limiares["retencao_janela_corpo_fim_s"]
    fecho_ini = limiares["retencao_janela_fecho_ini_s"]

    janelas: List[Tuple[str, float, float]] = []
    if total_final > corpo_ini:
        janelas.append(("corpo", corpo_ini, min(corpo_fim, total_final)))
    if total_final > fecho_ini:
        janelas.append(("fecho", fecho_ini, total_final))

    resultado: Dict[str, Dict[str, Any]] = {}
    for nome, ini, fim in janelas:
        duracao_janela = fim - ini
        if duracao_janela <= 0:
            continue
        tempo_insert = _tempo_de_insert_na_janela(blocos, ini, fim)
        fracao = tempo_insert / duracao_janela
        entrada: Dict[str, Any] = {"fracao": fracao, "ini_s": ini, "fim_s": fim}
        if fracao > maximo:
            entrada["sugestao"] = (
                "tire um insert do " + nome
                + "; alvo %.0f%% a %.0f%%" % (minimo * 100, maximo * 100)
            )
        elif fracao < minimo:
            inserts_na_janela = [
                b.numero for b in blocos
                if b.e_insert and min(b.inicio_final + b.duracao_final, fim) > max(b.inicio_final, ini)
            ]
            if len(inserts_na_janela) >= 2:
                entrada["sugestao"] = (
                    "intercale um bloco A entre os inserts " + str(inserts_na_janela[0])
                    + " e " + str(inserts_na_janela[1])
                    + "; alvo %.0f%% a %.0f%%" % (minimo * 100, maximo * 100)
                )
            else:
                entrada["sugestao"] = (
                    "adicione ou alongue um insert no " + nome
                    + "; alvo %.0f%% a %.0f%%" % (minimo * 100, maximo * 100)
                )
        resultado[nome] = entrada
    return resultado


def planejar(
    tipos: Sequence[str],
    pps: float = 2.9,
    aceleracao: float = 1.45,
    palavras: Optional[Sequence[int]] = None,
    alvo_s: Optional[float] = None,
    limiares: Dict[str, Any] = LIMIARES,
) -> Dict[str, Any]:
    """Monta o plano de bloco a bloco (mínimo/máximo de palavras) e simula
    a linha do tempo: com `palavras` (roteiro já contado) ou, sem ela, com
    o MÍNIMO de cada bloco (pior caso mais compacto)."""
    tipos = validar_tipos(tipos)
    if palavras is not None and len(palavras) != len(tipos):
        raise ValueError(
            "quantidade de --palavras (" + str(len(palavras)) + ") diferente da "
            "quantidade de --blocos (" + str(len(tipos)) + "). Faça: passe uma "
            "contagem de palavras para cada bloco do plano"
        )

    linhas: List[LinhaPlano] = []
    for i, tipo in enumerate(tipos, start=1):
        min_p = min_palavras_do_tipo(tipo, pps, aceleracao, limiares)
        max_p = max_palavras_do_tipo(tipo, pps, aceleracao, limiares)
        usada = palavras[i - 1] if palavras is not None else min_p
        linhas.append(
            LinhaPlano(
                indice=i,
                tipo=tipo,
                min_palavras=min_p,
                max_palavras=max_p,
                palavras=usada,
                min_s=_minimo_segundos(tipo, limiares),
                max_s=_maximo_segundos(tipo, limiares),
            )
        )

    soma_min_palavras = sum(l.min_palavras for l in linhas)
    soma_max_palavras = sum(l.max_palavras for l in linhas)
    soma_min_s = sum(l.min_palavras / pps / aceleracao for l in linhas)
    soma_max_s = sum(l.max_palavras / pps / aceleracao for l in linhas)

    palavras_simulacao = [l.palavras for l in linhas]
    blocos_simulados = _simular(tipos, palavras_simulacao, pps, aceleracao)
    total_final_s = sum(b.duracao_final for b in blocos_simulados)
    densidade = calcular_densidade(blocos_simulados, limiares)

    alvo_cabe: Optional[bool] = None
    if alvo_s is not None:
        alvo_cabe = soma_min_s <= alvo_s <= soma_max_s

    avisos_plano = checar_ponte_do_plano(tipos)

    return {
        "linhas": linhas,
        "soma_min_palavras": soma_min_palavras,
        "soma_max_palavras": soma_max_palavras,
        "soma_min_s": soma_min_s,
        "soma_max_s": soma_max_s,
        "alvo_s": alvo_s,
        "alvo_cabe": alvo_cabe,
        "blocos_simulados": blocos_simulados,
        "total_final_s": total_final_s,
        "densidade": densidade,
        "usando_palavras_informadas": palavras is not None,
        "avisos_plano": avisos_plano,
    }


def formatar_relatorio(resultado: Dict[str, Any]) -> str:
    """Texto pronto pra CLI (`planejar_blocos.py`), em PT-BR."""
    linhas_txt: List[str] = []
    if resultado.get("avisos_plano"):
        linhas_txt.append("AVISOS DO PLANO:")
        for aviso in resultado["avisos_plano"]:
            linhas_txt.append("  - " + aviso)
        linhas_txt.append("")
    linhas_txt.append("PLANO POR BLOCO:")
    for l in resultado["linhas"]:
        nome_tipo = _NOMES_TIPO.get(l.tipo, l.tipo)
        linhas_txt.append(
            "  bloco %d (%s, %s): min %d palavras, max %d palavras (usado nesta simulação: %d)"
            % (l.indice, l.tipo, nome_tipo, l.min_palavras, l.max_palavras, l.palavras)
        )

    linhas_txt.append("")
    linhas_txt.append(
        "SOMA: min %d palavras (%.2fs finais), max %d palavras (%.2fs finais)"
        % (
            resultado["soma_min_palavras"], resultado["soma_min_s"],
            resultado["soma_max_palavras"], resultado["soma_max_s"],
        )
    )
    if resultado["alvo_s"] is not None:
        veredito = "cabe" if resultado["alvo_cabe"] else "não cabe"
        linhas_txt.append(
            "ALVO: %.2fs %s na faixa mín/máx da peça (%.2fs a %.2fs)"
            % (resultado["alvo_s"], veredito, resultado["soma_min_s"], resultado["soma_max_s"])
        )

    linhas_txt.append("")
    origem = "roteiro já contado (--palavras)" if resultado["usando_palavras_informadas"] else "mínimo de cada bloco"
    linhas_txt.append("SIMULAÇÃO (" + origem + "), início de cada bloco em segundos finais:")
    for b in resultado["blocos_simulados"]:
        linhas_txt.append(
            "  bloco %d: início %.2fs, duração %.2fs (%d palavras)"
            % (b.numero, b.inicio_final, b.duracao_final, b.palavras)
        )
    linhas_txt.append("  duração total final: %.2fs" % resultado["total_final_s"])

    linhas_txt.append("")
    linhas_txt.append("DENSIDADE DE INSERT POR JANELA:")
    if not resultado["densidade"]:
        linhas_txt.append("  peça curta demais pra ter janela corpo/fecho medida")
    for nome, dados in resultado["densidade"].items():
        base = "  %s (%.1fs a %.1fs): %.0f%%" % (nome, dados["ini_s"], dados["fim_s"], dados["fracao"] * 100)
        if "sugestao" in dados:
            base += ". Faça: " + dados["sugestao"]
        linhas_txt.append(base)

    return "\n".join(linhas_txt)
