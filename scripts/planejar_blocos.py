#!/usr/bin/env python3
"""CLI: planeja quantas palavras cada bloco pode ter ANTES de escrever a
copy, usando os mesmos `LIMIARES` que `gate_copy` mede depois.

Uso:
  python3 planejar_blocos.py --modo pago --campanha carrinho \
      --blocos "I,L,I,A,I,A,C" [--pps 2.9] [--aceleracao 1.45] [--alvo-s 24]

  # simular um roteiro ja contado, sem escrever o pacote inteiro:
  python3 planejar_blocos.py --modo pago --campanha frio \
      --blocos "L,L,I,L,I,A,C" --palavras "13,12,17,15,24,4,17"

  # a partir da fila de PAPEIS (references/metodo-de-copy.md, secao 3): o
  # planejador deriva a FORMA sozinho, e imprime a forma derivada antes do
  # relatorio.
  python3 planejar_blocos.py --modo pago --campanha frio \
      --papeis "H,D,P,I,P,M,P+T,O,C"

  # formato de referencia da casa (references/modelo-mestre.md): completo
  # mira 62s finais (220 a 300 palavras), curto mira 28s (110 a 130):
  python3 planejar_blocos.py --modo pago --campanha frio \
      --papeis "H,D,P,I,P,M,P+T,O,C" --formato completo

Tipos de bloco (--blocos, separados por vírgula):
  I  = bloco com inserção de vídeo
  L  = bloco só com lettering em placa
  LC = bloco com lettering em coluna ou carimbo
  A  = apresentador sozinho, sem KEY
  P  = bloco de ponte, apresentador sozinho ligando o corpo ao CTA
  C  = bloco de CTA

Papéis (--papeis, separados por vírgula, aceita combinação como "P+T"):
  H  = hook            D  = dor ou diagnóstico   P  = prova (insert)
  I  = identificação    M  = mecanismo ou virada  O  = oferta
  T  = ponte            C  = CTA
"""

from __future__ import annotations

import argparse
import os
import sys
from typing import List, Optional

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPTS_DIR)

from gate_copy.planejador import (  # noqa: E402
    checar_oferta_do_plano,
    derivar_forma_de_papeis,
    formatar_relatorio,
    planejar,
)

# Alvo de duração final por formato (references/modelo-mestre.md, "O tamanho
# de verdade"): completo é o padrão da casa (220 a 300 palavras, 52 a 71s
# finais, alvo no meio em 62s); curto só quando o cliente pedir (110 a 130
# palavras, 26 a 31s finais, alvo no meio em 28s).
ALVO_S_POR_FORMATO = {"completo": 62.0, "curto": 28.0}

# Formato completo pede o molde inteiro (9 partes do modelo mestre): menos
# de 9 blocos na forma é sinal de que uma parte foi pulada.
MINIMO_BLOCOS_FORMATO_COMPLETO = 9


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
    parser.add_argument(
        "--blocos", default=None,
        help="a FORMA da peça, separada por vírgula: I,L,LC,A,P,C (use --blocos OU --papeis, nunca os dois)",
    )
    parser.add_argument(
        "--papeis", default=None,
        help="o PAPEL de cada bloco, separado por vírgula: H,D,P,I,M,O,T,C (aceita combinação, "
        "ex. P+T); o planejador deriva a forma sozinho (use --blocos OU --papeis, nunca os dois)",
    )
    parser.add_argument("--palavras", default=None, help="contagem de palavras já escritas, uma por bloco")
    parser.add_argument("--pps", type=float, default=2.9, help="palavras por segundo (padrão 2.9)")
    parser.add_argument("--aceleracao", type=float, default=1.45, help="aceleração de edição (padrão 1.45)")
    parser.add_argument("--alvo-s", dest="alvo_s", type=float, default=None, help="duração final alvo, em segundos")
    parser.add_argument(
        "--formato", choices=("completo", "curto"), default=None,
        help="formato de referência da casa (references/modelo-mestre.md): completo mira 62s "
        "finais (220 a 300 palavras), curto mira 28s (110 a 130); define --alvo-s sozinho "
        "quando --alvo-s não é passado",
    )
    args = parser.parse_args(argv)

    if args.blocos and args.papeis:
        print(
            "use --blocos OU --papeis, nunca os dois. Faça: escolha um dos dois jeitos de "
            "descrever a peça",
            file=sys.stderr,
        )
        return 2
    if not args.blocos and not args.papeis:
        print(
            "falta --blocos ou --papeis. Faça: descreva a peça pela FORMA (--blocos) ou pelo "
            "PAPEL de cada bloco (--papeis)",
            file=sys.stderr,
        )
        return 2

    avisos_papeis: List[str] = []
    if args.papeis:
        papeis = _lista_de_str(args.papeis)
        if not papeis:
            print("--papeis vazio. Faça: passe ao menos um papel (H, D, P, I, M, O, T ou C)", file=sys.stderr)
            return 2
        try:
            tipos = derivar_forma_de_papeis(papeis)
        except ValueError as erro:
            print(str(erro), file=sys.stderr)
            return 2
        avisos_papeis = checar_oferta_do_plano(papeis)
    else:
        tipos = _lista_de_str(args.blocos)
        if not tipos:
            print("--blocos vazio. Faça: passe ao menos um tipo de bloco (I, L, LC, A, P ou C)", file=sys.stderr)
            return 2

    try:
        palavras = _lista_de_int(args.palavras)
    except ValueError:
        print("--palavras precisa ser uma lista de números separados por vírgula", file=sys.stderr)
        return 2

    alvo_s = args.alvo_s
    if alvo_s is None and args.formato:
        alvo_s = ALVO_S_POR_FORMATO[args.formato]

    try:
        resultado = planejar(
            tipos,
            pps=args.pps,
            aceleracao=args.aceleracao,
            palavras=palavras,
            alvo_s=alvo_s,
        )
    except ValueError as erro:
        print(str(erro), file=sys.stderr)
        return 2

    print("modo: " + args.modo + (" | campanha: " + args.campanha if args.campanha else ""))
    if args.papeis:
        print("forma derivada de --papeis: " + ",".join(tipos))
        if avisos_papeis:
            print("AVISOS DO PLANO (papéis):")
            for aviso in avisos_papeis:
                print("  - " + aviso)
        print("")
    if args.formato:
        print(
            "formato: %s (alvo %.0fs finais, references/modelo-mestre.md)"
            % (args.formato, ALVO_S_POR_FORMATO[args.formato])
        )
        if args.formato == "completo" and len(tipos) < MINIMO_BLOCOS_FORMATO_COMPLETO:
            print(
                "  AVISO: plano com %d bloco(s), abaixo de %d; o formato completo carrega as "
                "9 partes do modelo mestre. Faça: confira em references/modelo-mestre.md qual "
                "parte ficou de fora" % (len(tipos), MINIMO_BLOCOS_FORMATO_COMPLETO)
            )
        print("")
    print(formatar_relatorio(resultado))
    return 0


if __name__ == "__main__":
    sys.exit(main())
