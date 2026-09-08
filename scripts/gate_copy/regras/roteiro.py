#!/usr/bin/env python3
"""Regras sobre o roteiro como um todo: direções e âncoras de insert
(requisito 13), marca no gancho (requisito 6), tamanho de frase (requisito
15), sinais de envelhecimento (requisito 16), antítese paralela (requisito
17) e janelas de insert / duração total (requisito 18).

Compatibilidade: Python 3.9 (sem `X | None`; `from __future__ import
annotations` mais `Optional[X]`).
"""

from __future__ import annotations

import math
import re
from typing import List, Optional, Sequence, Tuple

from ..achados import AVISO, REPROVACAO, Achado
from ..leitura import Bloco, Conceito, Hook
from ..limiares import LIMIARES
from ..texto import (
    REGEX_ANTITESE,
    REGEX_DATA,
    REGEX_DIGITO_SOLTO,
    REGEX_DIRECAO_VAGA,
    REGEX_EDICAO,
    REGEX_PRECO,
    indice_sublista,
    normalizar,
    normalizar_codigo,
    palavras_normalizadas,
    remover_acentos,
)

def checar_direcoes(blocos: Sequence[Bloco]) -> List[Achado]:
    """Requisito 13: toda linha tem colchete e direção não vazia; âncora vaga reprova."""
    achados: List[Achado] = []
    for bloco in blocos:
        if not bloco.tem_colchete or not bloco.direcao.strip():
            achados.append(
                Achado(
                    REPROVACAO,
                    "roteiro bloco " + str(bloco.numero),
                    "linha sem colchete ou sem direção (seção 2 e requisito 13)",
                    acao="coloque a direção entre colchetes no início da linha",
                    medido=repr(bloco.linha_original),
                    limiar="direção entre colchetes, não vazia",
                )
            )
        if bloco.e_insert:
            ancora_palavras = palavras_normalizadas(bloco.ancora)
            vaga = REGEX_DIRECAO_VAGA.search(normalizar(bloco.ancora))
            if len(ancora_palavras) < 3 or vaga:
                achados.append(
                    Achado(
                        REPROVACAO,
                        "roteiro bloco " + str(bloco.numero),
                        "âncora de insert vaga demais pra casar por igualdade (seção 2)",
                        acao="descreva a âncora do insert com pelo menos 3 palavras específicas",
                        medido=repr(bloco.ancora),
                        limiar=">=3 palavras, sem termo generico",
                    )
                )
    return achados


def _logo_ancorado(hook: Optional[Hook]) -> bool:
    if hook is None:
        return False
    # `_ler_secoes_chave_valor` normaliza a CHAVE lida do arquivo (seção 21):
    # "logo_ancorado:" vira "logo ancorado" no dict (underscore não é letra
    # nem dígito, então normalizar() troca por espaço). Consulta pela
    # variante com espaço para bater com o que foi realmente guardado.
    return normalizar_codigo(hook.get("logo ancorado")) == "sim"


def checar_marca(conceito: Conceito, blocos: Sequence[Bloco], hooks: Sequence[Hook]) -> List[Achado]:
    """Requisito 6, seção 9 linhas 'marca' (R2.5, decisão 11)."""
    achados: List[Achado] = []
    marcas_norm = [palavras_normalizadas(m) for m in conceito.marcas if m]
    # Nota: round(logo_proibido_ate_s * aceleracao * pps) da 12.61 em ponto
    # flutuante (round -> 13). O contrato cita 12 como o padrao; escolhida a
    # leitura literal do numero do contrato (secao 3/9), com floor.
    limite_reprovacao = math.floor(
        LIMIARES["hook_logo_proibido_ate_s"] * conceito.aceleracao * conceito.pps
    )

    def checa(onde: str, fala: str, logo_ancorado: bool) -> None:
        """Casa cada marca contra a fala e reporta um Achado por trecho.
        Quando varias marcas casam em trechos que se sobrepoem (ex.:
        "Operacao Claude Code", "Claude Code" e "Claude" todas dentro do
        mesmo pedaco da fala, uma sendo substring da outra), so a mais longa
        e reportada: as mais curtas sao redundantes, ja se ve o problema
        inteiro na mais longa. Marcas em trechos que NAO se tocam
        continuam cada uma com o seu proprio Achado."""
        fala_p = palavras_normalizadas(fala)
        combinacoes: List[Tuple[int, int, List[str]]] = []
        for marca_p in marcas_norm:
            idx = indice_sublista(fala_p, marca_p)
            if idx is None:
                continue
            combinacoes.append((idx, idx + len(marca_p) - 1, marca_p))
        combinacoes.sort(key=lambda c: (c[0], -len(c[2])))

        trechos: List[Tuple[int, int, List[str]]] = []  # (fim_do_trecho, indice_da_melhor, melhor_marca)
        for idx, fim, marca_p in combinacoes:
            if trechos and idx <= trechos[-1][0]:
                fim_atual, idx_melhor, melhor_marca = trechos[-1]
                novo_fim = max(fim_atual, fim)
                if len(marca_p) > len(melhor_marca):
                    idx_melhor, melhor_marca = idx, marca_p
                trechos[-1] = (novo_fim, idx_melhor, melhor_marca)
            else:
                trechos.append((fim, idx, marca_p))

        for _fim, idx, marca_p in trechos:
            if idx < 3:
                # Nunca abre com marca, mesmo com logo ancorado (regra do
                # brief, valor de partida sem medicao propria).
                achados.append(
                    Achado(
                        REPROVACAO,
                        onde,
                        "marca começa dentro das 3 primeiras palavras (R2.5), reprova mesmo com logo ancorado",
                        acao="tire a marca das 3 primeiras palavras ou declare logo_ancorado: sim no hook",
                        medido="indice " + str(idx) + ": " + " ".join(marca_p),
                        limiar="indice >= 3",
                    )
                )
            elif idx < limite_reprovacao:
                if logo_ancorado:
                    achados.append(
                        Achado(
                            AVISO,
                            onde,
                            "marca dentro dos 3s com logo ancorado (decisão 11): a esteira confere a âncora",
                            acao="confirme com a esteira se a âncora do logo cobre este trecho da fala",
                            medido="indice " + str(idx) + ": " + " ".join(marca_p),
                            limiar="indice >= " + str(limite_reprovacao),
                        )
                    )
                else:
                    achados.append(
                        Achado(
                            REPROVACAO,
                            onde,
                            "marca dentro das primeiras " + str(limite_reprovacao)
                            + " palavras sem logo_ancorado: sim (R2.5)",
                            acao="tire a marca das " + str(limite_reprovacao)
                            + " primeiras palavras ou declare logo_ancorado: sim no hook",
                            medido="indice " + str(idx) + ": " + " ".join(marca_p),
                            limiar="indice >= " + str(limite_reprovacao),
                        )
                    )

    hook_a = next((h for h in hooks if normalizar(h.nome) == "hook a"), None)
    if blocos:
        checa("roteiro bloco 1 (hook A)", blocos[0].fala, _logo_ancorado(hook_a))
    for hook in hooks:
        checa(hook.nome, hook.fala, _logo_ancorado(hook))
    return achados


def checar_frases(blocos: Sequence[Bloco]) -> List[Achado]:
    """Requisito 15."""
    achados: List[Achado] = []
    max_p = LIMIARES["frase_max_palavras"]
    aviso_p = LIMIARES["frase_aviso_palavras"]
    for bloco in blocos:
        for frase in re.split(r"[.!?]", bloco.fala):
            n = len(frase.split())
            if n == 0:
                continue
            if n > max_p:
                achados.append(
                    Achado(
                        REPROVACAO, "roteiro bloco " + str(bloco.numero),
                        "frase com mais de " + str(max_p) + " palavras",
                        acao="quebre esta frase em duas, mais curtas",
                        medido=str(n), limiar="<= " + str(max_p),
                    )
                )
            elif n > aviso_p:
                achados.append(
                    Achado(
                        AVISO, "roteiro bloco " + str(bloco.numero),
                        "frase acima de " + str(aviso_p) + " palavras",
                        acao="considere quebrar esta frase em duas, mais curtas",
                        medido=str(n), limiar="<= " + str(aviso_p),
                    )
                )
    return achados


def checar_envelhecimento(conceito: Conceito, blocos: Sequence[Bloco]) -> List[Achado]:
    """Requisito 16."""
    achados: List[Achado] = []
    permite_dentro = conceito.campanha in ("carrinho", "lote")
    for bloco in blocos:
        textos = {"fala": bloco.fala, "LEAD": bloco.lead or "", "KEY": bloco.chave or ""}
        for rotulo, texto in textos.items():
            if not texto:
                continue
            n = normalizar(texto)
            achou = REGEX_DATA.search(n) or REGEX_PRECO.search(n) or REGEX_EDICAO.search(n)
            if achou:
                nivel = AVISO if permite_dentro else REPROVACAO
                achados.append(
                    Achado(
                        nivel, "roteiro bloco " + str(bloco.numero) + " (" + rotulo + ")",
                        "sinal de envelhecimento: data, preço ou edição numerada (decisões 6 e 19)",
                        acao="tire a data, preço ou edição numerada deste trecho",
                        medido=texto,
                    )
                )
        if REGEX_DIGITO_SOLTO.search(bloco.fala):
            achados.append(
                Achado(
                    AVISO, "roteiro bloco " + str(bloco.numero),
                    "algarismo solto na fala; numero por extenso na fala",
                    acao="escreva o número por extenso na fala deste bloco",
                    medido=bloco.fala,
                )
            )
    return achados


def _normalizar_com_pontuacao(texto: Optional[str]) -> str:
    """Como `normalizar`, mas preserva ".", "!", "," e "?": o padrão da
    antítese paralela (requisito 17) precisa da pontuação pra achar a
    fronteira entre as duas orações ("não é X. E Y.")."""
    if not texto:
        return ""
    t = remover_acentos(texto).lower()
    t = re.sub(r"[^0-9a-z\s.!?,]", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def checar_antitese(blocos: Sequence[Bloco], hooks: Sequence[Hook]) -> List[Achado]:
    """Requisito 17."""
    achados: List[Achado] = []
    for bloco in blocos:
        if REGEX_ANTITESE.search(_normalizar_com_pontuacao(bloco.fala)):
            achados.append(
                Achado(
                    AVISO, "roteiro bloco " + str(bloco.numero), "antítese paralela, cara de IA",
                    acao="reescreva a frase sem o padrão 'não é X, é Y'",
                    medido=bloco.fala,
                )
            )
    for hook in hooks:
        if REGEX_ANTITESE.search(_normalizar_com_pontuacao(hook.fala)):
            achados.append(
                Achado(
                    AVISO, hook.nome, "antítese paralela, cara de IA",
                    acao="reescreva a frase sem o padrão 'não é X, é Y'",
                    medido=hook.fala,
                )
            )
    return achados


def checar_janelas_de_insert(conceito: Conceito, blocos: Sequence[Bloco]) -> List[Achado]:
    """Requisito 18."""
    achados: List[Achado] = []
    if not blocos:
        return achados
    total_final = sum(b.duracao_final for b in blocos)

    ini1, fim1 = LIMIARES["retencao_insert_1_ini_s"], LIMIARES["retencao_insert_1_fim_s"]
    tem_insert_1 = any(b.e_insert and ini1 <= b.inicio_final <= fim1 for b in blocos)
    if not tem_insert_1:
        achados.append(
            Achado(
                AVISO, "roteiro", "nenhum insert começa na janela do primeiro insert (R3.2)",
                acao="posicione ou adicione um insert começando nesta janela",
                medido="janela vazia", limiar=str(ini1) + "s a " + str(fim1) + "s",
            )
        )

    exigido_acima = LIMIARES["retencao_insert_2_exigido_acima_de_s"]
    if total_final > exigido_acima:
        ini2, fim2 = LIMIARES["retencao_insert_2_ini_s"], LIMIARES["retencao_insert_2_fim_s"]
        tem_insert_2 = any(b.e_insert and ini2 <= b.inicio_final <= fim2 for b in blocos)
        if not tem_insert_2:
            achados.append(
                Achado(
                    AVISO, "roteiro", "nenhum insert começa na janela do segundo insert (R3.2)",
                    acao="posicione ou adicione um insert começando nesta janela",
                    medido="janela vazia", limiar=str(ini2) + "s a " + str(fim2) + "s",
                )
            )

    modo = normalizar_codigo(conceito.modo)
    campanha = normalizar_codigo(conceito.campanha)
    if campanha == "remarketing":
        faixa = (LIMIARES["duracao_total_remarketing_min_s"], LIMIARES["duracao_total_remarketing_max_s"])
    elif modo == "organico":
        faixa = (LIMIARES["duracao_total_organico_min_s"], LIMIARES["duracao_total_organico_max_s"])
    else:
        faixa = (LIMIARES["duracao_total_pago_min_s"], LIMIARES["duracao_total_pago_max_s"])
    if not (faixa[0] <= total_final <= faixa[1]):
        achados.append(
            Achado(
                AVISO, "roteiro", "duração total fora da faixa esperada (R6.1)",
                acao="ajuste o roteiro (corte ou acrescente fala) pra caber na faixa esperada",
                medido="%.2fs" % total_final, limiar=str(faixa[0]) + "s a " + str(faixa[1]) + "s",
            )
        )
    return achados


def _tempo_de_insert_na_janela(blocos: Sequence[Bloco], ini: float, fim: float) -> float:
    """Soma, em segundos, quanto tempo de insert (duração final) cai dentro
    da janela [ini, fim), pela sobreposição do intervalo do bloco."""
    total = 0.0
    for bloco in blocos:
        if not bloco.e_insert:
            continue
        b_ini = bloco.inicio_final
        b_fim = bloco.inicio_final + bloco.duracao_final
        sobreposicao = min(b_fim, fim) - max(b_ini, ini)
        if sobreposicao > 0:
            total += sobreposicao
    return total


def checar_densidade_insert(conceito: Conceito, blocos: Sequence[Bloco]) -> List[Achado]:
    """Requisito 18 (seção 9, "densidade de insert por janela", R3.4,
    aviso). Mede a fração do tempo coberto por insert nas janelas 'corpo'
    (3,0 a 15,0s) e 'fecho' (15,0s ao fim); a janela 'hook' (0 a 3s) fica
    isenta (aplica_a_partir_de_s)."""
    achados: List[Achado] = []
    if not blocos:
        return achados
    total_final = sum(b.duracao_final for b in blocos)
    minimo = LIMIARES["retencao_densidade_insert_min"]
    maximo = LIMIARES["retencao_densidade_insert_max"]

    corpo_ini = LIMIARES["retencao_janela_corpo_ini_s"]
    corpo_fim = LIMIARES["retencao_janela_corpo_fim_s"]
    fecho_ini = LIMIARES["retencao_janela_fecho_ini_s"]

    janelas: List[Tuple[str, float, float]] = []
    if total_final > corpo_ini:
        janelas.append(("corpo", corpo_ini, min(corpo_fim, total_final)))
    if total_final > fecho_ini:
        janelas.append(("fecho", fecho_ini, total_final))

    for nome, ini, fim in janelas:
        duracao_janela = fim - ini
        if duracao_janela <= 0:
            continue
        tempo_insert = _tempo_de_insert_na_janela(blocos, ini, fim)
        fracao = tempo_insert / duracao_janela
        if fracao < minimo or fracao > maximo:
            sugestao = (
                "mova ou tire um insert desta janela" if fracao > maximo
                else "intercale um bloco de apresentador sozinho entre dois inserts desta janela"
            )
            achados.append(
                Achado(
                    AVISO,
                    "roteiro janela " + nome,
                    "densidade de insert fora da faixa esperada (R3.4)",
                    acao=sugestao + "; alvo %.0f%% a %.0f%%" % (minimo * 100, maximo * 100),
                    medido="%.0f%%" % (fracao * 100),
                    limiar="%.0f%% a %.0f%%" % (minimo * 100, maximo * 100),
                )
            )
    return achados
