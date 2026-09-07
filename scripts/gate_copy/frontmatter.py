#!/usr/bin/env python3
"""Parser do front matter de `conceito.md` (seção 1 do contrato).

Usa `yaml.safe_load` quando `pyyaml` está instalado. Sem `pyyaml` (Mac limpo,
aluno instalando o gate pela primeira vez), cai num parser próprio que cobre
o subconjunto do YAML usado nos pacotes de copy: chaves `chave: valor` no
nível zero, valores escalares (string, int, float, booleano em `true/false`
ou `sim/não`), listas em linhas `  - item` sob uma chave sem valor, e strings
entre aspas simples ou duplas.

Compatibilidade: Python 3.9 (sem `X | None`; `from __future__ import
annotations` mais `Optional[X]`).
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

try:
    import yaml  # type: ignore
except ImportError:
    yaml = None  # type: ignore


def _converter_escalar(bruto: str) -> Any:
    valor = bruto.strip()
    if not valor:
        return None
    if (valor.startswith('"') and valor.endswith('"') and len(valor) >= 2) or (
        valor.startswith("'") and valor.endswith("'") and len(valor) >= 2
    ):
        return valor[1:-1]
    minusculo = valor.lower()
    if minusculo in ("true", "sim"):
        return True
    if minusculo in ("false", "nao", "não"):
        return False
    try:
        return int(valor)
    except ValueError:
        pass
    try:
        return float(valor)
    except ValueError:
        pass
    return valor


def _ler_front_matter_proprio(texto: str) -> Dict[str, Any]:
    """Parser próprio do subconjunto de YAML usado nos pacotes de copy.

    Assume nível zero de indentação para chaves e indentação (qualquer
    quantidade de espaços) para itens de lista `- item`.
    """
    dados: Dict[str, Any] = {}
    chave_pendente: Optional[str] = None
    lista_pendente: Optional[List[Any]] = None

    for linha_bruta in texto.splitlines():
        if not linha_bruta.strip():
            continue
        if linha_bruta.strip().startswith("#"):
            continue

        indentado = linha_bruta[:1] in (" ", "\t")
        linha = linha_bruta.strip()

        if indentado and linha.startswith("- ") and chave_pendente is not None:
            if lista_pendente is None:
                lista_pendente = []
                dados[chave_pendente] = lista_pendente
            lista_pendente.append(_converter_escalar(linha[2:]))
            continue

        # linha no nivel zero: fecha lista pendente (se houver) e comeca campo novo
        chave_pendente = None
        lista_pendente = None

        chave, separador, resto = linha.partition(":")
        if not separador:
            continue
        chave = chave.strip()
        resto = resto.strip()

        if not resto:
            # pode ser o comeco de uma lista nas proximas linhas
            chave_pendente = chave
            lista_pendente = None
            dados.setdefault(chave, None)
            continue

        dados[chave] = _converter_escalar(resto)

    return dados


def ler_front_matter(texto: str) -> Dict[str, Any]:
    """Parseia o bloco de front matter (conteúdo entre os `---`).

    Usa `yaml.safe_load` quando disponível; sem `pyyaml`, usa o parser
    próprio (`_ler_front_matter_proprio`)."""
    if yaml is not None:
        dados = yaml.safe_load(texto)
        return dados or {}
    return _ler_front_matter_proprio(texto)
