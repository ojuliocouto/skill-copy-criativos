#!/usr/bin/env python3
"""Regra do CTA (requisito 10, seção 6): fala igual ao último bloco do
roteiro, tipo e verbo de ação exigidos no modo pago, escassez legítima
obrigatória em carrinho/lote e proibida em frio/captação, e as regras do
modo orgânico (loop, envio, pergunta).

Compatibilidade: Python 3.9 (sem `X | None`; `from __future__ import
annotations` mais `Optional[X]`).
"""

from __future__ import annotations

from typing import List, Sequence

from ..achados import REPROVACAO, Achado
from ..leitura import Bloco, Conceito, Cta
from ..limiares import VERBOS_DE_ACAO
from ..texto import (
    REGEX_DATA,
    REGEX_ESCASSEZ,
    REGEX_ORGANICO_ENVIO,
    REGEX_ORGANICO_PROIBIDO,
    REGEX_PRECO,
    normalizar,
    normalizar_codigo,
    palavras_normalizadas,
)

def checar_cta(conceito: Conceito, blocos: Sequence[Bloco], cta: Cta) -> List[Achado]:
    """Requisito 10, seção 6."""
    achados: List[Achado] = []
    if not blocos:
        return achados
    ultimo = blocos[-1]
    fala_cta = cta.get("fala")
    if normalizar(fala_cta) != normalizar(ultimo.fala):
        achados.append(
            Achado(REPROVACAO, "cta.md", "fala do CTA diferente da fala do último bloco do roteiro", medido=fala_cta, limiar=ultimo.fala)
        )
    fala_norm = normalizar(fala_cta)
    key_p = palavras_normalizadas(ultimo.chave) if ultimo.chave else []
    fala_p = palavras_normalizadas(fala_cta)
    modo = normalizar_codigo(conceito.modo)
    campanha = normalizar_codigo(conceito.campanha)
    tipo = normalizar_codigo(cta.get("tipo"))

    if modo == "pago":
        if tipo != "cta":
            achados.append(Achado(REPROVACAO, "cta.md", "modo pago exige tipo: cta", medido=tipo, limiar="cta"))
        tem_verbo = any(v in fala_p or v in key_p for v in VERBOS_DE_ACAO)
        if not tem_verbo:
            achados.append(Achado(REPROVACAO, "cta.md", "CTA vago: nenhum verbo de ação na fala nem no KEY (seção 6)"))
        tem_escassez = bool(REGEX_ESCASSEZ.search(fala_norm))
        if campanha in ("carrinho", "lote"):
            if not tem_escassez:
                achados.append(Achado(REPROVACAO, "cta.md", "campanha " + campanha + " exige escassez legítima", medido=fala_cta))
        elif campanha in ("frio", "captacao", "perpetuo_frio"):
            tem_preco = bool(REGEX_PRECO.search(fala_norm))
            tem_data = bool(REGEX_DATA.search(fala_norm))
            if tem_escassez or tem_preco or tem_data:
                achados.append(
                    Achado(REPROVACAO, "cta.md", "campanha " + campanha + " proibe escassez, preço ou data (R6.4)", medido=fala_cta)
                )
        elif campanha == "remarketing":
            pass  # so verbo, oferta permitida
    elif modo == "organico":
        if tipo not in ("loop", "envio", "pergunta"):
            achados.append(Achado(REPROVACAO, "cta.md", "modo orgânico exige tipo em loop, envio ou pergunta", medido=tipo))
        if REGEX_ORGANICO_PROIBIDO.search(fala_norm):
            achados.append(Achado(REPROVACAO, "cta.md", "orgânico proibe 'toca em', 'clica', 'link', 'saiba mais', 'bio', 'arrasta' (R6.5)", medido=fala_cta))
        if tipo == "pergunta" and not fala_cta.strip().endswith("?"):
            achados.append(Achado(REPROVACAO, "cta.md", "tipo pergunta exige fala terminando com ?", medido=fala_cta))
        if tipo == "envio" and not REGEX_ORGANICO_ENVIO.search(fala_norm):
            achados.append(Achado(REPROVACAO, "cta.md", "tipo envio exige 'manda pra'/'marca'/'compartilha'/'envia pra'", medido=fala_cta))
        if tipo == "loop" and not cta.get("loop"):
            achados.append(Achado(REPROVACAO, "cta.md", "tipo loop exige campo loop preenchido"))
    return achados

