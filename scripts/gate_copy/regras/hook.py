#!/usr/bin/env python3
"""Regras do hook: bloco 1 do roteiro (requisito 7) e hooks.md inteiro
(requisito 7): 3 hooks distintos, id de tática válido, cluster batendo com
a tabela e liberado pro objetivo (R1.4), hook cru com lettering: nenhum
(R1.5), tamanho máximo de fala (R1.2), ausência de frase de apresentação
(R2.7), âncora do problema/promessa nas primeiras palavras (R2.6) e Hook A
igual ao bloco 1.

Compatibilidade: Python 3.9 (sem `X | None`; `from __future__ import
annotations` mais `Optional[X]`).
"""

from __future__ import annotations

import math
from typing import List, Optional, Sequence

from ..achados import REPROVACAO, Achado
from ..leitura import Bloco, Conceito, Hook
from ..limiares import CLUSTERS_LIBERADOS, LIMIARES, TATICAS_EMBUTIDAS
from ..texto import REGEX_APRESENTACAO, indice_sublista, normalizar, normalizar_codigo, palavras_normalizadas

def checar_hook(conceito: Conceito, blocos: Sequence[Bloco]) -> List[Achado]:
    """Requisito 7 (bloco 1 = hook A): âncora do problema/promessa nas
    primeiras palavras e frase de apresentação (R2.6/R2.7)."""
    achados: List[Achado] = []
    if not blocos:
        return achados
    bloco1 = blocos[0]
    limite_indice = math.ceil(LIMIARES["hook_problema_nomeado_ate_s"] * conceito.pps)
    if REGEX_APRESENTACAO.search(normalizar(bloco1.fala)):
        achados.append(
            Achado(
                REPROVACAO,
                "roteiro bloco 1",
                "frase de apresentação no hook (R2.7)",
                medido=bloco1.fala,
                limiar="sem 'eu sou o', 'meu nome é', 'aqui é o'",
            )
        )
    return achados


def _checar_ancora_de_hook(onde: str, ancora: str, fala: str, limite_indice: int) -> List[Achado]:
    achados: List[Achado] = []
    fala_p = palavras_normalizadas(fala)
    ancora_p = palavras_normalizadas(ancora)
    idx = indice_sublista(fala_p, ancora_p) if ancora_p else None
    if not ancora_p or idx is None or idx >= limite_indice:
        achados.append(
            Achado(
                REPROVACAO,
                onde,
                "âncora do problema/promessa fora das primeiras palavras (R2.6)",
                medido=("não encontrada" if idx is None else "indice " + str(idx)) + ": " + repr(ancora),
                limiar="indice < " + str(limite_indice),
            )
        )
    return achados


def checar_hooks_md(
    conceito: Conceito,
    blocos: Sequence[Bloco],
    hooks: Sequence[Hook],
    taticas: Optional[Sequence[dict]] = None,
) -> List[Achado]:
    """Requisito 7: hooks.md inteiro (seção 3).

    `taticas` sobrescreve o catálogo embutido de 29 táticas quando a CLI
    carrega o `taticas_hook.yaml` real da esteira (`--taticas` ou o padrão
    em `~/creative-studio/config/taticas_hook.yaml`); ausente ou vazio, cai
    no catálogo embutido (`TATICAS_EMBUTIDAS`)."""
    achados: List[Achado] = []
    limite_indice = math.ceil(LIMIARES["hook_problema_nomeado_ate_s"] * conceito.pps)
    limite_palavras = math.floor(LIMIARES["diversidade_hook_fala_max_s"] * conceito.pps)

    if len(hooks) != 3:
        achados.append(
            Achado(
                REPROVACAO,
                "hooks.md",
                "esperados 3 hooks (R1.2 a R1.5), regra 3-2-2 do Leo",
                medido=str(len(hooks)),
                limiar="3",
            )
        )

    ids_vistos: List[str] = []
    tem_cru = False
    catalogo = taticas if taticas else TATICAS_EMBUTIDAS
    ids_validos = {t["id"] for t in catalogo}
    clusters_por_id = {t["id"]: t["cluster"] for t in catalogo}
    liberados = CLUSTERS_LIBERADOS.get(conceito.objetivo, set())

    for hook in hooks:
        onde = hook.nome
        hook_id = normalizar_codigo(hook.get("id"))
        if hook_id:
            ids_vistos.append(hook_id)
        if hook_id and hook_id not in ids_validos:
            achados.append(
                Achado(
                    REPROVACAO, onde, "id de tática inexistente nas 29 (seção 3)",
                    medido=hook_id, limiar="id da lista embutida/taticas_hook.yaml",
                )
            )
        cluster = normalizar_codigo(hook.get("cluster"))
        if hook_id in clusters_por_id and cluster and cluster != clusters_por_id[hook_id]:
            achados.append(
                Achado(
                    REPROVACAO, onde, "cluster não bate com o da tabela de táticas",
                    medido=cluster, limiar=clusters_por_id[hook_id],
                )
            )
        if cluster and liberados and cluster not in liberados:
            achados.append(
                Achado(
                    REPROVACAO, onde,
                    "cluster fora do objetivo " + conceito.objetivo + " (R1.4)",
                    medido=cluster, limiar="um de: " + ", ".join(sorted(liberados)),
                )
            )

        if hook.cru:
            tem_cru = True
            lettering = normalizar_codigo(hook.get("lettering"))
            if lettering != "nenhum":
                achados.append(
                    Achado(
                        REPROVACAO, onde, "hook cru precisa de lettering: nenhum",
                        medido=hook.get("lettering"), limiar="nenhum",
                    )
                )

        fala = hook.fala
        n_palavras = len(fala.split())
        if n_palavras > limite_palavras:
            achados.append(
                Achado(
                    REPROVACAO, onde,
                    "fala do hook acima do máximo de " + str(limite_palavras) + " palavras (R1.2)",
                    medido=str(n_palavras), limiar="<= " + str(limite_palavras),
                )
            )
        if REGEX_APRESENTACAO.search(normalizar(fala)):
            achados.append(
                Achado(REPROVACAO, onde, "frase de apresentação no hook (R2.7)", medido=fala)
            )

        ancora = hook.get("ancora")
        achados.extend(_checar_ancora_de_hook(onde, ancora, fala, limite_indice))

        if normalizar(hook.nome) == "hook a" and blocos:
            if normalizar(fala) != normalizar(blocos[0].fala):
                achados.append(
                    Achado(
                        REPROVACAO, onde,
                        "Hook A tem que ter a MESMA fala do bloco 1 do roteiro",
                        medido=fala, limiar=blocos[0].fala,
                    )
                )

    if ids_vistos and len(set(ids_vistos)) != len(ids_vistos):
        achados.append(
            Achado(REPROVACAO, "hooks.md", "ids de hook repetidos, têm que ser distintos", medido=str(ids_vistos))
        )
    if hooks and not tem_cru:
        achados.append(
            Achado(REPROVACAO, "hooks.md", "nenhum hook cru: sim (R1.5)", limiar="ao menos 1")
        )
    return achados

