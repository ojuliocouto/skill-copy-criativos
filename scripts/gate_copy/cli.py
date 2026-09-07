#!/usr/bin/env python3
"""CLI: `python3 -m gate_copy <pacote>` (ou o `gate_copy.py` fino na raiz de
`scripts/`, mantido por compatibilidade com o SKILL.md). Lê `--gates` (ou o
`gates.yaml` padrão da esteira, se existir) e imprime reprovações, avisos e
o resumo por bloco; ou o resultado em JSON com `--json`.

Compatibilidade: Python 3.9 (sem `X | None`; `from __future__ import
annotations` mais `Optional[X]`).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any, Dict, Optional, Sequence

from .motor import rodar

_AVISO_PYYAML_IMPRESSO = False


def _carregar_yaml_opcional(caminho: Optional[str]) -> Optional[Dict[str, Any]]:
    """Le um YAML da esteira (`--gates`/`--taticas`), se houver.

    Sem `pyyaml` instalado (Mac limpo, primeira instalacao do gate): imprime
    um aviso em stderr (uma vez) e devolve None, pra o chamador seguir com os
    limiares e taticas embutidos, sem nunca quebrar o gate por causa disso.
    """
    global _AVISO_PYYAML_IMPRESSO
    if not caminho or not os.path.isfile(caminho):
        return None
    try:
        import yaml  # type: ignore
    except ImportError:
        if not _AVISO_PYYAML_IMPRESSO:
            print(
                "pyyaml não instalado: rodando com os limiares e táticas embutidos "
                "(instale com: python3 -m pip install --user pyyaml)",
                file=sys.stderr,
            )
            _AVISO_PYYAML_IMPRESSO = True
        return None
    with open(caminho, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _carregar_taticas_opcional(caminho: Optional[str]) -> Optional[list]:
    """Lê `taticas_hook.yaml` (chave `taticas_hook.taticas`, lista de
    id/nome/cluster). Sem arquivo, sem a chave ou lista vazia: devolve None
    e `checar_hooks_md` cai no catálogo embutido (`TATICAS_EMBUTIDAS`)."""
    dados = _carregar_yaml_opcional(caminho)
    if not dados:
        return None
    bloco = dados.get("taticas_hook") or {}
    lista = bloco.get("taticas")
    if not lista:
        return None
    resultado = []
    for item in lista:
        if isinstance(item, dict) and item.get("id") and item.get("cluster"):
            resultado.append(
                {"id": str(item["id"]), "nome": str(item.get("nome", "")), "cluster": str(item["cluster"])}
            )
    return resultado or None


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Gate de copy do pacote creative-studio")
    parser.add_argument("pacote", help="diretório do pacote de copy")
    parser.add_argument(
        "--gates",
        default=None,
        help="caminho do gates.yaml da esteira (padrão: ~/creative-studio/config/gates.yaml, se existir)",
    )
    parser.add_argument(
        "--taticas",
        default=None,
        help=(
            "caminho do taticas_hook.yaml da esteira (padrão: "
            "~/creative-studio/config/taticas_hook.yaml, se existir; sem o arquivo, "
            "usa o catálogo embutido de 29 táticas)"
        ),
    )
    parser.add_argument("--json", action="store_true", help="saída em JSON")
    args = parser.parse_args(argv)

    gates_padrao = os.path.expanduser("~/creative-studio/config/gates.yaml")
    caminho_gates = args.gates or (gates_padrao if os.path.isfile(gates_padrao) else None)
    gates_dados = _carregar_yaml_opcional(caminho_gates)

    taticas_padrao = os.path.expanduser("~/creative-studio/config/taticas_hook.yaml")
    caminho_taticas = args.taticas or (taticas_padrao if os.path.isfile(taticas_padrao) else None)
    taticas_dados = _carregar_taticas_opcional(caminho_taticas)

    resultado = rodar(args.pacote, gates_dados=gates_dados, taticas=taticas_dados)

    if args.json:
        print(json.dumps(resultado, ensure_ascii=False))
    else:
        if resultado["reprovacoes"]:
            print("REPROVAÇÕES:")
            for r in resultado["reprovacoes"]:
                print("  - " + r)
        if resultado["avisos"]:
            print("AVISOS:")
            for a in resultado["avisos"]:
                print("  - " + a)
        if resultado["blocos"]:
            print("RESUMO POR BLOCO:")
            for b in resultado["blocos"]:
                print(
                    "  bloco %d: %d palavras, %.2fs natural, %.2fs final, insert=%s, key=%s"
                    % (b["bloco"], b["palavras"], b["duracao_natural_s"], b["duracao_final_s"], b["tem_insert"], b["key"])
                )
        if not resultado["reprovacoes"] and not resultado["avisos"]:
            print("Pacote aprovado, sem reprovações nem avisos.")

    return 1 if resultado["reprovacoes"] else 0
