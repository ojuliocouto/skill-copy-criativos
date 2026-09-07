#!/usr/bin/env python3
"""Regra de assets (requisito 11, seção 7): toda âncora de insert do
roteiro com linha em assets.md, enquadramento e origem dentro do domínio,
origem `criar:*` exigindo referência com 5+ palavras (e avisando pra
propor ao Júlio antes, decisão 34), e `serve: não` exigindo ressalva
(decisão 35).

Compatibilidade: Python 3.9 (sem `X | None`; `from __future__ import
annotations` mais `Optional[X]`).
"""

from __future__ import annotations

from typing import List, Sequence

from ..achados import AVISO, REPROVACAO, Achado
from ..leitura import AssetLinha, Bloco
from ..limiares import ENQUADRAMENTOS_ASSET, ORIGENS_ASSET_CRIAR, ORIGENS_ASSET_FIXAS
from ..texto import normalizar

def checar_assets(blocos: Sequence[Bloco], assets: Sequence[AssetLinha]) -> List[Achado]:
    """Requisito 11, seção 7."""
    achados: List[Achado] = []
    ancoras_roteiro = {normalizar(b.ancora): b.ancora for b in blocos if b.e_insert}
    ancoras_assets = {normalizar(a.ancora): a for a in assets}

    for norm, original in ancoras_roteiro.items():
        if norm not in ancoras_assets:
            achados.append(Achado(REPROVACAO, "assets.md", "sem linha para a âncora do roteiro", medido=original))

    for norm, linha in ancoras_assets.items():
        onde = "assets.md #" + linha.numero
        if norm not in ancoras_roteiro:
            achados.append(Achado(AVISO, onde, "linha sem bloco correspondente no roteiro", medido=linha.ancora))
        if linha.enquadramento not in ENQUADRAMENTOS_ASSET:
            achados.append(Achado(REPROVACAO, onde, "enquadramento fora do domínio", medido=linha.enquadramento, limiar=str(sorted(ENQUADRAMENTOS_ASSET))))
        if linha.origem not in ORIGENS_ASSET_FIXAS and linha.origem not in ORIGENS_ASSET_CRIAR:
            achados.append(Achado(REPROVACAO, onde, "origem fora do domínio", medido=linha.origem))
        if linha.origem in ORIGENS_ASSET_CRIAR:
            if len((linha.referencia or "").split()) < 5:
                achados.append(Achado(REPROVACAO, onde, "origem criar: exige referência com 5+ palavras", medido=linha.referencia))
            else:
                achados.append(Achado(AVISO, onde, "criação própria: propor ao Júlio antes (decisão 34)", medido=linha.origem))
        if linha.serve not in ("sim", "nao"):
            achados.append(Achado(REPROVACAO, onde, "serve fora do domínio sim/não", medido=linha.serve))
        elif linha.serve == "nao" and not linha.ressalva.strip():
            achados.append(Achado(REPROVACAO, onde, "serve: não sem ressalva (decisão 35)"))
    return achados

