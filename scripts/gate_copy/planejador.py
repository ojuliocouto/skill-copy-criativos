#!/usr/bin/env python3
"""Planejador de blocos: recebe o PLANO da peça (a sequência de tipos de
bloco) antes de a copy existir, e devolve quantas palavras cada bloco pode
ter, usando os mesmos `LIMIARES` que o gate de copy mede depois.

Tipos de bloco aceitos (seção 9 do contrato, mesma tabela do gate):
- "I": bloco com inserção de vídeo (mínimo `insert_min_s`).
- "L": bloco só com lettering em placa (mínimo da categoria "placa").
- "LC": bloco com lettering em coluna ou carimbo (mínimo dessas categorias).
- "A": apresentador sozinho, sem KEY (máximo `retencao_avatar_sozinho_max_s`,
  sem mínimo próprio).
- "P": bloco de ponte, apresentador sozinho ligando o corpo ao CTA (mesmos
  limites de "A"). O plano avisa quando o bloco logo antes do "C" não é
  "P" nem "I" (regra do dono da metodologia: CTA sem ponte).
- "C": bloco de CTA (mínimo `cta_min_s`, teto de aviso `cta_max_s`).

Duas formas de uso:
1. `planejar(tipos, pps, aceleracao)`: monta a peça com o MÍNIMO de
   palavras de cada bloco (o pior caso mais compacto) e simula a linha do
   tempo e a densidade de insert por janela nesse mínimo.
2. `planejar(tipos, pps, aceleracao, palavras=[...])`: simula um roteiro
   JÁ CONTADO (sem escrever o pacote inteiro), pros mesmos números que o
   gate mediria depois.

Reaproveita `leitura.Bloco` e a mesma função de sobreposição de janela do
gate (`regras.roteiro._tempo_de_insert_na_janela`), pra dar exatamente o
número que o gate mede depois, não uma reimplementação paralela que possa
divergir.

Compatibilidade: Python 3.9 (sem `X | None`; `from __future__ import
annotations` mais `Optional[X]`).
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence, Tuple

from .leitura import Bloco
from .limiares import LIMIARES
from .regras.roteiro import _tempo_de_insert_na_janela

TIPOS_VALIDOS = ("I", "L", "LC", "A", "P", "C")

# Tabela de conversão papel -> forma (references/metodo-de-copy.md, seção 3,
# e SKILL.md passo 0): o papel diz o que o bloco FAZ na argumentação, a
# forma diz o que aparece na TELA. Um papel combinado ("P+T", "O+T": a
# ponte entra na última frase de outro papel) usa a forma do papel base
# (a parte antes do "+"); o "+T" não muda a forma do bloco.
MAPA_PAPEL_PARA_FORMA: Dict[str, str] = {
    "H": "L",  # hook: placa no gancho
    "D": "L",  # dor ou diagnostico
    "P": "I",  # prova: insert
    "I": "A",  # identificacao: apresentador sozinho
    "M": "A",  # mecanismo ou virada: apresentador sozinho
    "O": "L",  # oferta
    "T": "P",  # ponte: apresentador sozinho ligando o corpo ao CTA
    "C": "C",  # CTA
}

_NOMES_TIPO = {
    "I": "insert",
    "L": "lettering em placa",
    "LC": "lettering em coluna/carimbo",
    "A": "apresentador sozinho (sem KEY)",
    "P": "ponte (apresentador sozinho, liga o corpo ao CTA)",
    "C": "CTA",
}

# Tipos que valem como "tem ponte" imediatamente antes do "C": um bloco de
# ponte propriamente dito, ou um insert (a fala da ponte pode vir junto com
# o insert, como no exemplo agenda-cheia, bloco 8).
_TIPOS_QUE_CONTAM_COMO_PONTE = ("P", "I")

# Tipos com maximo PROPRIO (limite de duracao real, nao o teto generico de
# frase): usados pra saber quando o ponto medio e (min+max)/2 versus min+6.
_TIPOS_COM_MAXIMO_PROPRIO = ("A", "P", "C")


def validar_tipos(tipos: Sequence[str]) -> List[str]:
    """Levanta `ValueError` (mensagem em PT-BR, acionável) se algum tipo
    não estiver em `TIPOS_VALIDOS`."""
    invalidos = [t for t in tipos if t not in TIPOS_VALIDOS]
    if invalidos:
        raise ValueError(
            "tipo de bloco invalido: " + ", ".join(sorted(set(invalidos)))
            + ". Faça: use só I, L, LC, A, P ou C em --blocos"
        )
    return list(tipos)


def derivar_forma_de_papeis(papeis: Sequence[str]) -> List[str]:
    """Converte uma sequência de PAPÉIS (`H`, `D`, `P`, `I`, `M`, `O`, `T`,
    `C`, ou combinações como `P+T`) na FORMA da peça (`I`, `L`, `LC`, `A`,
    `P`, `C`), usando `MAPA_PAPEL_PARA_FORMA`. Levanta `ValueError`
    (mensagem em PT-BR, acionável) se algum papel não estiver na tabela.

    Numa combinação (`X+T`), a forma do bloco é a do papel BASE (a parte
    antes do "+"): a ponte entra na última frase do bloco, sem trocar o que
    aparece na tela."""
    formas: List[str] = []
    invalidos: List[str] = []
    for papel in papeis:
        base = papel.split("+", 1)[0].strip().upper()
        if base not in MAPA_PAPEL_PARA_FORMA:
            invalidos.append(papel)
            continue
        formas.append(MAPA_PAPEL_PARA_FORMA[base])
    if invalidos:
        raise ValueError(
            "papel invalido: " + ", ".join(sorted(set(invalidos)))
            + ". Faça: use só H, D, P, I, M, O, T ou C (ou uma combinação como P+T) em --papeis"
        )
    return formas


# Componentes (papel OU forma) que valem como "tem ponte" imediatamente
# antes do "C": os símbolos de FORMA "P" (ponte) e "I" (insert, a fala da
# ponte pode vir junto com o insert), mais os símbolos de PAPEL "T" (ponte)
# e "O" (a ponte pode ser a última frase da própria oferta, decisão do
# dono da metodologia). Um "T"/"O" nunca aparece no alfabeto de forma, e um
# "P"/"I" de forma não colide com o significado de papel, então o mesmo
# conjunto serve pras duas chamadas (`checar_ponte_do_plano(tipos)` com a
# FORMA derivada, ou com a lista de PAPÉIS direto).
_COMPONENTES_QUE_CONTAM_COMO_PONTE = frozenset(_TIPOS_QUE_CONTAM_COMO_PONTE) | {"T", "O"}

# Janela de blocos ANTES do "C" onde o bloco de oferta pode morar (mesma
# janela que o gate mede em `regras.cta.checar_oferta`: até os 3 blocos
# imediatamente anteriores ao CTA, porque o bloco de oferta pode ocupar
# mais de uma posição, e a ponte pode ficar colada nele, entre a oferta e
# o CTA).
_JANELA_OFERTA_ANTES_DO_CTA = 3


def checar_ponte_do_plano(tipos: Sequence[str]) -> List[str]:
    """Avisa quando o bloco logo antes de um "C" não carrega ponte. Aceita
    "P" ou "I" na FORMA da peça, e "T", "P+T", "I", "O+T" ou "O" no PAPEL
    (a ponte pode ser a última frase da própria oferta)."""
    avisos: List[str] = []
    for i, tipo in enumerate(tipos):
        if tipo.strip().upper() != "C":
            continue
        anterior = tipos[i - 1] if i > 0 else None
        componentes = [c.strip().upper() for c in anterior.split("+")] if anterior else []
        tem_ponte = any(c in _COMPONENTES_QUE_CONTAM_COMO_PONTE for c in componentes)
        if not tem_ponte:
            avisos.append(
                "plano sem ponte antes do CTA (bloco " + str(i + 1) + "). Faça: use P "
                "(bloco de ponte) ou I (insert com a fala da ponte) imediatamente antes do C"
            )
    return avisos


def checar_oferta_do_plano(papeis: Sequence[str]) -> List[str]:
    """Avisa quando nenhum dos até 3 papéis imediatamente antes de um "C"
    carrega "O" (sozinho ou combinado, como "O+T"): regra do dono da
    metodologia, seção 3 e 4 de `references/metodo-de-copy.md` (bloco de
    oferta obrigatório antes do CTA). Mesma janela que o gate mede em
    `regras.cta.checar_oferta` (o bloco de oferta pode não ser o
    imediatamente anterior ao CTA, com a ponte entre os dois). Opera no
    alfabeto de PAPÉIS (`--papeis`), não no de forma."""
    avisos: List[str] = []
    for i, papel in enumerate(papeis):
        if papel.strip().upper() != "C":
            continue
        inicio_janela = max(0, i - _JANELA_OFERTA_ANTES_DO_CTA)
        candidatos = papeis[inicio_janela:i]
        tem_oferta = any(
            "O" in [c.strip().upper() for c in candidato.split("+")]
            for candidato in candidatos
        )
        if not tem_oferta:
            avisos.append(
                "plano sem bloco O de oferta antes do CTA (bloco " + str(i + 1) + "). Faça: "
                "acrescente um papel O (oferta) em algum dos " + str(_JANELA_OFERTA_ANTES_DO_CTA)
                + " blocos antes do C, sozinho ou combinado (O+T)"
            )
    return avisos


def _minimo_segundos(tipo: str, limiares: Dict[str, Any]) -> float:
    if tipo == "I":
        return float(limiares["insert_min_s"])
    if tipo == "L":
        return limiares["lettering_permanencia_min_ms"]["placa"] / 1000.0
    if tipo == "LC":
        perm = limiares["lettering_permanencia_min_ms"]
        return max(perm["coluna"], perm["carimbo"]) / 1000.0
    if tipo == "C":
        return float(limiares["cta_min_s"])
    return 0.0  # "A"/"P": sem minimo proprio


def _maximo_segundos(tipo: str, limiares: Dict[str, Any]) -> Optional[float]:
    if tipo in ("A", "P"):
        return float(limiares["retencao_avatar_sozinho_max_s"])
    if tipo == "C":
        return float(limiares["cta_max_s"])  # teto de aviso, nao reprovacao
    return None


def min_palavras_do_tipo(tipo: str, pps: float, aceleracao: float, limiares: Dict[str, Any] = LIMIARES) -> int:
    if tipo in ("A", "P"):
        # sem minimo de duracao proprio, mas com piso de palavras (uma
        # frase curta): sem isso a simulacao no minimo sai com 0 palavras
        # e "duracao 0.00s", distorcendo a densidade de insert.
        return int(limiares["piso_apresentador_sozinho_palavras"])
    segundos = _minimo_segundos(tipo, limiares)
    if segundos <= 0:
        return 0
    return math.ceil(segundos * pps * aceleracao)


def max_palavras_do_tipo(tipo: str, pps: float, aceleracao: float, limiares: Dict[str, Any] = LIMIARES) -> int:
    teto_frase = int(limiares["frase_max_palavras"])
    segundos = _maximo_segundos(tipo, limiares)
    if segundos is None:
        return teto_frase
    return min(teto_frase, math.floor(segundos * pps * aceleracao))


def medio_palavras_do_tipo(tipo: str, min_palavras: int, max_palavras: int) -> int:
    """Palavras do bloco no PONTO MEDIO entre o minimo e o maximo: a
    simulacao que se parece com um roteiro real (nem o pior caso mais
    compacto, nem o teto de frase). Para bloco sem maximo PROPRIO (I, L,
    LC: o "maximo" deles e so o teto generico de frase, nao um limite de
    duracao do proprio tipo), usa minimo + 6 em vez de (min+max)/2."""
    if tipo in _TIPOS_COM_MAXIMO_PROPRIO:
        return int(round((min_palavras + max_palavras) / 2.0))
    return min_palavras + 6


@dataclass
class LinhaPlano:
    indice: int
    tipo: str
    min_palavras: int
    max_palavras: int
    palavras: int
    min_s: float
    max_s: Optional[float]


def _simular(tipos: Sequence[str], palavras: Sequence[int], pps: float, aceleracao: float) -> List[Bloco]:
    blocos: List[Bloco] = []
    inicio = 0.0
    for i, (tipo, n_palavras) in enumerate(zip(tipos, palavras), start=1):
        natural = n_palavras / pps if pps else 0.0
        final = natural / aceleracao if aceleracao else 0.0
        blocos.append(
            Bloco(
                numero=i,
                linha_original="",
                direcao="",
                fala="",
                ancora=("insert planejado bloco " + str(i)) if tipo == "I" else None,
                lead=None,
                chave="KEY PLANEJADO" if tipo in ("L", "LC", "C") else None,
                palavras=n_palavras,
                duracao_natural=natural,
                duracao_final=final,
                inicio_final=inicio,
            )
        )
        inicio += final
    return blocos


def calcular_densidade(blocos: Sequence[Bloco], limiares: Dict[str, Any] = LIMIARES) -> Dict[str, Dict[str, Any]]:
    """Densidade de insert por janela (mesma conta de
    `regras.roteiro.checar_densidade_insert`): fração de tempo com insert
    nas janelas 'corpo' e 'fecho', mais a sugestão quando sai da faixa."""
    total_final = sum(b.duracao_final for b in blocos)
    minimo = limiares["retencao_densidade_insert_min"]
    maximo = limiares["retencao_densidade_insert_max"]
    corpo_ini = limiares["retencao_janela_corpo_ini_s"]
    corpo_fim = limiares["retencao_janela_corpo_fim_s"]
    fecho_ini = limiares["retencao_janela_fecho_ini_s"]

    janelas: List[Tuple[str, float, float]] = []
    if total_final > corpo_ini:
        janelas.append(("corpo", corpo_ini, min(corpo_fim, total_final)))
    if total_final > fecho_ini:
        janelas.append(("fecho", fecho_ini, total_final))

    resultado: Dict[str, Dict[str, Any]] = {}
    for nome, ini, fim in janelas:
        duracao_janela = fim - ini
        if duracao_janela <= 0:
            continue
        tempo_insert = _tempo_de_insert_na_janela(blocos, ini, fim)
        fracao = tempo_insert / duracao_janela
        entrada: Dict[str, Any] = {"fracao": fracao, "ini_s": ini, "fim_s": fim}
        if fracao > maximo:
            entrada["sugestao"] = (
                "tire um insert do " + nome
                + "; alvo %.0f%% a %.0f%%" % (minimo * 100, maximo * 100)
            )
        elif fracao < minimo:
            inserts_na_janela = [
                b.numero for b in blocos
                if b.e_insert and min(b.inicio_final + b.duracao_final, fim) > max(b.inicio_final, ini)
            ]
            if len(inserts_na_janela) >= 2:
                entrada["sugestao"] = (
                    "intercale um bloco A entre os inserts " + str(inserts_na_janela[0])
                    + " e " + str(inserts_na_janela[1])
                    + "; alvo %.0f%% a %.0f%%" % (minimo * 100, maximo * 100)
                )
            else:
                entrada["sugestao"] = (
                    "adicione ou alongue um insert no " + nome
                    + "; alvo %.0f%% a %.0f%%" % (minimo * 100, maximo * 100)
                )
        resultado[nome] = entrada
    return resultado


def checar_vizinhos_sem_insert(blocos: Sequence[Bloco], limiares: Dict[str, Any] = LIMIARES) -> List[str]:
    """Blocos vizinhos sem insert cuja soma de duração final passa do mesmo
    teto que o gate mede depois em `regras.duracoes.checar_duracoes`
    (`retencao.avatar_sozinho_max_s`, R3.3). Sem essa checagem no
    planejador, a forma da peça só ia acusar esse aviso depois de a copy já
    estar escrita."""
    avisos: List[str] = []
    maximo = float(limiares["retencao_avatar_sozinho_max_s"])
    for a, b in zip(blocos, blocos[1:]):
        if a.e_insert or b.e_insert:
            continue
        soma = a.duracao_final + b.duracao_final
        if soma > maximo:
            avisos.append(
                "blocos %d e %d sem insert somam %.2fs; teto %.1fs. Faça: intercale um "
                "insert ou encurte um deles" % (a.numero, b.numero, soma, maximo)
            )
    return avisos


def capacidade_de_garrafais(tipos: Sequence[str]) -> int:
    """Quantos blocos da FORMA comportam garrafal (decisão 8,
    `references/formato-do-pacote.md` seção 4): o bloco 1 (o gancho, que
    aceita qualquer forma) mais cada bloco "A" ou "P" fora do bloco 1
    (fora do gancho a garrafal só cabe em bloco de apresentador SOZINHO,
    sem insert e sem KEY). Reportado ANTES de escrever, porque a peça
    pede 2 a 3 garrafais no total (R4, `garrafais.md`), e uma forma com
    menos de 2 blocos capazes já nasce apertada."""
    if not tipos:
        return 0
    capacidade = 1  # bloco 1, o gancho
    capacidade += sum(1 for i, t in enumerate(tipos, start=1) if i != 1 and t in ("A", "P"))
    return capacidade


def checar_capacidade_de_garrafais(tipos: Sequence[str]) -> List[str]:
    """Avisa quando a forma comporta menos de 2 blocos pra garrafal."""
    capacidade = capacidade_de_garrafais(tipos)
    if capacidade < 2:
        return [
            "forma comporta só %d bloco pra garrafal (bloco 1 + blocos A/P sem KEY); "
            "a peça pede 2 a 3 garrafais no total. Faça: intercale um bloco A ou P "
            "sem KEY pra abrir uma segunda posição" % capacidade
        ]
    return []


def planejar(
    tipos: Sequence[str],
    pps: float = 2.9,
    aceleracao: float = 1.45,
    palavras: Optional[Sequence[int]] = None,
    alvo_s: Optional[float] = None,
    limiares: Dict[str, Any] = LIMIARES,
) -> Dict[str, Any]:
    """Monta o plano de bloco a bloco (mínimo/máximo de palavras) e simula
    a linha do tempo.

    Com `palavras` (roteiro já contado): simula esse roteiro, pros mesmos
    números que o gate mediria depois.

    Sem `palavras`: simula DUAS vezes. A simulação no MÍNIMO de cada bloco
    (pior caso mais compacto) fica em `blocos_simulados_minimo` /
    `densidade_minimo`, só de referência. A recomendação final (`palavras`
    de cada `LinhaPlano`, `blocos_simulados`, `total_final_s`, `densidade`)
    usa o PONTO MÉDIO entre mínimo e máximo de cada bloco: é a simulação
    que se parece com um roteiro real, sem os blocos "A"/"P" saindo com
    0 palavras."""
    tipos = validar_tipos(tipos)
    if palavras is not None and len(palavras) != len(tipos):
        raise ValueError(
            "quantidade de --palavras (" + str(len(palavras)) + ") diferente da "
            "quantidade de --blocos (" + str(len(tipos)) + "). Faça: passe uma "
            "contagem de palavras para cada bloco do plano"
        )

    linhas: List[LinhaPlano] = []
    for i, tipo in enumerate(tipos, start=1):
        min_p = min_palavras_do_tipo(tipo, pps, aceleracao, limiares)
        max_p = max_palavras_do_tipo(tipo, pps, aceleracao, limiares)
        if palavras is not None:
            usada = palavras[i - 1]
        else:
            usada = medio_palavras_do_tipo(tipo, min_p, max_p)
        linhas.append(
            LinhaPlano(
                indice=i,
                tipo=tipo,
                min_palavras=min_p,
                max_palavras=max_p,
                palavras=usada,
                min_s=_minimo_segundos(tipo, limiares),
                max_s=_maximo_segundos(tipo, limiares),
            )
        )

    soma_min_palavras = sum(l.min_palavras for l in linhas)
    soma_max_palavras = sum(l.max_palavras for l in linhas)
    soma_min_s = sum(l.min_palavras / pps / aceleracao for l in linhas)
    soma_max_s = sum(l.max_palavras / pps / aceleracao for l in linhas)

    palavras_simulacao = [l.palavras for l in linhas]
    blocos_simulados = _simular(tipos, palavras_simulacao, pps, aceleracao)
    total_final_s = sum(b.duracao_final for b in blocos_simulados)
    densidade = calcular_densidade(blocos_simulados, limiares)
    avisos_vizinhos = checar_vizinhos_sem_insert(blocos_simulados, limiares)

    blocos_simulados_minimo: Optional[List[Bloco]] = None
    densidade_minimo: Optional[Dict[str, Dict[str, Any]]] = None
    total_final_s_minimo: Optional[float] = None
    avisos_vizinhos_minimo: Optional[List[str]] = None
    if palavras is None:
        palavras_minimo = [l.min_palavras for l in linhas]
        blocos_simulados_minimo = _simular(tipos, palavras_minimo, pps, aceleracao)
        total_final_s_minimo = sum(b.duracao_final for b in blocos_simulados_minimo)
        densidade_minimo = calcular_densidade(blocos_simulados_minimo, limiares)
        avisos_vizinhos_minimo = checar_vizinhos_sem_insert(blocos_simulados_minimo, limiares)

    alvo_cabe: Optional[bool] = None
    if alvo_s is not None:
        alvo_cabe = soma_min_s <= alvo_s <= soma_max_s

    avisos_plano = checar_ponte_do_plano(tipos)
    capacidade_garrafais = capacidade_de_garrafais(tipos)
    avisos_garrafais = checar_capacidade_de_garrafais(tipos)

    return {
        "linhas": linhas,
        "soma_min_palavras": soma_min_palavras,
        "soma_max_palavras": soma_max_palavras,
        "soma_min_s": soma_min_s,
        "soma_max_s": soma_max_s,
        "alvo_s": alvo_s,
        "alvo_cabe": alvo_cabe,
        "blocos_simulados": blocos_simulados,
        "total_final_s": total_final_s,
        "densidade": densidade,
        "blocos_simulados_minimo": blocos_simulados_minimo,
        "total_final_s_minimo": total_final_s_minimo,
        "densidade_minimo": densidade_minimo,
        "usando_palavras_informadas": palavras is not None,
        "avisos_plano": avisos_plano,
        "avisos_vizinhos": avisos_vizinhos,
        "avisos_vizinhos_minimo": avisos_vizinhos_minimo,
        "capacidade_garrafais": capacidade_garrafais,
        "avisos_garrafais": avisos_garrafais,
    }


def formatar_relatorio(resultado: Dict[str, Any]) -> str:
    """Texto pronto pra CLI (`planejar_blocos.py`), em PT-BR."""
    linhas_txt: List[str] = []
    linhas_txt.append(
        "CAPACIDADE DE GARRAFAIS: %d bloco(s) (bloco 1 + blocos A/P sem KEY)"
        % resultado.get("capacidade_garrafais", 0)
    )
    if resultado.get("avisos_garrafais"):
        for aviso in resultado["avisos_garrafais"]:
            linhas_txt.append("  AVISO: " + aviso)
    linhas_txt.append("")
    if resultado.get("avisos_plano"):
        linhas_txt.append("AVISOS DO PLANO:")
        for aviso in resultado["avisos_plano"]:
            linhas_txt.append("  - " + aviso)
        linhas_txt.append("")
    usando_palavras = resultado["usando_palavras_informadas"]
    rotulo_usada = "roteiro já contado (--palavras)" if usando_palavras else "ponto médio (recomendação final)"
    linhas_txt.append("PLANO POR BLOCO:")
    for l in resultado["linhas"]:
        nome_tipo = _NOMES_TIPO.get(l.tipo, l.tipo)
        linhas_txt.append(
            "  bloco %d (%s, %s): min %d palavras, max %d palavras (usado nesta simulação [%s]: %d)"
            % (l.indice, l.tipo, nome_tipo, l.min_palavras, l.max_palavras, rotulo_usada, l.palavras)
        )

    linhas_txt.append("")
    linhas_txt.append(
        "SOMA: min %d palavras (%.2fs finais), max %d palavras (%.2fs finais)"
        % (
            resultado["soma_min_palavras"], resultado["soma_min_s"],
            resultado["soma_max_palavras"], resultado["soma_max_s"],
        )
    )
    if resultado["alvo_s"] is not None:
        veredito = "cabe" if resultado["alvo_cabe"] else "não cabe"
        linhas_txt.append(
            "ALVO: %.2fs %s na faixa mín/máx da peça (%.2fs a %.2fs)"
            % (resultado["alvo_s"], veredito, resultado["soma_min_s"], resultado["soma_max_s"])
        )

    def _bloco_simulacao_txt(blocos: Sequence[Bloco]) -> List[str]:
        saida: List[str] = []
        for b in blocos:
            saida.append(
                "  bloco %d: início %.2fs, duração %.2fs (%d palavras)"
                % (b.numero, b.inicio_final, b.duracao_final, b.palavras)
            )
        return saida

    def _densidade_txt(densidade: Dict[str, Dict[str, Any]]) -> List[str]:
        saida: List[str] = []
        if not densidade:
            saida.append("  peça curta demais pra ter janela corpo/fecho medida")
        for nome, dados in densidade.items():
            base = "  %s (%.1fs a %.1fs): %.0f%%" % (nome, dados["ini_s"], dados["fim_s"], dados["fracao"] * 100)
            if "sugestao" in dados:
                base += ". Faça: " + dados["sugestao"]
            saida.append(base)
        return saida

    def _avisos_vizinhos_txt(avisos: Optional[Sequence[str]]) -> List[str]:
        saida: List[str] = []
        if avisos:
            saida.append("AVISOS (blocos vizinhos sem insert):")
            for aviso in avisos:
                saida.append("  - " + aviso)
        return saida

    if not usando_palavras:
        # Sem roteiro real: mostra as duas simulações (mínimo, so de
        # referência do pior caso; ponto médio, a recomendação final).
        linhas_txt.append("")
        linhas_txt.append("SIMULAÇÃO NO MÍNIMO DE CADA BLOCO (pior caso mais compacto, só referência):")
        linhas_txt.extend(_bloco_simulacao_txt(resultado["blocos_simulados_minimo"]))
        linhas_txt.append("  duração total final: %.2fs" % resultado["total_final_s_minimo"])
        linhas_txt.append("")
        linhas_txt.append("DENSIDADE DE INSERT POR JANELA (no mínimo):")
        linhas_txt.extend(_densidade_txt(resultado["densidade_minimo"]))
        avisos_txt = _avisos_vizinhos_txt(resultado.get("avisos_vizinhos_minimo"))
        if avisos_txt:
            linhas_txt.append("")
            linhas_txt.extend(avisos_txt)

        linhas_txt.append("")
        linhas_txt.append("SIMULAÇÃO NO PONTO MÉDIO (recomendação final, parecida com um roteiro real):")
        linhas_txt.extend(_bloco_simulacao_txt(resultado["blocos_simulados"]))
        linhas_txt.append("  duração total final: %.2fs" % resultado["total_final_s"])
        linhas_txt.append("")
        linhas_txt.append("DENSIDADE DE INSERT POR JANELA (recomendação final, ponto médio):")
        linhas_txt.extend(_densidade_txt(resultado["densidade"]))
        avisos_txt = _avisos_vizinhos_txt(resultado.get("avisos_vizinhos"))
        if avisos_txt:
            linhas_txt.append("")
            linhas_txt.extend(avisos_txt)
    else:
        linhas_txt.append("")
        linhas_txt.append("SIMULAÇÃO (" + rotulo_usada + "), início de cada bloco em segundos finais:")
        linhas_txt.extend(_bloco_simulacao_txt(resultado["blocos_simulados"]))
        linhas_txt.append("  duração total final: %.2fs" % resultado["total_final_s"])
        linhas_txt.append("")
        linhas_txt.append("DENSIDADE DE INSERT POR JANELA:")
        linhas_txt.extend(_densidade_txt(resultado["densidade"]))
        avisos_txt = _avisos_vizinhos_txt(resultado.get("avisos_vizinhos"))
        if avisos_txt:
            linhas_txt.append("")
            linhas_txt.extend(avisos_txt)

    return "\n".join(linhas_txt)
