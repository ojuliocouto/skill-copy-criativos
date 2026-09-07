#!/usr/bin/env python3
"""`Achado`: o item que toda função `checar_*` devolve (reprovação ou
aviso, com onde, recado, medido e limiar). `REPROVACAO`/`AVISO` são os dois
níveis possíveis.

Compatibilidade: Python 3.9 (sem `X | None`; `from __future__ import
annotations` mais `Optional[X]`).
"""

from __future__ import annotations

from dataclasses import dataclass

REPROVACAO = "reprovacao"
AVISO = "aviso"

@dataclass(frozen=True)
class Achado:
    nivel: str
    onde: str
    recado: str
    medido: str = ""
    limiar: str = ""

    def linha(self) -> str:
        pedacos = [self.onde + ": " + self.recado]
        if self.medido or self.limiar:
            pedacos.append("(medido: " + self.medido + "; limiar: " + self.limiar + ")")
        return " ".join(pedacos)
