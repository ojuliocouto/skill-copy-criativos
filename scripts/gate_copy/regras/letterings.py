#!/usr/bin/env python3
"""Regra de letterings (requisito 8, seção 5): LEAD/KEY da tabela batendo
com o roteiro, palavras do KEY presentes na fala, limite de palavras de
conteúdo do KEY, LEAD com até 4 palavras, forma dentro do domínio e
rodízio de forma entre blocos vizinhos.

Compatibilidade: Python 3.9 (sem `X | None`; `from __future__ import
annotations` mais `Optional[X]`).
"""

from __future__ import annotations

from typing import Dict, List, Optional, Sequence

from ..achados import AVISO, REPROVACAO, Achado
from ..leitura import Bloco, Cta, LetteringLinha
from ..limiares import FORMAS_LETTERING
from ..texto import (
    contar_palavras_de_conteudo_do_key,
    normalizar,
    normalizar_codigo,
    palavras_normalizadas,
    todas_palavras_na_fala,
)

def checar_letterings(
    blocos: Sequence[Bloco], letterings: Sequence[LetteringLinha], cta: Optional[Cta]
) -> List[Achado]:
    """Requisito 8, seção 5."""
    achados: List[Achado] = []
    por_bloco = {b.numero: b for b in blocos}
    letterings_por_bloco = {l.bloco: l for l in letterings}
    ultimo_bloco_numero = blocos[-1].numero if blocos else None
    cta_tipo = normalizar_codigo(cta.get("tipo")) if cta else ""

    formas_por_bloco: Dict[int, str] = {}

    for bloco in blocos:
        if not bloco.chave:
            continue
        onde = "roteiro/letterings bloco " + str(bloco.numero)
        linha = letterings_por_bloco.get(bloco.numero)
        if linha is None:
            achados.append(
                Achado(REPROVACAO, onde, "bloco com KEY no roteiro sem linha em letterings.md")
            )
            continue
        if normalizar(linha.lead) != normalizar(bloco.lead or ""):
            achados.append(
                Achado(
                    REPROVACAO, onde, "LEAD da tabela diferente do LEAD do roteiro",
                    medido=linha.lead, limiar=bloco.lead or "",
                )
            )
        if normalizar(linha.key) != normalizar(bloco.chave or ""):
            achados.append(
                Achado(
                    REPROVACAO, onde, "KEY da tabela diferente do KEY do roteiro",
                    medido=linha.key, limiar=bloco.chave or "",
                )
            )

        fala_p = palavras_normalizadas(bloco.fala)
        faltando = todas_palavras_na_fala(bloco.chave, fala_p)
        if faltando:
            achados.append(
                Achado(
                    REPROVACAO, onde, "palavra do KEY não está na fala do bloco",
                    medido=str(faltando), limiar="todas as palavras do KEY na fala",
                )
            )

        max_palavras_key = 3 if (bloco.numero == ultimo_bloco_numero and cta_tipo == "cta") else 2
        n_conteudo = contar_palavras_de_conteudo_do_key(bloco.chave)
        if n_conteudo > max_palavras_key:
            achados.append(
                Achado(
                    REPROVACAO, onde,
                    "KEY com mais palavras de conteúdo que o permitido (algarismo e "
                    "palavra funcional não contam, seção 5)",
                    medido=str(n_conteudo), limiar="<= " + str(max_palavras_key),
                )
            )

        if bloco.lead:
            n_lead = len(bloco.lead.split())
            if n_lead > 4:
                achados.append(
                    Achado(REPROVACAO, onde, "LEAD com mais de 4 palavras", medido=str(n_lead), limiar="<= 4")
                )
            lead_faltando = todas_palavras_na_fala(bloco.lead, fala_p)
            if lead_faltando:
                achados.append(
                    Achado(AVISO, onde, "palavra do LEAD fora da fala", medido=str(lead_faltando))
                )

        forma = linha.forma
        if forma == "placa":
            achados.append(
                Achado(
                    REPROVACAO,
                    onde,
                    "forma 'placa' sozinha não é válida: declare h1, h2 ou h4",
                    medido=forma,
                    limiar="placa_h1, placa_h2 ou placa_h4",
                )
            )
        elif forma not in FORMAS_LETTERING:
            achados.append(
                Achado(REPROVACAO, onde, "forma de lettering fora do domínio", medido=forma, limiar=str(sorted(FORMAS_LETTERING)))
            )
        else:
            formas_por_bloco[bloco.numero] = forma
            if forma == "carimbo" and not bloco.e_insert:
                achados.append(
                    Achado(
                        AVISO,
                        onde,
                        "carimbo é lettering de apoio, só em bloco com insert",
                        medido=forma,
                    )
                )

    ordenados = sorted(formas_por_bloco.items())
    for (num_a, forma_a), (num_b, forma_b) in zip(ordenados, ordenados[1:]):
        if num_b - num_a == 1 and forma_a == forma_b and forma_a != "seta_cta":
            achados.append(
                Achado(
                    AVISO,
                    "letterings blocos " + str(num_a) + " e " + str(num_b),
                    "mesma forma de lettering em blocos vizinhos (rodízio, decisão 13)",
                    medido=forma_a,
                )
            )
    return achados

