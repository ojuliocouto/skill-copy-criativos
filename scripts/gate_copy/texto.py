#!/usr/bin/env python3
"""Normalização de texto (seção 4 do contrato: minúsculas, sem acento, sem
pontuação, hífen vira espaço), contagens de palavras e as regexes livres
usadas pelas regras de roteiro e CTA.

Compatibilidade: Python 3.9 (sem `X | None`; `from __future__ import
annotations` mais `Optional[X]`).
"""

from __future__ import annotations

import re
import unicodedata
from typing import List, Optional, Sequence

from .limiares import NUMERAIS

REGEX_APRESENTACAO = re.compile(r"\b(eu sou [oa]|meu nome e|aqui e [oa]|aqui quem fala)\b")
REGEX_ANTITESE = re.compile(r"nao e [^.!?]{2,60}[.!?,] ?(e|sao|e sim)\b")
REGEX_ESCASSEZ = re.compile(
    r"vaga|vagas|ingresso|ingressos|lote|prazo|ultim|hoje|encerra|fecha|acaba|restam?"
)
REGEX_PRECO = re.compile(r"r\$|reais|por apenas|parcel")
_MESES = (
    "janeiro|fevereiro|marco|abril|maio|junho|julho|agosto|setembro|outubro|"
    "novembro|dezembro"
)
_DIAS_DA_SEMANA = (
    "segunda|terca|quarta|quinta|sexta|sabado|domingo"
)
# So pega "dia" seguido de numero ou de mes (nao "dia da medicao", "dia da
# entrega", "dia da instalacao", "no dia" solto): "dia da"/"dia do" NAO tem
# digito logo depois, entao nao casa. Dias da semana so contam com um
# numero por perto (ex.: "segunda, dia 15"), nunca a palavra sozinha.
REGEX_DATA = re.compile(
    r"\b\d{1,2} de (" + _MESES + r")\b|\b20\d\d\b|\bdia \d"
    r"|\b(" + _DIAS_DA_SEMANA + r")[a-z]*\b[^.!?]{0,20}?\b\d{1,2}\b"
)
REGEX_EDICAO = re.compile(r"\bedicao\b|turma \d|lote \d|\d+a\b")
REGEX_DIGITO_SOLTO = re.compile(r"\b\d+\b")
REGEX_ORGANICO_PROIBIDO = re.compile(
    r"toca em|toque em|clica|clique|link|saiba mais|bio|arrasta|arraste"
)
REGEX_ORGANICO_ENVIO = re.compile(
    r"manda pra|mande pra|marca |marque |compartilha|compartilhe|envia pra"
)
REGEX_DIRECAO_VAGA = re.compile(
    r"algo|generico|qualquer|imagens de|video de|imagem de"
)

# ---------------------------------------------------------------------------
# Normalizacao de texto (secao 4 do pedido: minusculas, sem acento, sem
# pontuacao, hifen vira espaco)
# ---------------------------------------------------------------------------


def remover_acentos(texto: str) -> str:
    normalizado = unicodedata.normalize("NFKD", texto)
    return "".join(c for c in normalizado if not unicodedata.combining(c))


def normalizar(texto: Optional[str]) -> str:
    """Minusculas, sem acento, hifen vira espaco, pontuacao fora."""
    if not texto:
        return ""
    t = remover_acentos(texto).lower()
    t = t.replace("-", " ")
    t = re.sub(r"[^0-9a-z\s]", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def palavras_normalizadas(texto: Optional[str]) -> List[str]:
    n = normalizar(texto)
    return n.split() if n else []


def normalizar_codigo(texto: Optional[str]) -> str:
    """Normaliza um valor de dominio (forma, cor, id de tatica/formato, tipo,
    origem...). Ao contrario de `normalizar`, preserva "_" e ":", porque os
    ids da esteira usam snake_case (ex.: "seta_cta", "myth_busting",
    "criar:ui_html") e a normalizacao de texto livre trocaria "_" por espaco."""
    if not texto:
        return ""
    t = remover_acentos(texto).strip().lower()
    t = re.sub(r"\s+", " ", t)
    t = re.sub(r"\s*:\s*", ":", t)
    return t


def contem_sublista(lista: Sequence[str], sub: Sequence[str]) -> bool:
    return indice_sublista(lista, sub) is not None


def indice_sublista(lista: Sequence[str], sub: Sequence[str]) -> Optional[int]:
    n = len(sub)
    if n == 0:
        return None
    for i in range(len(lista) - n + 1):
        if list(lista[i:i + n]) == list(sub):
            return i
    return None


def numero_esta_na_fala(token_digito: str, fala_palavras: Sequence[str]) -> bool:
    """Casa um algarismo (ex.: "5") com a fala por extenso (ex.: "cinco")."""
    if token_digito in fala_palavras:
        return True
    for variante in NUMERAIS.get(token_digito, ()):
        if contem_sublista(fala_palavras, variante.split()):
            return True
    return False


_REGEX_TOKEN_HORA = re.compile(r"^(\d+)h$")


def token_esta_na_fala(token: str, fala_palavras: Sequence[str]) -> bool:
    if token.isdigit():
        return numero_esta_na_fala(token, fala_palavras)
    m = _REGEX_TOKEN_HORA.match(token)
    if m:
        # "11h" (notacao de hora) casa com o mesmo numeral por extenso que
        # "11" ("onze"): o "h" e formato de hora, nao parte do numero.
        return numero_esta_na_fala(m.group(1), fala_palavras)
    return token in fala_palavras


def todas_palavras_na_fala(texto: str, fala_palavras: Sequence[str]) -> List[str]:
    """Devolve os tokens de `texto` que NAO estao na fala (lista vazia = ok)."""
    faltando = []
    for token in palavras_normalizadas(texto):
        if not token_esta_na_fala(token, fala_palavras):
            faltando.append(token)
    return faltando


def contar_palavras_nao_numericas(texto: str) -> int:
    return sum(1 for t in palavras_normalizadas(texto) if not t.isdigit())


# Palavras funcionais que NAO contam pro limite de tamanho do KEY (correcao
# de leitura, secao 5): so palavra de CONTEUDO conta pro maximo de 2 (ou 3
# no CTA). Nao vale pro LEAD, que conta toda palavra.
PALAVRAS_FUNCIONAIS_KEY: frozenset = frozenset(
    {
        "de", "do", "da", "dos", "das", "no", "na", "nos", "nas", "em", "que",
        "e", "o", "a", "os", "as", "um", "uma", "pra", "pro", "com", "sem",
    }
)


def contar_palavras_de_conteudo_do_key(texto: str) -> int:
    """Conta as palavras do KEY que valem pro limite de tamanho (secao 5):
    nem algarismo, nem palavra funcional."""
    return sum(
        1
        for t in palavras_normalizadas(texto)
        if not t.isdigit() and t not in PALAVRAS_FUNCIONAIS_KEY
    )

