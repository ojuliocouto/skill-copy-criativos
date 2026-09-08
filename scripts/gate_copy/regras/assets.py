#!/usr/bin/env python3
"""Regra de assets (requisito 11, seção 7): toda âncora de insert do
roteiro com linha em assets.md, enquadramento e origem dentro do domínio
(origem com sufixo `:imagem`, ex. `drive:imagem`, avisa que é imagem
parada), origem `criar:*` exigindo referência com 5+ palavras (e avisando
pra propor ao cliente antes de produzir, decisão 34), e `serve: não`
exigindo ressalva (decisão 35).

Compatibilidade: Python 3.9 (sem `X | None`; `from __future__ import
annotations` mais `Optional[X]`).
"""

from __future__ import annotations

from typing import List, Sequence

from ..achados import AVISO, REPROVACAO, Achado
from ..leitura import AssetLinha, Bloco
from ..limiares import ENQUADRAMENTOS_ASSET, ORIGENS_ASSET_CRIAR, ORIGENS_ASSET_FIXAS
from ..texto import normalizar

_SUFIXO_IMAGEM = ":imagem"


def _origem_valida(origem: str) -> bool:
    if origem in ORIGENS_ASSET_FIXAS or origem in ORIGENS_ASSET_CRIAR:
        return True
    if origem.endswith(_SUFIXO_IMAGEM):
        base = origem[: -len(_SUFIXO_IMAGEM)]
        return base in ORIGENS_ASSET_FIXAS
    return False


def checar_assets(blocos: Sequence[Bloco], assets: Sequence[AssetLinha]) -> List[Achado]:
    """Requisito 11, seção 7."""
    achados: List[Achado] = []
    ancoras_roteiro = {normalizar(b.ancora): b.ancora for b in blocos if b.e_insert}
    ancoras_assets = {normalizar(a.ancora): a for a in assets}

    for norm, original in ancoras_roteiro.items():
        if norm not in ancoras_assets:
            achados.append(
                Achado(
                    REPROVACAO, "assets.md", "sem linha para a âncora do roteiro",
                    acao="adicione uma linha em assets.md para essa âncora",
                    medido=original,
                )
            )

    for norm, linha in ancoras_assets.items():
        onde = "assets.md #" + linha.numero
        if norm not in ancoras_roteiro:
            achados.append(
                Achado(
                    AVISO, onde, "linha sem bloco correspondente no roteiro",
                    acao="apague a linha ou corrija a âncora pra bater com um bloco do roteiro",
                    medido=linha.ancora,
                )
            )
        if linha.enquadramento not in ENQUADRAMENTOS_ASSET:
            achados.append(
                Achado(
                    REPROVACAO, onde, "enquadramento fora do domínio",
                    acao="troque o enquadramento por um do domínio aceito",
                    medido=linha.enquadramento, limiar=str(sorted(ENQUADRAMENTOS_ASSET)),
                )
            )
        if linha.origem.endswith(_SUFIXO_IMAGEM) and _origem_valida(linha.origem):
            achados.append(
                Achado(
                    AVISO, onde, "asset é imagem parada: a esteira precisa dar movimento (pan ou zoom leve)",
                    acao="peça pan ou zoom leve na esteira pra este asset não ficar estático",
                    medido=linha.origem,
                )
            )
        if not _origem_valida(linha.origem):
            achados.append(
                Achado(
                    REPROVACAO, onde, "origem fora do domínio",
                    acao="troque a origem por uma do domínio aceito",
                    medido=linha.origem,
                )
            )
        if linha.origem in ORIGENS_ASSET_CRIAR:
            if len((linha.referencia or "").split()) < 5:
                achados.append(
                    Achado(
                        REPROVACAO, onde, "origem criar: exige referência com 5+ palavras",
                        acao="descreva a referência com pelo menos 5 palavras",
                        medido=linha.referencia,
                    )
                )
            else:
                achados.append(
                    Achado(
                        AVISO, onde, "criação própria: propor ao cliente antes de produzir (decisão 34)",
                        acao="proponha o asset ao cliente antes de mandar produzir",
                        medido=linha.origem,
                    )
                )
        if linha.serve not in ("sim", "nao"):
            achados.append(
                Achado(
                    REPROVACAO, onde, "serve fora do domínio sim/não",
                    acao="preencha serve com sim ou não",
                    medido=linha.serve,
                )
            )
        elif linha.serve == "nao" and not linha.ressalva.strip():
            achados.append(
                Achado(
                    REPROVACAO, onde, "serve: não sem ressalva (decisão 35)",
                    acao="preencha a coluna ressalva explicando o porquê de serve: não",
                )
            )
    return achados
