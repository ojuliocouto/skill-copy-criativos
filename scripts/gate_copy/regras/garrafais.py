#!/usr/bin/env python3
"""Regra de garrafais (requisito 9, seção 4): total entre 2 e 3 (aviso com
1, reprovação acima de 3), até 2 no gancho, palavra e âncora presentes na
fala do bloco, garrafal não repetindo o KEY do mesmo bloco, só no bloco 1
quando o bloco tem insert e cor dentro do domínio.

Compatibilidade: Python 3.9 (sem `X | None`; `from __future__ import
annotations` mais `Optional[X]`).
"""

from __future__ import annotations

from typing import List, Sequence

from ..achados import AVISO, REPROVACAO, Achado
from ..leitura import Bloco, Garrafal
from ..limiares import CORES_GARRAFAL
from ..texto import contem_sublista, palavras_normalizadas, todas_palavras_na_fala

def checar_garrafais(blocos: Sequence[Bloco], garrafais: Sequence[Garrafal]) -> List[Achado]:
    """Requisito 9, seção 4."""
    achados: List[Achado] = []
    por_bloco = {b.numero: b for b in blocos}

    total = len(garrafais)
    if total == 1:
        achados.append(Achado(AVISO, "garrafais.md", "só 1 garrafal na peça", medido="1", limiar="2 ou 3"))
    elif total > 3:
        achados.append(Achado(REPROVACAO, "garrafais.md", "mais de 3 garrafais na peça", medido=str(total), limiar="<= 3"))

    no_gancho = [g for g in garrafais if g.bloco == 1]
    if len(no_gancho) > 2:
        achados.append(
            Achado(REPROVACAO, "garrafais.md bloco 1", "mais de 2 garrafais no gancho", medido=str(len(no_gancho)), limiar="<= 2")
        )

    for g in garrafais:
        onde = "garrafais.md " + g.nome
        bloco = por_bloco.get(g.bloco)
        if bloco is None:
            achados.append(Achado(REPROVACAO, onde, "bloco inexistente no roteiro", medido=str(g.bloco)))
            continue
        fala_p = palavras_normalizadas(bloco.fala)
        if todas_palavras_na_fala(g.palavra, fala_p):
            achados.append(Achado(REPROVACAO, onde, "palavra da garrafal não está na fala do bloco", medido=g.palavra))
        if not contem_sublista(fala_p, palavras_normalizadas(g.ancora)):
            achados.append(Achado(REPROVACAO, onde, "âncora da garrafal não está na fala do bloco", medido=g.ancora))
        if bloco.chave:
            palavras_key = set(palavras_normalizadas(bloco.chave))
            palavras_garrafal = set(palavras_normalizadas(g.palavra))
            if palavras_garrafal and palavras_garrafal.issubset(palavras_key):
                achados.append(Achado(REPROVACAO, onde, "garrafal repete o KEY do mesmo bloco", medido=g.palavra, limiar=bloco.chave))
        if g.bloco != 1 and (bloco.e_insert or bloco.chave):
            achados.append(
                Achado(
                    REPROVACAO,
                    onde,
                    "garrafal fora do bloco 1 precisa de apresentador sozinho (sem inserção de vídeo e sem KEY)",
                )
            )
        if g.cor not in CORES_GARRAFAL:
            achados.append(Achado(REPROVACAO, onde, "cor fora do domínio", medido=g.cor, limiar=str(sorted(CORES_GARRAFAL))))
    return achados

