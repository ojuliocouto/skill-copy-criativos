#!/usr/bin/env python3
"""`Achado`: o item que toda função `checar_*` devolve (reprovação ou
aviso, com onde, recado, medido, limiar e a ação recomendada). `REPROVACAO`/
`AVISO` são os dois níveis possíveis.

Toda mensagem final (`linha()`) segue o formato:
`<onde>: <o que está errado> (medido: X; limiar: Y). Faça: <ação>`.
Quando não houver `medido` ou `limiar`, o parênteses correspondente é
omitido (nunca aparece "limiar: " vazio); quando não houver nenhum dos
dois, o parênteses inteiro some. `acao` é obrigatório: toda mensagem do
gate precisa ser acionável.

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
    acao: str
    medido: str = ""
    limiar: str = ""

    def __post_init__(self) -> None:
        if not self.acao or not self.acao.strip():
            raise ValueError(
                "Achado sem acao: toda mensagem do gate precisa dizer o que fazer "
                "(onde=" + repr(self.onde) + ", recado=" + repr(self.recado) + ")"
            )

    def _parenteses(self) -> str:
        if self.medido and self.limiar:
            return "(medido: " + self.medido + "; limiar: " + self.limiar + ")"
        if self.medido:
            return "(medido: " + self.medido + ")"
        if self.limiar:
            return "(limiar: " + self.limiar + ")"
        return ""

    def linha(self) -> str:
        base = self.onde + ": " + self.recado
        parenteses = self._parenteses()
        if parenteses:
            base = base + " " + parenteses
        if not base.endswith("."):
            base = base + "."
        return base + " Faça: " + self.acao
