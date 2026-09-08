#!/usr/bin/env python3
"""CLI: planeja quantas palavras cada bloco pode ter ANTES de escrever a
copy, usando os mesmos `LIMIARES` que `gate_copy` mede depois.

Uso:
  python3 planejar_blocos.py --modo pago --campanha carrinho \
      --blocos "I,L,I,A,I,A,C" [--pps 2.9] [--aceleracao 1.45] [--alvo-s 24]

  # simular um roteiro ja contado, sem escrever o pacote inteiro:
  python3 planejar_blocos.py --modo pago --campanha frio \
      --blocos "L,L,I,L,I,A,C" --palavras "13,12,17,15,24,4,17"

Tipos de bloco (--blocos, separados por vírgula):
  I  = bloco com inserção de vídeo
  L  = bloco só com lettering em placa
  LC = bloco com lettering em coluna ou carimbo
  A  = apresentador sozinho, sem KEY
  P  = bloco de ponte, apresentador sozinho ligando o corpo ao CTA
  C  = bloco de CTA
"""

from __future__ import annotations

import argparse
import os
import sys
from typing import List, Optional

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPTS_DIR)

from gate_copy.planejador import formatar_relatorio, planejar  # noqa: E402


def _lista_de_str(valor: str) -> List[str]:
    return [t.strip().upper() for t in valor.split(",") if t.strip()]


def _lista_de_int(valor: Optional[str]) -> Optional[List[int]]:
    if valor is None:
        return None
    return [int(p.strip()) for p in valor.split(",") if p.strip()]


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Planeja o número de palavras por bloco antes da copy")
    parser.add_argument("--modo", choices=("pago", "organico"), default="pago", help="modo da peça (informativo)")
    parser.add_argument("--campanha", default="", help="campanha da peça (informativo)")
    parser.add_argument("--blocos", required=True, help="sequência de tipos separados por vírgula: I,L,LC,A,P,C")
    parser.add_argument("--palavras", default=None, help="contagem de palavras já escritas, uma por bloco")
    parser.add_argument("--pps", type=float, default=2.9, help="palavras por segundo (padrão 2.9)")
    parser.add_argument("--aceleracao", type=float, default=1.45, help="aceleração de edição (padrão 1.45)")
    parser.add_argument("--alvo-s", dest="alvo_s", type=float, default=None, help="duração final alvo, em segundos")
    args = parser.parse_args(argv)

    tipos = _lista_de_str(args.blocos)
    if not tipos:
        print("--blocos vazio. Faça: passe ao menos um tipo de bloco (I, L, LC, A, P ou C)", file=sys.stderr)
        return 2

    try:
        palavras = _lista_de_int(args.palavras)
    except ValueError:
        print("--palavras precisa ser uma lista de números separados por vírgula", file=sys.stderr)
        return 2

    try:
        resultado = planejar(
            tipos,
            pps=args.pps,
            aceleracao=args.aceleracao,
            palavras=palavras,
            alvo_s=args.alvo_s,
        )
    except ValueError as erro:
        print(str(erro), file=sys.stderr)
        return 2

    print("modo: " + args.modo + (" | campanha: " + args.campanha if args.campanha else ""))
    print(formatar_relatorio(resultado))
    return 0


if __name__ == "__main__":
    sys.exit(main())
