#!/usr/bin/env python3
"""Orquestração: `rodar()` lê os 8 arquivos do pacote, roda toda checagem e
devolve reprovações + avisos + resumo por bloco.

Os limiares em `gate_copy.limiares.LIMIARES` são mutados NO LUGAR (clear +
update), nunca reatribuídos: cada módulo de regra fez `from ..limiares
import LIMIARES`, o que prende o nome ao dicionário original. Reatribuir
`limiares.LIMIARES = outro_dict` quebraria essas referências; mutar o
mesmo objeto mantém todo mundo em sincronia, e o `finally` devolve o
dicionário ao estado original mesmo se alguma checagem falhar.

Compatibilidade: Python 3.9 (sem `X | None`; `from __future__ import
annotations` mais `Optional[X]`).
"""

from __future__ import annotations

import os
from typing import Any, Dict, List, Optional, Sequence

from .achados import AVISO, REPROVACAO, Achado
from .leitura import (
    PacoteInvalido,
    ler_assets,
    ler_conceito,
    ler_cta,
    ler_garrafais,
    ler_hooks,
    ler_letterings,
    ler_matriz,
    ler_roteiro,
)
from .limiares import LIMIARES, aplicar_gates
from .regras.assets import checar_assets
from .regras.cta import checar_cta, checar_oferta, checar_ponte
from .regras.duracoes import checar_duracoes
from .regras.garrafais import checar_garrafais
from .regras.hook import checar_hook, checar_hooks_md
from .regras.letterings import checar_letterings
from .regras.matriz import checar_matriz
from .regras.roteiro import (
    checar_antitese,
    checar_densidade_insert,
    checar_direcoes,
    checar_eco,
    checar_envelhecimento,
    checar_frases,
    checar_janelas_de_insert,
    checar_marca,
)

ARQUIVOS_OBRIGATORIOS = (
    "conceito.md",
    "roteiro.txt",
    "hooks.md",
    "garrafais.md",
    "letterings.md",
    "cta.md",
    "assets.md",
    "matriz.md",
)


def _caminho(pacote_dir: str, nome: str) -> str:
    return os.path.join(pacote_dir, nome)


def rodar(
    pacote_dir: str,
    gates_dados: Optional[Dict[str, Any]] = None,
    taticas: Optional[Sequence[Dict[str, str]]] = None,
) -> Dict[str, Any]:
    limiares_efetivos = aplicar_gates(LIMIARES, gates_dados)
    # Mutação NO LUGAR (nunca `LIMIARES = ...`): cada `regras/*.py` fez
    # `from ..limiares import LIMIARES`, prendendo o nome ao dicionário
    # original. Reatribuir o atributo do módulo criaria um dicionário novo
    # que essas referências não veriam.
    limiares_originais = {
        chave: (dict(valor) if isinstance(valor, dict) else valor)
        for chave, valor in LIMIARES.items()
    }
    LIMIARES.clear()
    LIMIARES.update(limiares_efetivos)
    try:
        # R8.4: sem conceito.md o gate recusa o pacote inteiro, nomeando o arquivo.
        conceito = ler_conceito(_caminho(pacote_dir, "conceito.md"))

        for nome in ARQUIVOS_OBRIGATORIOS[1:]:
            if not os.path.isfile(_caminho(pacote_dir, nome)):
                return {
                    "reprovacoes": [
                        Achado(
                            REPROVACAO,
                            "pacote",
                            "arquivo obrigatório faltando: " + nome,
                            acao="crie o arquivo " + nome + " no pacote antes de rodar o gate de novo",
                        ).linha()
                    ],
                    "avisos": [],
                    "blocos": [],
                }

        blocos = ler_roteiro(_caminho(pacote_dir, "roteiro.txt"), conceito)
        hooks = ler_hooks(_caminho(pacote_dir, "hooks.md"))
        garrafais = ler_garrafais(_caminho(pacote_dir, "garrafais.md"))
        letterings = ler_letterings(_caminho(pacote_dir, "letterings.md"))
        cta = ler_cta(_caminho(pacote_dir, "cta.md"))
        assets = ler_assets(_caminho(pacote_dir, "assets.md"))
        campos_matriz, pecas = ler_matriz(_caminho(pacote_dir, "matriz.md"))

        achados: List[Achado] = []
        achados.extend(checar_direcoes(blocos))
        achados.extend(checar_marca(conceito, blocos, hooks))
        achados.extend(checar_hook(conceito, blocos, hooks))
        achados.extend(checar_hooks_md(conceito, blocos, hooks, taticas=taticas))
        achados.extend(checar_letterings(blocos, letterings, cta))
        achados.extend(checar_garrafais(blocos, garrafais))
        achados.extend(checar_cta(conceito, blocos, cta))
        achados.extend(checar_ponte(conceito, blocos, cta))
        achados.extend(checar_oferta(conceito, blocos, cta))
        achados.extend(checar_assets(blocos, assets))
        achados.extend(checar_matriz(conceito, hooks, campos_matriz, pecas))
        achados.extend(checar_frases(blocos))
        achados.extend(checar_envelhecimento(conceito, blocos))
        achados.extend(checar_antitese(blocos, hooks))
        achados.extend(checar_duracoes(conceito, blocos, letterings, cta))
        achados.extend(checar_janelas_de_insert(conceito, blocos))
        achados.extend(checar_densidade_insert(conceito, blocos))
        achados.extend(checar_eco(blocos, hooks, raiz_pacote=pacote_dir))

        reprovacoes = [a.linha() for a in achados if a.nivel == REPROVACAO]
        avisos = [a.linha() for a in achados if a.nivel == AVISO]
        resumo_blocos = [
            {
                "bloco": b.numero,
                "palavras": b.palavras,
                "duracao_natural_s": round(b.duracao_natural, 2),
                "duracao_final_s": round(b.duracao_final, 2),
                "tem_insert": b.e_insert,
                "key": b.chave or "",
            }
            for b in blocos
        ]
        return {"reprovacoes": reprovacoes, "avisos": avisos, "blocos": resumo_blocos}
    except PacoteInvalido as erro:
        return {"reprovacoes": ["pacote: " + str(erro)], "avisos": [], "blocos": []}
    finally:
        LIMIARES.clear()
        LIMIARES.update(limiares_originais)

