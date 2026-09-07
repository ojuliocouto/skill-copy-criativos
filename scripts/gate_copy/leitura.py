#!/usr/bin/env python3
"""Modelos de dados e leitores: cada função `ler_*` lê um dos 8 arquivos do
pacote (seção correspondente do contrato entre parênteses) e devolve os
dataclasses definidos aqui.

Compatibilidade: Python 3.9 (sem `X | None`; `from __future__ import
annotations` mais `Optional[X]`).
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence, Tuple

from .frontmatter import ler_front_matter
from .texto import normalizar, normalizar_codigo

@dataclass
class Bloco:
    numero: int
    linha_original: str
    direcao: str
    fala: str
    ancora: Optional[str] = None
    lead: Optional[str] = None
    chave: Optional[str] = None
    palavras: int = 0
    duracao_natural: float = 0.0
    duracao_final: float = 0.0
    inicio_final: float = 0.0

    @property
    def e_insert(self) -> bool:
        return self.ancora is not None

    @property
    def tem_logo(self) -> bool:
        return "logo" in normalizar(self.direcao).split()

    @property
    def tem_colchete(self) -> bool:
        return bool(self.direcao) or "[" in self.linha_original


@dataclass
class Conceito:
    dados: Dict[str, Any]

    def get(self, chave: str, padrao: Any = None) -> Any:
        return self.dados.get(chave, padrao)

    @property
    def pps(self) -> float:
        return float(self.dados.get("palavras_por_segundo", 2.9) or 2.9)

    @property
    def aceleracao(self) -> float:
        return float(self.dados.get("aceleracao", 1.45) or 1.45)

    @property
    def marcas(self) -> List[str]:
        marcas = self.dados.get("marcas") or []
        if isinstance(marcas, str):
            return [marcas]
        return list(marcas)

    @property
    def objetivo(self) -> str:
        objetivo = self.dados.get("objetivo")
        if objetivo:
            return str(objetivo)
        campanha = str(self.dados.get("campanha", ""))
        if campanha in ("carrinho", "lote"):
            return "carrinho"
        return "frio"

    @property
    def modo(self) -> str:
        return str(self.dados.get("modo", ""))

    @property
    def campanha(self) -> str:
        return str(self.dados.get("campanha", ""))


@dataclass
class Hook:
    nome: str  # "Hook A", "Hook B", "Hook C"
    dados: Dict[str, str]

    def get(self, chave: str, padrao: str = "") -> str:
        return self.dados.get(chave, padrao)

    @property
    def fala(self) -> str:
        return self.dados.get("fala", "")

    @property
    def cru(self) -> bool:
        return normalizar_codigo(self.dados.get("cru", "")) in ("sim",)


@dataclass
class Garrafal:
    nome: str
    palavra: str
    bloco: int
    ancora: str
    cor: str


@dataclass
class LetteringLinha:
    bloco: int
    lead: str
    key: str
    ancora_na_fala: str
    forma: str


@dataclass
class Cta:
    dados: Dict[str, str]

    def get(self, chave: str, padrao: str = "") -> str:
        return self.dados.get(chave, padrao)


@dataclass
class AssetLinha:
    numero: str
    ancora: str
    enquadramento: str
    origem: str
    referencia: str
    serve: str
    ressalva: str


@dataclass
class MatrizLinha:
    numero: str
    peca: str
    hook: str
    legenda: str
    formato: str
    avatar_em_tela: str

# ---------------------------------------------------------------------------
# Leitores (um por arquivo do pacote)
# ---------------------------------------------------------------------------


class PacoteInvalido(Exception):
    """Insumo faltando ou ilegível no pacote (R8.4: recusa nomeando o arquivo)."""


def _ler_arquivo(caminho: str) -> str:
    if not os.path.isfile(caminho):
        raise PacoteInvalido("arquivo faltando: " + caminho)
    with open(caminho, "r", encoding="utf-8") as f:
        return f.read()


def ler_conceito(caminho: str) -> Conceito:
    """conceito.md (seção 1): front matter YAML entre '---'."""
    texto = _ler_arquivo(caminho)
    m = re.search(r"^---\s*\n(.*?)\n---\s*\n", texto, re.DOTALL | re.MULTILINE)
    if not m:
        raise PacoteInvalido("conceito.md sem front matter YAML válido")
    dados = ler_front_matter(m.group(1)) or {}
    if not isinstance(dados, dict):
        raise PacoteInvalido("conceito.md com front matter que não é um mapa")
    return Conceito(dados=dados)


# Reproduz o comportamento de leitura de creative_studio/inserts/fontes.py,
# sem importar o pacote da esteira (pedido explicito da tarefa).
_ABERTURA = "["
_FECHAMENTO = "]"
_SEPARADOR_DE_CAMPO = "|"
_SEPARADOR_DE_VALOR = ":"
_PREFIXOS_DE_INSERT = ("insercao de video", "insercao de video")  # normalizado


def _partir_linha_roteiro(linha: str) -> Tuple[str, str]:
    limpa = linha.strip()
    if not limpa.startswith(_ABERTURA) or _FECHAMENTO not in limpa:
        return "", limpa
    direcao, _, fala = limpa[len(_ABERTURA):].partition(_FECHAMENTO)
    return direcao.strip(), fala.strip()


def _campos_direcao(direcao: str) -> List[str]:
    return [pedaco.strip() for pedaco in direcao.split(_SEPARADOR_DE_CAMPO)]


def _valor_do_campo_direcao(campos: Sequence[str], nome: str) -> Optional[str]:
    for campo in campos[1:]:
        rotulo, _, valor = campo.partition(_SEPARADOR_DE_VALOR)
        if normalizar(rotulo) == nome:
            return valor.strip()
    return None


def _ancora_da_direcao(campos: Sequence[str]) -> Optional[str]:
    cabeca = campos[0]
    rotulo, separador, resto = cabeca.partition(_SEPARADOR_DE_VALOR)
    if not separador:
        return None
    if normalizar(rotulo) not in _PREFIXOS_DE_INSERT:
        return None
    ancora = resto.strip()
    return ancora if ancora else None


def ler_roteiro(caminho: str, conceito: Conceito) -> List[Bloco]:
    """roteiro.txt (seção 2). Uma linha = um bloco; linha em branco é ignorada."""
    texto = _ler_arquivo(caminho)
    blocos: List[Bloco] = []
    inicio_acumulado = 0.0
    for linha in texto.splitlines():
        if not linha.strip():
            continue
        direcao, fala = _partir_linha_roteiro(linha)
        campos = _campos_direcao(direcao) if direcao else [""]
        ancora = _ancora_da_direcao(campos)
        lead = _valor_do_campo_direcao(campos, "lead")
        chave = _valor_do_campo_direcao(campos, "key")
        palavras = len(fala.split())
        natural = palavras / conceito.pps if conceito.pps else 0.0
        final = natural / conceito.aceleracao if conceito.aceleracao else 0.0
        blocos.append(
            Bloco(
                numero=len(blocos) + 1,
                linha_original=linha,
                direcao=direcao,
                fala=fala,
                ancora=ancora,
                lead=lead,
                chave=chave,
                palavras=palavras,
                duracao_natural=natural,
                duracao_final=final,
                inicio_final=inicio_acumulado,
            )
        )
        inicio_acumulado += final
    return blocos


def _ler_secoes_chave_valor(texto: str) -> List[Tuple[str, Dict[str, str]]]:
    """Le arquivos .md com secoes '## Nome' e linhas '- chave: valor'.

    Usado por hooks.md, garrafais.md e cta.md (secao 21 do contrato: chave e
    valor lidos com "chave: valor", negrito ignorado).
    """
    secoes: List[Tuple[str, Dict[str, str]]] = []
    titulo_atual: Optional[str] = None
    dados_atual: Dict[str, str] = {}
    for linha in texto.splitlines():
        bruta = linha.strip()
        if bruta.startswith("## "):
            if titulo_atual is not None:
                secoes.append((titulo_atual, dados_atual))
            titulo_atual = bruta[3:].strip()
            dados_atual = {}
            continue
        if bruta.startswith("- "):
            corpo = bruta[2:].strip()
            corpo = corpo.replace("**", "")
            chave, sep, valor = corpo.partition(":")
            if sep:
                dados_atual[normalizar(chave)] = valor.strip()
    if titulo_atual is not None:
        secoes.append((titulo_atual, dados_atual))
    return secoes


def ler_hooks(caminho: str) -> List[Hook]:
    """hooks.md (seção 3): uma seção '## Hook X' por hook."""
    texto = _ler_arquivo(caminho)
    hooks = []
    for titulo, dados in _ler_secoes_chave_valor(texto):
        if normalizar(titulo).startswith("hook"):
            hooks.append(Hook(nome=titulo, dados=dados))
    return hooks


def ler_garrafais(caminho: str) -> List[Garrafal]:
    """garrafais.md (seção 4): uma seção '## Gn' por garrafal."""
    texto = _ler_arquivo(caminho)
    garrafais = []
    for titulo, dados in _ler_secoes_chave_valor(texto):
        try:
            bloco = int(str(dados.get("bloco", "0")).strip())
        except ValueError:
            bloco = 0
        garrafais.append(
            Garrafal(
                nome=titulo,
                palavra=dados.get("palavra", ""),
                bloco=bloco,
                ancora=dados.get("ancora", ""),
                cor=dados.get("cor", ""),
            )
        )
    return garrafais


def ler_cta(caminho: str) -> Cta:
    """cta.md (seção 6): uma única seção de campos."""
    texto = _ler_arquivo(caminho)
    secoes = _ler_secoes_chave_valor(texto)
    if secoes:
        return Cta(dados=secoes[0][1])
    # cta.md pode nao ter titulo de secao "## ...": trata o arquivo inteiro.
    dados: Dict[str, str] = {}
    for linha in texto.splitlines():
        bruta = linha.strip()
        if bruta.startswith("- "):
            corpo = bruta[2:].strip().replace("**", "")
            chave, sep, valor = corpo.partition(":")
            if sep:
                dados[normalizar(chave)] = valor.strip()
    return Cta(dados=dados)


def _ler_tabela_markdown(texto: str) -> List[List[str]]:
    """Le uma tabela markdown e devolve as linhas de dados (sem cabecalho nem
    separador), cada uma como lista de celulas com o texto limpo."""
    linhas_tabela = [l for l in texto.splitlines() if l.strip().startswith("|")]
    if len(linhas_tabela) < 2:
        return []
    dados = []
    for linha in linhas_tabela[2:]:  # pula cabecalho + separador ---
        celulas = [c.strip() for c in linha.strip().strip("|").split("|")]
        if all(re.match(r"^:?-+:?$", c) for c in celulas if c):
            continue
        dados.append(celulas)
    return dados


def ler_letterings(caminho: str) -> List[LetteringLinha]:
    """letterings.md (seção 5): tabela bloco | LEAD | KEY | âncora | forma | ..."""
    texto = _ler_arquivo(caminho)
    linhas = _ler_tabela_markdown(texto)
    resultado = []
    for celulas in linhas:
        if len(celulas) < 5:
            continue
        try:
            bloco = int(celulas[0])
        except ValueError:
            continue
        resultado.append(
            LetteringLinha(
                bloco=bloco,
                lead=celulas[1],
                key=celulas[2],
                ancora_na_fala=celulas[3],
                forma=normalizar_codigo(celulas[4]),
            )
        )
    return resultado


def ler_assets(caminho: str) -> List[AssetLinha]:
    """assets.md (seção 7): tabela # | âncora | enquadramento | origem | referência | serve | ressalva."""
    texto = _ler_arquivo(caminho)
    linhas = _ler_tabela_markdown(texto)
    resultado = []
    for celulas in linhas:
        while len(celulas) < 7:
            celulas.append("")
        resultado.append(
            AssetLinha(
                numero=celulas[0],
                ancora=celulas[1],
                enquadramento=normalizar_codigo(celulas[2]),
                origem=normalizar_codigo(celulas[3]),
                referencia=celulas[4],
                serve=normalizar_codigo(celulas[5]),
                ressalva=celulas[6],
            )
        )
    return resultado


def ler_matriz(caminho: str) -> Tuple[Dict[str, Any], List[MatrizLinha]]:
    """matriz.md (seção 8): campos soltos + tabela de 12 peças."""
    texto = _ler_arquivo(caminho)
    campos: Dict[str, Any] = {}
    for linha in texto.splitlines():
        bruta = linha.strip()
        if bruta.startswith("- "):
            corpo = bruta[2:].strip().replace("**", "")
            chave, sep, valor = corpo.partition(":")
            if sep:
                campos[normalizar(chave)] = valor.strip()
    linhas = _ler_tabela_markdown(texto)
    pecas = []
    for celulas in linhas:
        while len(celulas) < 6:
            celulas.append("")
        pecas.append(
            MatrizLinha(
                numero=celulas[0],
                peca=celulas[1],
                hook=celulas[2],
                legenda=celulas[3],
                formato=celulas[4],
                avatar_em_tela=normalizar_codigo(celulas[5]),
            )
        )
    return campos, pecas
