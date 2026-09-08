#!/usr/bin/env python3
"""Regra do CTA (requisito 10, seção 6): fala igual ao último bloco do
roteiro, tipo e verbo de ação exigidos no modo pago, escassez legítima
obrigatória em carrinho/lote e proibida em frio/captação, e as regras do
modo orgânico (loop, envio, pergunta).

Compatibilidade: Python 3.9 (sem `X | None`; `from __future__ import
annotations` mais `Optional[X]`).
"""

from __future__ import annotations

import re
from typing import List, Optional, Sequence

from ..achados import REPROVACAO, Achado
from ..leitura import Bloco, Conceito, Cta
from ..limiares import MARCADORES_DE_PONTE, VERBOS_DE_ACAO
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

_REGEX_CAMPO_PONTE = re.compile(r"bloco\s+(\d+)\s*[:,]?\s*(.+)", re.IGNORECASE)


def _tem_marcador_de_ponte(texto: str) -> bool:
    n = normalizar(texto)
    return any(normalizar(marcador) in n for marcador in MARCADORES_DE_PONTE)


def checar_ponte(conceito: Conceito, blocos: Sequence[Bloco], cta: Cta) -> List[Achado]:
    """Regra da ponte antes do CTA: em modo pago com tipo cta, o bloco
    imediatamente anterior ao CTA (ou a primeira frase do próprio CTA)
    precisa ligar o que foi mostrado ao que o clique entrega. `cta.md`
    aceita um campo opcional `ponte: bloco N, frase`, que precisa bater
    (substring, normalizado) com a fala do bloco N citado."""
    achados: List[Achado] = []
    if not blocos:
        return achados
    modo = normalizar_codigo(conceito.modo)
    tipo = normalizar_codigo(cta.get("tipo")) if cta else ""
    if modo != "pago" or tipo != "cta":
        return achados

    ultimo = blocos[-1]
    anterior: Optional[Bloco] = blocos[-2] if len(blocos) >= 2 else None
    primeira_frase_cta = re.split(r"[.!?]", ultimo.fala or "")[0]

    tem_ponte = (anterior is not None and _tem_marcador_de_ponte(anterior.fala)) or _tem_marcador_de_ponte(
        primeira_frase_cta
    )
    if not tem_ponte:
        achados.append(
            Achado(
                REPROVACAO,
                "cta.md",
                "CTA sem ponte: o bloco anterior não liga o que foi mostrado ao que o clique entrega",
                acao="feche o bloco anterior dizendo o que a pessoa leva na aula/evento/treinamento",
            )
        )

    ponte_declarada = cta.get("ponte") if cta else ""
    if ponte_declarada:
        m = _REGEX_CAMPO_PONTE.match(ponte_declarada.strip())
        if not m:
            achados.append(
                Achado(
                    REPROVACAO, "cta.md", "campo ponte fora do formato 'bloco N, frase'",
                    acao="use o formato 'bloco N, \"frase da ponte\"' no campo ponte",
                    medido=ponte_declarada,
                )
            )
        else:
            numero_bloco = int(m.group(1))
            frase = m.group(2).strip().strip('"').strip("'").strip()
            bloco_citado = next((b for b in blocos if b.numero == numero_bloco), None)
            if bloco_citado is None:
                achados.append(
                    Achado(
                        REPROVACAO, "cta.md", "campo ponte cita bloco inexistente no roteiro",
                        acao="corrija o número do bloco no campo ponte",
                        medido=ponte_declarada,
                    )
                )
            elif normalizar(frase) not in normalizar(bloco_citado.fala):
                achados.append(
                    Achado(
                        REPROVACAO, "cta.md", "frase do campo ponte não está na fala do bloco citado",
                        acao="corrija a frase do campo ponte pra bater com a fala do bloco",
                        medido=frase, limiar=bloco_citado.fala,
                    )
                )
    return achados

def checar_cta(conceito: Conceito, blocos: Sequence[Bloco], cta: Cta) -> List[Achado]:
    """Requisito 10, seção 6."""
    achados: List[Achado] = []
    if not blocos:
        return achados
    ultimo = blocos[-1]
    fala_cta = cta.get("fala")
    if normalizar(fala_cta) != normalizar(ultimo.fala):
        achados.append(
            Achado(
                REPROVACAO, "cta.md", "fala do CTA diferente da fala do último bloco do roteiro",
                acao="copie a fala do último bloco do roteiro pro campo fala do cta.md",
                medido=fala_cta, limiar=ultimo.fala,
            )
        )
    fala_norm = normalizar(fala_cta)
    key_p = palavras_normalizadas(ultimo.chave) if ultimo.chave else []
    fala_p = palavras_normalizadas(fala_cta)
    modo = normalizar_codigo(conceito.modo)
    campanha = normalizar_codigo(conceito.campanha)
    tipo = normalizar_codigo(cta.get("tipo"))

    if modo == "pago":
        if tipo != "cta":
            achados.append(
                Achado(
                    REPROVACAO, "cta.md", "modo pago exige tipo: cta",
                    acao="preencha tipo: cta em cta.md",
                    medido=tipo, limiar="cta",
                )
            )
        tem_verbo = any(v in fala_p or v in key_p for v in VERBOS_DE_ACAO)
        if not tem_verbo:
            achados.append(
                Achado(
                    REPROVACAO, "cta.md", "CTA vago: nenhum verbo de ação na fala nem no KEY (seção 6)",
                    acao="inclua um verbo de ação da lista aceita na fala ou no KEY do CTA",
                )
            )
        tem_escassez = bool(REGEX_ESCASSEZ.search(fala_norm))
        if campanha in ("carrinho", "lote"):
            if not tem_escassez:
                achados.append(
                    Achado(
                        REPROVACAO, "cta.md", "campanha " + campanha + " exige escassez legítima",
                        acao="inclua um sinal de escassez legítima na fala do CTA (vaga, prazo, lote)",
                        medido=fala_cta,
                    )
                )
        elif campanha in ("frio", "captacao", "perpetuo_frio"):
            tem_preco = bool(REGEX_PRECO.search(fala_norm))
            tem_data = bool(REGEX_DATA.search(fala_norm))
            if tem_escassez or tem_preco or tem_data:
                achados.append(
                    Achado(
                        REPROVACAO, "cta.md", "campanha " + campanha + " proibe escassez, preço ou data (R6.4)",
                        acao="tire escassez, preço e data da fala do CTA nesta campanha",
                        medido=fala_cta,
                    )
                )
        elif campanha == "remarketing":
            pass  # so verbo, oferta permitida
    elif modo == "organico":
        if tipo not in ("loop", "envio", "pergunta"):
            achados.append(
                Achado(
                    REPROVACAO, "cta.md", "modo orgânico exige tipo em loop, envio ou pergunta",
                    acao="preencha tipo com loop, envio ou pergunta",
                    medido=tipo,
                )
            )
        if REGEX_ORGANICO_PROIBIDO.search(fala_norm):
            achados.append(
                Achado(
                    REPROVACAO, "cta.md",
                    "orgânico proibe 'toca em', 'clica', 'link', 'saiba mais', 'bio', 'arrasta' (R6.5)",
                    acao="reescreva o CTA sem termos de clique, típicos de anúncio pago",
                    medido=fala_cta,
                )
            )
        if tipo == "pergunta" and not fala_cta.strip().endswith("?"):
            achados.append(
                Achado(
                    REPROVACAO, "cta.md", "tipo pergunta exige fala terminando com ?",
                    acao="termine a fala do CTA com ponto de interrogação",
                    medido=fala_cta,
                )
            )
        if tipo == "envio" and not REGEX_ORGANICO_ENVIO.search(fala_norm):
            achados.append(
                Achado(
                    REPROVACAO, "cta.md", "tipo envio exige 'manda pra'/'marca'/'compartilha'/'envia pra'",
                    acao="inclua uma chamada de envio explícita na fala do CTA",
                    medido=fala_cta,
                )
            )
        if tipo == "loop" and not cta.get("loop"):
            achados.append(
                Achado(
                    REPROVACAO, "cta.md", "tipo loop exige campo loop preenchido",
                    acao="preencha o campo loop em cta.md descrevendo o gancho de volta ao início",
                )
            )
    return achados
