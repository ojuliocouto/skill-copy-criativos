#!/usr/bin/env python3
"""Wrapper fino: delega pro pacote `gate_copy/` no mesmo diretório.

Mantido na raiz de `scripts/` por compatibilidade com o SKILL.md, que chama
`python3 ~/.claude/skills/copy-criativos/scripts/gate_copy.py <pacote>`. A
lógica de verdade (leitura, regras, CLI) mora em `gate_copy/`; use
`python3 -m gate_copy <pacote>` como alternativa.

Este arquivo e o pacote `gate_copy/` têm o MESMO NOME de propósito no
mesmo diretório. Isso funciona porque, quando este arquivo roda como
script (`python3 gate_copy.py ...`), o Python o carrega como módulo
`__main__`, não como `gate_copy`: então o `import gate_copy` logo abaixo
não colide consigo mesmo, e resolve pro pacote (diretório com
`__init__.py`), que o localizador de arquivos do Python prioriza sobre um
módulo `.py` de mesmo nome quando os dois estão no mesmo `sys.path`.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gate_copy.cli import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
