#!/usr/bin/env python3
"""Gate de copy: valida um pacote de copy contra o contrato de
`~/.claude/skills/copy-criativos/references/formato-do-pacote.md` antes de a
peça chegar na esteira `creative-studio`.

Pacote modular: `limiares.py` (números e catálogos embutidos), `texto.py`
(normalização, contagens, regexes), `achados.py` (`Achado` + `REPROVACAO`/
`AVISO`), `leitura.py` (dataclasses + `ler_*`, um por arquivo do pacote),
`regras/` (um `checar_*` por família de regra), `motor.py` (`rodar()`
junta tudo) e `cli.py` (`main()`, a CLI). Roda com `python3 -m gate_copy
<pacote>` ou via o `gate_copy.py` fino na raiz de `scripts/`.

Compatibilidade: Python 3.9 (sem `X | None`; `from __future__ import
annotations` mais `Optional[X]`).
"""

from __future__ import annotations

from .achados import AVISO, REPROVACAO, Achado
from .cli import main
from .leitura import (
    AssetLinha,
    Bloco,
    Conceito,
    Cta,
    Garrafal,
    Hook,
    LetteringLinha,
    MatrizLinha,
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
from .motor import ARQUIVOS_OBRIGATORIOS, rodar
from .texto import (
    normalizar,
    normalizar_codigo,
    numero_esta_na_fala,
    palavras_normalizadas,
    remover_acentos,
    todas_palavras_na_fala,
)

__all__ = [
    "Achado",
    "REPROVACAO",
    "AVISO",
    "LIMIARES",
    "aplicar_gates",
    "ARQUIVOS_OBRIGATORIOS",
    "rodar",
    "main",
    "PacoteInvalido",
    "Bloco",
    "Conceito",
    "Hook",
    "Garrafal",
    "LetteringLinha",
    "Cta",
    "AssetLinha",
    "MatrizLinha",
    "ler_conceito",
    "ler_roteiro",
    "ler_hooks",
    "ler_garrafais",
    "ler_letterings",
    "ler_cta",
    "ler_assets",
    "ler_matriz",
    "normalizar",
    "normalizar_codigo",
    "palavras_normalizadas",
    "remover_acentos",
    "numero_esta_na_fala",
    "todas_palavras_na_fala",
]
