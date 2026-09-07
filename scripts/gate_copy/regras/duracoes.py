#!/usr/bin/env python3
"""Regra de duração final por bloco (requisito 14, tabela da seção 9):
mínimo de insert, lettering (permanência + leitura extra por palavra) e
CTA (o maior dos que se aplicam ao bloco); máximo pro bloco sem insert e
sem KEY sozinho e para dois blocos vizinhos sem insert somados.

Compatibilidade: Python 3.9 (sem `X | None`; `from __future__ import
annotations` mais `Optional[X]`).
"""

from __future__ import annotations

import math
from typing import Dict, List, Optional, Sequence, Tuple

from ..achados import AVISO, REPROVACAO, Achado
from ..leitura import Bloco, Conceito, Cta, LetteringLinha
from ..limiares import CATEGORIA_PERMANENCIA_LETTERING, FORMAS_LETTERING, LIMIARES
from ..texto import contar_palavras_nao_numericas, normalizar_codigo

def _categoria_permanencia_do_bloco(bloco: Bloco, letterings_por_bloco: Dict[int, LetteringLinha]) -> str:
    """Categoria de permanência mínima (seção 9): as 3 placas (h1/h2/h4) usam
    a mesma permanencia_min_ms.placa; as demais formas usam a própria
    chave. Sem linha válida em letterings.md, cai na categoria "placa"
    (padrão quando ausente, requisito 14)."""
    linha = letterings_por_bloco.get(bloco.numero)
    if linha and linha.forma in FORMAS_LETTERING:
        return CATEGORIA_PERMANENCIA_LETTERING.get(linha.forma, "placa")
    return "placa"


def checar_duracoes(
    conceito: Conceito, blocos: Sequence[Bloco], letterings: Sequence[LetteringLinha], cta: Optional[Cta]
) -> List[Achado]:
    """Requisito 14, tabela da seção 9."""
    achados: List[Achado] = []
    letterings_por_bloco = {l.bloco: l for l in letterings}
    permanencias = LIMIARES["lettering_permanencia_min_ms"]
    extra_ms = LIMIARES["lettering_leitura_por_palavra_extra_ms"]
    graca = LIMIARES["lettering_palavras_de_graca"]
    ultimo_bloco_numero = blocos[-1].numero if blocos else None
    cta_tipo = normalizar_codigo(cta.get("tipo")) if cta else ""

    def palavras_faltando(minimo_final_s: float, palavras_atuais: int) -> int:
        minimo_palavras = math.ceil(minimo_final_s * conceito.aceleracao * conceito.pps)
        return max(0, minimo_palavras - palavras_atuais)

    for bloco in blocos:
        minimos: List[Tuple[str, float]] = []
        if bloco.e_insert:
            minimos.append(("insert", LIMIARES["insert_min_s"]))
        if bloco.chave:
            categoria = _categoria_permanencia_do_bloco(bloco, letterings_por_bloco)
            n_extra = max(0, contar_palavras_nao_numericas(bloco.chave) - graca)
            base_ms = permanencias.get(categoria, permanencias["placa"])
            minimo_ms = base_ms + n_extra * extra_ms
            minimos.append(("lettering " + categoria, minimo_ms / 1000.0))
        if bloco.numero == ultimo_bloco_numero and cta_tipo == "cta":
            minimos.append(("cta", LIMIARES["cta_min_s"]))

        if minimos:
            rotulo_min, minimo_s = max(minimos, key=lambda par: par[1])
            if bloco.duracao_final < minimo_s:
                faltam = palavras_faltando(minimo_s, bloco.palavras)
                achados.append(
                    Achado(
                        REPROVACAO,
                        "roteiro bloco " + str(bloco.numero),
                        "duração final abaixo do mínimo de " + rotulo_min,
                        medido="%.2fs (%d palavras)" % (bloco.duracao_final, bloco.palavras),
                        limiar="%.2fs; faltam %d palavras para fechar" % (minimo_s, faltam),
                    )
                )
        if bloco.numero == ultimo_bloco_numero and cta_tipo == "cta":
            teto = LIMIARES["cta_max_s"]
            if bloco.duracao_final > teto:
                achados.append(
                    Achado(
                        AVISO,
                        "roteiro bloco " + str(bloco.numero),
                        "duração final do CTA acima do teto (seção 6, fechamento.janela_final_max_s)",
                        medido="%.2fs" % bloco.duracao_final,
                        limiar="<= %.2fs" % teto,
                    )
                )

        if not minimos:
            maximo = LIMIARES["retencao_avatar_sozinho_max_s"]
            if bloco.duracao_final > maximo:
                achados.append(
                    Achado(
                        REPROVACAO,
                        "roteiro bloco " + str(bloco.numero),
                        "bloco sem insert e sem KEY acima do máximo (R3.3)",
                        medido="%.2fs" % bloco.duracao_final,
                        limiar="<= %.2fs" % maximo,
                    )
                )

    for a, b in zip(blocos, blocos[1:]):
        if not a.e_insert and not b.e_insert:
            soma = a.duracao_final + b.duracao_final
            maximo = LIMIARES["retencao_avatar_sozinho_max_s"]
            if soma > maximo:
                achados.append(
                    Achado(
                        AVISO,
                        "roteiro blocos " + str(a.numero) + " e " + str(b.numero),
                        "blocos vizinhos sem insert somam acima do máximo (R3.3)",
                        medido="%.2fs" % soma,
                        limiar="<= %.2fs" % maximo,
                    )
                )
    return achados

