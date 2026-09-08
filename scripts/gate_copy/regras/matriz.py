#!/usr/bin/env python3
"""Regra da matriz (requisito 12, seção 8): 12 linhas, nome da peça no
padrão `{conceito}_{canal}_{formato}_{hook}_{legenda}_v{n}` (legenda em
`[a-z0-9_-]+`), conjunto de hooks igual ao de hooks.md, exatamente 2
legendas e 2 formatos distintos e ao menos um formato sem avatar em tela
(R7.1).

Compatibilidade: Python 3.9 (sem `X | None`; `from __future__ import
annotations` mais `Optional[X]`).
"""

from __future__ import annotations

import re
from typing import Any, Dict, List, Sequence

from ..achados import REPROVACAO, Achado
from ..leitura import Conceito, Hook, MatrizLinha
from ..limiares import FORMATOS_EMBUTIDOS
from ..texto import normalizar_codigo

# Padrão aceito pro segmento livre de legenda (e implicitamente pro id do
# conceito, que entra no nome literal): letras minúsculas, dígitos,
# underscore e hífen.
_PADRAO_LEGENDA = r"[a-z0-9_-]+"


def checar_matriz(conceito: Conceito, hooks: Sequence[Hook], campos: Dict[str, Any], pecas: Sequence[MatrizLinha]) -> List[Achado]:
    """Requisito 12, seção 8."""
    achados: List[Achado] = []
    if len(pecas) != 12:
        achados.append(
            Achado(
                REPROVACAO, "matriz.md", "esperadas 12 linhas (R7.1)",
                acao="complete a tabela de matriz.md até ter 12 linhas",
                medido=str(len(pecas)), limiar="12",
            )
        )

    hooks_ids = {normalizar_codigo(h.get("id")) for h in hooks if h.get("id")}
    formatos_ids = "|".join(re.escape(f["id"]) for f in FORMATOS_EMBUTIDOS)
    hooks_ids_regex = "|".join(re.escape(h) for h in hooks_ids) if hooks_ids else "a^"
    conceito_id = re.escape(normalizar_codigo(conceito.get("conceito", "")) or conceito.get("conceito", ""))
    canal = re.escape(str(conceito.get("canal", "")))
    padrao = re.compile(
        "^" + conceito_id + "_" + canal + "_(" + formatos_ids + ")_(" + hooks_ids_regex + ")_(" + _PADRAO_LEGENDA + ")_v\\d+$"
    )

    hooks_na_matriz = set()
    formatos_na_matriz = set()
    legendas_na_matriz = set()
    tem_sem_avatar = False

    dict_formatos = {f["id"]: f["avatar_em_tela"] for f in FORMATOS_EMBUTIDOS}

    for linha in pecas:
        onde = "matriz.md #" + linha.numero
        peca_norm = normalizar_codigo(linha.peca)
        if not padrao.match(peca_norm):
            achados.append(
                Achado(
                    REPROVACAO, onde,
                    "nome da peca fora do padrao {conceito}_{canal}_{formato}_{hook}_{legenda}_v{n} "
                    "(legenda e conceito aceitam " + _PADRAO_LEGENDA + ")",
                    acao="renomeie a peça pro padrão {conceito}_{canal}_{formato}_{hook}_{legenda}_v{n}",
                    medido=linha.peca,
                )
            )
        hooks_na_matriz.add(normalizar_codigo(linha.hook))
        formatos_na_matriz.add(normalizar_codigo(linha.formato))
        legendas_na_matriz.add(normalizar_codigo(linha.legenda))
        if dict_formatos.get(normalizar_codigo(linha.formato)) is False:
            tem_sem_avatar = True

    if hooks_ids and hooks_na_matriz and hooks_na_matriz != hooks_ids:
        achados.append(
            Achado(
                REPROVACAO, "matriz.md", "conjunto de hooks da matriz diferente dos ids de hooks.md",
                acao="ajuste a coluna hook da matriz pra usar só os ids declarados em hooks.md",
                medido=str(sorted(hooks_na_matriz)), limiar=str(sorted(hooks_ids)),
            )
        )
    if len(legendas_na_matriz) != 2:
        achados.append(
            Achado(
                REPROVACAO, "matriz.md", "esperadas 2 legendas distintas",
                acao="ajuste a matriz pra ter exatamente 2 legendas distintas",
                medido=str(sorted(legendas_na_matriz)),
            )
        )
    if len(formatos_na_matriz) != 2:
        achados.append(
            Achado(
                REPROVACAO, "matriz.md", "esperados 2 formatos distintos",
                acao="ajuste a matriz pra ter exatamente 2 formatos distintos",
                medido=str(sorted(formatos_na_matriz)),
            )
        )
    if pecas and not tem_sem_avatar:
        achados.append(
            Achado(
                REPROVACAO, "matriz.md", "nenhum formato sem avatar em tela (R7.1)",
                acao="troque um dos 2 formatos por um sem avatar em tela (sem_avatar, noticia ou alerta)",
            )
        )
    return achados
