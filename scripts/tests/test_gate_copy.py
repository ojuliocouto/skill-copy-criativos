"""Suite de testes do gate de copy (TDD): cada teste muta UMA coisa do pacote
valido (`pacote_ok`) e confere que aparece a reprovacao (ou aviso) certa,
citando a secao do contrato em `references/formato-do-pacote.md`.

Roda com: /usr/bin/python3 -m pytest ~/.claude/skills/copy-criativos/scripts/tests -q
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional

import pytest

SCRIPTS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, SCRIPTS_DIR)

import gate_copy as gc  # noqa: E402

GATE_PATH = os.path.join(SCRIPTS_DIR, "gate_copy.py")
GATES_YAML_ESTEIRA = os.path.expanduser("~/creative-studio/config/gates.yaml")


# ---------------------------------------------------------------------------
# Pacote base valido (baseline): 10 blocos, ancorado no roteiro real do
# ad21v2, ajustado pra fechar limpo em todas as regras do contrato.
# ---------------------------------------------------------------------------

CONCEITO = """---
conceito: cinco_entregas
angulo: Tour / O que tem dentro (categoria Produto, biblioteca dos 78)
estrutura_invisivel: gancho curiosidade + promessa; beneficio funcional em lista; quebra de objecao de conhecimento; credibilidade por prova social; CTA com escassez real
avatar: dono de negocio que estuda I.A e ainda nao tem nada rodando
apresentador: Thales Laray
promessa: sair da Operacao Claude Code com cinco entregas prontas em dois dias
modo: pago
canal: reels
campanha: carrinho
objetivo: carrinho
marcas:
  - Operacao Claude Code
  - Claude Code
  - Claude
palavras_por_segundo: 2.9
aceleracao: 1.45
---

Brief: teste de fixture do gate de copy, pacote valido.
"""

ROTEIRO = """[thales de frente + lettering | LEAD: em dois dias | KEY: 5 ENTREGAS PRONTAS] Em dois dias você sai da Operação Claude Code com cinco entregas prontas.
[thales de frente + lettering | LEAD: entrega cinco | KEY: UM SQUAD] Cinco: um squad. Todos os seus times de inteligência artificial juntos, rodando sem ninguém puxando cada etapa manualmente todo dia.
[inserção de vídeo: claude criando uma skill do zero | LEAD: entrega quatro | KEY: SKILLS DO ZERO] Quatro: as suas próprias skills, criadas do zero. E skill é texto, se você sabe escrever como faz, você sabe montar direitinho.
[inserção de vídeo: prospecção buscando clientes sozinha | LEAD: entrega três | KEY: PROSPECÇÃO SOZINHA] Três: uma prospecção rodando sozinha, buscando cliente pra você todo santo dia, sempre no mesmo horário certinho.
[thales de frente pra câmera] E olha, nenhuma dessas entregas exige que você aprenda a programar, são coisas rodando no seu negócio de verdade.
[inserção de vídeo: quiz de qualificação sendo respondido | LEAD: entrega dois | KEY: QUIZ QUE FILTRA] Dois: um quiz de qualificação que filtra quem entra e manda o lead pronto direto pro seu WhatsApp.
[inserção de vídeo: página profissional publicada pelo claude | LEAD: entrega um | KEY: PÁGINA NO AR] E um: a sua página profissional no ar, publicada e hospedada pelo Claude, sem você mexer em nada disso.
[inserção de vídeo: pipoca de provas sociais de alunos] E não é à toa que oito mil pessoas já passaram pelos meus treinamentos ao longo desses anos todos.
[thales de frente pra câmera] São dois dias, do zero, na Operação Claude Code. É isso que você constrói no evento.
[thales de frente + lettering + logo da occ | LEAD: toca em saiba mais | KEY: GARANTE SEU INGRESSO] Então aproveita que ainda tem vaga, toca em saiba mais e garante seu ingresso. Vamos embora!
"""

HOOKS = """# Hooks: cinco_entregas

## Hook A
- id: curiosity
- tatica: Curiosity
- cluster: curiosidade
- cru: não
- fala: Em dois dias você sai da Operação Claude Code com cinco entregas prontas.
- ancora: dois dias
- lettering: LEAD: em dois dias | KEY: 5 ENTREGAS PRONTAS
- logo_ancorado: sim
- insert: nenhum

## Hook B
- id: contrarian
- tatica: Contrarian
- cluster: interrupcao_padrao
- cru: sim
- fala: Aprender I.A sozinho é a forma mais lenta de travar seu negócio.
- ancora: aprender i.a
- lettering: nenhum
- insert: nenhum

## Hook C
- id: myth_busting
- tatica: Myth Busting
- cluster: interrupcao_padrao
- cru: não
- fala: Você não precisa saber programar pra ter automação rodando no seu negócio essa semana.
- ancora: não precisa
- lettering: nenhum
- insert: nenhum
"""

GARRAFAIS = """# Garrafais: cinco_entregas

## G1
- palavra: 2 DIAS
- bloco: 1
- ancora: dois dias
- cor: casa
- papel: o numero da promessa, abre a peca marcando o prazo

## G2
- palavra: VERDADE
- bloco: 5
- ancora: negócio de verdade
- cor: quente
- papel: a virada de argumento
"""

LETTERINGS = """# Letterings: cinco_entregas

| bloco | LEAD | KEY | âncora na fala | forma | conteúdo/tempo |
|---|---|---|---|---|---|
| 1 | em dois dias | 5 ENTREGAS PRONTAS | prontas | placa_h1 | 2 |
| 2 | entrega cinco | UM SQUAD | squad | placa_h2 | 1/2 |
| 3 | entrega quatro | SKILLS DO ZERO | zero | placa_h4 | 2/3 |
| 4 | entrega três | PROSPECÇÃO SOZINHA | sozinha | coluna | 2 |
| 6 | entrega dois | QUIZ QUE FILTRA | filtra | placa_h1 | 2/3 |
| 7 | entrega um | PÁGINA NO AR | ar | coluna | 2/3 |
| 10 | toca em saiba mais | GARANTE SEU INGRESSO | garante | seta_cta | 3 |
"""

CTA = """# CTA: cinco_entregas

- modo: pago
- campanha: carrinho
- tipo: cta
- fala: Então aproveita que ainda tem vaga, toca em saiba mais e garante seu ingresso. Vamos embora!
- verbo_de_acao: toca, garante
- escassez: ainda tem vaga
- lettering: LEAD: toca em saiba mais | KEY: GARANTE SEU INGRESSO
- logo: Operação Claude Code, nome dito na fala do bloco anterior
"""

ASSETS = """# Assets: cinco_entregas

| # | âncora (do roteiro) | enquadramento | origem | referência | serve | ressalva |
|---|---|---|---|---|---|---|
| 1 | claude criando uma skill do zero | inteiro | criar:ui_html | terminal do Claude Code criando a skill, tipografia grande | sim | proposta: mockup HTML fiel do terminal, aprovar antes |
| 2 | prospecção buscando clientes sozinha | inteiro | doc | comentário do doc, link 1 | sim | |
| 3 | quiz de qualificação sendo respondido | inteiro | galeria | GalerIA, variante 5 | sim | |
| 4 | página profissional publicada pelo claude | inteiro | galeria | GalerIA, variante 8 | sim | |
| 5 | pipoca de provas sociais de alunos | inteiro | drive | pasta de depoimentos | sim | |
"""

MATRIZ = """# Matriz: cinco_entregas

- conceito: cinco_entregas
- canal: reels
- hooks: curiosity, contrarian, myth_busting
- legendas: laranja, amarela
- formatos: split, sem_avatar

| # | peça | hook | legenda | formato | avatar em tela |
|---|---|---|---|---|---|
| 1 | cinco_entregas_reels_split_curiosity_laranja_v1 | curiosity | laranja | split | sim |
| 2 | cinco_entregas_reels_split_curiosity_amarela_v1 | curiosity | amarela | split | sim |
| 3 | cinco_entregas_reels_split_contrarian_laranja_v1 | contrarian | laranja | split | sim |
| 4 | cinco_entregas_reels_split_contrarian_amarela_v1 | contrarian | amarela | split | sim |
| 5 | cinco_entregas_reels_split_myth_busting_laranja_v1 | myth_busting | laranja | split | sim |
| 6 | cinco_entregas_reels_split_myth_busting_amarela_v1 | myth_busting | amarela | split | sim |
| 7 | cinco_entregas_reels_sem_avatar_curiosity_laranja_v1 | curiosity | laranja | sem_avatar | não |
| 8 | cinco_entregas_reels_sem_avatar_curiosity_amarela_v1 | curiosity | amarela | sem_avatar | não |
| 9 | cinco_entregas_reels_sem_avatar_contrarian_laranja_v1 | contrarian | laranja | sem_avatar | não |
| 10 | cinco_entregas_reels_sem_avatar_contrarian_amarela_v1 | contrarian | amarela | sem_avatar | não |
| 11 | cinco_entregas_reels_sem_avatar_myth_busting_laranja_v1 | myth_busting | laranja | sem_avatar | não |
| 12 | cinco_entregas_reels_sem_avatar_myth_busting_amarela_v1 | myth_busting | amarela | sem_avatar | não |
"""

BASE: Dict[str, str] = {
    "conceito.md": CONCEITO,
    "roteiro.txt": ROTEIRO,
    "hooks.md": HOOKS,
    "garrafais.md": GARRAFAIS,
    "letterings.md": LETTERINGS,
    "cta.md": CTA,
    "assets.md": ASSETS,
    "matriz.md": MATRIZ,
}

# gates.yaml real da esteira, se existir; senao roda so com os padroes de
# LIMIARES embutidos no gate_copy.py.
_GATES_DADOS: Optional[Dict] = None
if os.path.isfile(GATES_YAML_ESTEIRA):
    import yaml as _yaml

    with open(GATES_YAML_ESTEIRA, "r", encoding="utf-8") as _f:
        _GATES_DADOS = _yaml.safe_load(_f)


def escrever_pacote(
    diretorio: str,
    overrides: Optional[Dict[str, str]] = None,
    remover: Optional[List[str]] = None,
) -> str:
    conteudo = dict(BASE)
    conteudo.update(overrides or {})
    for nome in remover or []:
        conteudo.pop(nome, None)
    for nome, texto in conteudo.items():
        with open(os.path.join(diretorio, nome), "w", encoding="utf-8") as f:
            f.write(texto)
    return diretorio


def rodar(tmp_path, overrides=None, remover=None):
    escrever_pacote(str(tmp_path), overrides, remover)
    return gc.rodar(str(tmp_path), gates_dados=_GATES_DADOS)


def tem_reprovacao_contendo(resultado, trecho: str) -> bool:
    return any(trecho in r for r in resultado["reprovacoes"])


def tem_aviso_contendo(resultado, trecho: str) -> bool:
    return any(trecho in a for a in resultado["avisos"])


# ---------------------------------------------------------------------------
# Teste 1: pacote valido, zero reprovacoes
# ---------------------------------------------------------------------------


def test_pacote_valido_zero_reprovacoes(tmp_path):
    resultado = rodar(tmp_path)
    assert resultado["reprovacoes"] == []
    assert len(resultado["blocos"]) == 10


# ---------------------------------------------------------------------------
# Duracoes (secao 9, requisito 14)
# ---------------------------------------------------------------------------


def test_bloco_com_insert_curto_demais_reprova(tmp_path):
    roteiro = ROTEIRO.replace(
        "[inserção de vídeo: claude criando uma skill do zero | LEAD: entrega quatro | KEY: SKILLS DO ZERO] "
        "Quatro: as suas próprias skills, criadas do zero. E skill é texto, se você sabe escrever "
        "como faz, você sabe montar direitinho.",
        "[inserção de vídeo: claude criando uma skill do zero | LEAD: entrega quatro | KEY: SKILLS DO ZERO] "
        "Quatro: skills do zero.",
    )
    resultado = rodar(tmp_path, {"roteiro.txt": roteiro})
    assert resultado["reprovacoes"] == [
        r for r in resultado["reprovacoes"] if "duração final abaixo do mínimo de insert" in r
    ]
    assert tem_reprovacao_contendo(resultado, "roteiro bloco 3")
    assert tem_reprovacao_contendo(resultado, "duração final abaixo do mínimo de insert")


def test_cta_acima_do_teto_avisa(tmp_path):
    """Contrato seção 6: bloco de CTA com duração final acima de
    `fechamento.janela_final_max_s` (5,0s) avisa, não reprova."""
    fala_longa = (
        "Então aproveita que ainda tem vaga, toca em saiba mais e garante. "
        "Seu ingresso quentinho agora mesmo, rapidinho, sem enrolação nenhuma de verdade absoluta total. "
        "Vamos embora!"
    )
    overrides = {
        "roteiro.txt": ROTEIRO.replace(
            "Então aproveita que ainda tem vaga, toca em saiba mais e garante seu ingresso. Vamos embora!",
            fala_longa,
        ),
        "cta.md": CTA.replace(
            "- fala: Então aproveita que ainda tem vaga, toca em saiba mais e garante seu ingresso. Vamos embora!",
            "- fala: " + fala_longa,
        ),
    }
    resultado = rodar(tmp_path, overrides)
    assert resultado["reprovacoes"] == []
    assert tem_aviso_contendo(resultado, "duração final do CTA acima do teto")


def test_bloco_sem_insert_sem_key_acima_do_maximo_reprova(tmp_path):
    roteiro = ROTEIRO.replace(
        "São dois dias, do zero, na Operação Claude Code. É isso que você constrói no evento.",
        "São dois dias, do zero, na Operação Claude Code. É isso que você constrói no evento. Mesmo que "
        "você nunca tenha criado nada antes na vida inteira toda. Você consegue mesmo assim com certeza "
        "absoluta, sem trava nenhuma, rapidinho de verdade, todo santo dia.",
    )
    resultado = rodar(tmp_path, {"roteiro.txt": roteiro})
    assert len(resultado["reprovacoes"]) == 1
    assert tem_reprovacao_contendo(resultado, "roteiro bloco 9")
    assert tem_reprovacao_contendo(resultado, "bloco sem insert e sem KEY acima do máximo")


# ---------------------------------------------------------------------------
# Letterings (secao 5, requisito 8)
# ---------------------------------------------------------------------------


def test_vizinhos_sem_insert_com_key_ainda_avisa(tmp_path):
    """Contrato seção 9 (R3.3): a soma de blocos vizinhos sem insert é
    AVISO independente de KEY (o lettering cobre só parte do bloco). Os
    blocos 1 e 2 (sem insert; bloco 1 e 2 têm KEY) já somam acima do
    máximo na baseline."""
    resultado = rodar(tmp_path)
    assert tem_aviso_contendo(resultado, "roteiro blocos 1 e 2")
    assert tem_aviso_contendo(resultado, "blocos vizinhos sem insert somam acima do máximo")


def test_key_com_palavra_fora_da_fala_reprova(tmp_path):
    overrides = {
        "roteiro.txt": ROTEIRO.replace("KEY: UM SQUAD]", "KEY: UM SQUAD TURBO]"),
        "letterings.md": LETTERINGS.replace("| UM SQUAD |", "| UM SQUAD TURBO |"),
    }
    resultado = rodar(tmp_path, overrides)
    assert len(resultado["reprovacoes"]) == 1
    assert tem_reprovacao_contendo(resultado, "palavra do KEY não está na fala do bloco")
    assert tem_reprovacao_contendo(resultado, "turbo")


def test_key_com_3_palavras_de_conteudo_fora_do_cta_reprova(tmp_path):
    # Correcao do Julio: so palavra de CONTEUDO conta pro limite (algarismo e
    # palavra funcional "um" nao contam). "SQUAD RODANDO JUNTOS" tem 3
    # palavras de conteudo, todas na fala, isolando so essa reprovacao.
    overrides = {
        "roteiro.txt": ROTEIRO.replace("KEY: UM SQUAD]", "KEY: SQUAD RODANDO JUNTOS]"),
        "letterings.md": LETTERINGS.replace("| UM SQUAD |", "| SQUAD RODANDO JUNTOS |"),
    }
    resultado = rodar(tmp_path, overrides)
    assert len(resultado["reprovacoes"]) == 1
    assert tem_reprovacao_contendo(resultado, "KEY com mais palavras de conteúdo que o permitido")


def test_key_aprovado_no_piloto_com_palavra_funcional_nao_reprova(tmp_path):
    # "SKILLS DO ZERO", "QUIZ QUE FILTRA" e "PAGINA NO AR" (aprovados no
    # piloto) tem 2 palavras de CONTEUDO cada; "do", "que" e "no" sao
    # funcionais e nao contam pro limite (correcao do Julio, secao 5).
    resultado = rodar(tmp_path)
    assert not tem_reprovacao_contendo(resultado, "KEY com mais palavras de conteúdo")


def test_key_com_3_palavras_no_bloco_do_cta_nao_reprova(tmp_path):
    # "GARANTE SEU INGRESSO" no bloco do CTA aceita 3 (verbo + objeto, decisao 7).
    resultado = rodar(tmp_path)
    assert not tem_reprovacao_contendo(resultado, "roteiro/letterings bloco 10")


def test_forma_placa_generica_reprova(tmp_path):
    """Contrato seção 5: `forma` aceita placa_h1/h2/h4, não `placa` sozinha."""
    overrides = {"letterings.md": LETTERINGS.replace("| placa_h1 | 2 |\n", "| placa | 2 |\n", 1)}
    resultado = rodar(tmp_path, overrides)
    assert tem_reprovacao_contendo(resultado, "declare h1, h2 ou h4")


def test_forma_fora_do_dominio_reprova(tmp_path):
    overrides = {"letterings.md": LETTERINGS.replace("| coluna | 2 |\n", "| banner | 2 |\n", 1)}
    resultado = rodar(tmp_path, overrides)
    assert tem_reprovacao_contendo(resultado, "forma de lettering fora do domínio")


def test_placa_h1_vizinho_de_placa_h2_nao_reprova_rodizio(tmp_path):
    """Blocos 1 e 2 já usam placa_h1 e placa_h2 na baseline: sub-formas
    diferentes da mesma placa passam no rodízio (seção 5)."""
    resultado = rodar(tmp_path)
    assert not tem_aviso_contendo(resultado, "mesma forma de lettering em blocos vizinhos")


def test_carimbo_em_bloco_sem_insert_avisa(tmp_path):
    """Bloco 2 não tem insert (apresentador + lettering); carimbo é
    lettering de apoio, só serve em bloco com insert (seção 5)."""
    overrides = {"letterings.md": LETTERINGS.replace("| placa_h2 | 1/2 |\n", "| carimbo | 1/2 |\n", 1)}
    resultado = rodar(tmp_path, overrides)
    assert tem_aviso_contendo(resultado, "carimbo é lettering de apoio, só em bloco com insert")


def test_conteudo_tempo_bate_nao_avisa(tmp_path):
    """Baseline já declara "conteúdo/tempo" corretos (seção 5, correção C):
    nenhum aviso de coluna errada."""
    resultado = rodar(tmp_path)
    assert not tem_aviso_contendo(resultado, "coluna conteúdo/tempo")


def test_conteudo_tempo_numero_unico_errado_avisa(tmp_path):
    overrides = {
        # bloco 1: "5 ENTREGAS PRONTAS" e conteudo=2, tempo=2; declarar 3 erra os dois
        "letterings.md": LETTERINGS.replace(
            "| 5 ENTREGAS PRONTAS | prontas | placa_h1 | 2 |",
            "| 5 ENTREGAS PRONTAS | prontas | placa_h1 | 3 |",
        ),
    }
    resultado = rodar(tmp_path, overrides)
    assert tem_aviso_contendo(resultado, "coluna conteúdo/tempo não bate com o calculado")
    assert tem_aviso_contendo(resultado, "declarado 3; calculado 2/2")


def test_conteudo_tempo_a_b_errado_avisa(tmp_path):
    overrides = {
        # bloco 3: "SKILLS DO ZERO" e conteudo=2, tempo=3; declarar 2/2 erra o tempo
        "letterings.md": LETTERINGS.replace(
            "| SKILLS DO ZERO | zero | placa_h4 | 2/3 |",
            "| SKILLS DO ZERO | zero | placa_h4 | 2/2 |",
        ),
    }
    resultado = rodar(tmp_path, overrides)
    assert tem_aviso_contendo(resultado, "coluna conteúdo/tempo não bate com o calculado")
    assert tem_aviso_contendo(resultado, "declarado 2/2; calculado 2/3")


def test_conteudo_tempo_a_b_correto_nao_avisa(tmp_path):
    resultado = rodar(tmp_path)
    assert not tem_aviso_contendo(resultado, "SKILLS DO ZERO")


def test_conteudo_tempo_formato_invalido_avisa(tmp_path):
    overrides = {
        "letterings.md": LETTERINGS.replace(
            "| 5 ENTREGAS PRONTAS | prontas | placa_h1 | 2 |",
            "| 5 ENTREGAS PRONTAS | prontas | placa_h1 | dois |",
        ),
    }
    resultado = rodar(tmp_path, overrides)
    assert tem_aviso_contendo(resultado, "coluna conteúdo/tempo fora do formato")


def test_conteudo_tempo_em_branco_nao_avisa(tmp_path):
    """Compatibilidade: pacote sem a coluna (célula em branco) não avisa."""
    overrides = {
        "letterings.md": LETTERINGS.replace(
            "| 5 ENTREGAS PRONTAS | prontas | placa_h1 | 2 |",
            "| 5 ENTREGAS PRONTAS | prontas | placa_h1 |  |",
        ),
    }
    resultado = rodar(tmp_path, overrides)
    assert not tem_aviso_contendo(resultado, "coluna conteúdo/tempo")


def test_carimbo_em_bloco_com_insert_nao_avisa(tmp_path):
    """Bloco 3 tem insert (claude criando uma skill do zero); carimbo não
    avisa nesse caso."""
    overrides = {"letterings.md": LETTERINGS.replace("| placa_h4 | 2/3 |\n", "| carimbo | 2/3 |\n", 1)}
    resultado = rodar(tmp_path, overrides)
    assert not tem_aviso_contendo(resultado, "carimbo é lettering de apoio")


# ---------------------------------------------------------------------------
# Hooks (secao 3, requisitos 6 e 7)
# ---------------------------------------------------------------------------


def test_hook_com_cluster_promocional_em_objetivo_frio_reprova(tmp_path):
    overrides = {
        "conceito.md": CONCEITO.replace("objetivo: carrinho", "objetivo: frio"),
        "hooks.md": HOOKS.replace(
            "- id: contrarian\n- tatica: Contrarian\n- cluster: interrupcao_padrao",
            "- id: fomo\n- tatica: FOMO\n- cluster: promocional",
        ),
        "matriz.md": MATRIZ.replace("contrarian", "fomo"),
    }
    resultado = rodar(tmp_path, overrides)
    assert len(resultado["reprovacoes"]) == 1
    assert tem_reprovacao_contendo(resultado, "Hook B")
    assert tem_reprovacao_contendo(resultado, "cluster fora do objetivo frio")


def test_hook_sem_cru_reprova(tmp_path):
    overrides = {
        "hooks.md": HOOKS.replace(
            "## Hook B\n- id: contrarian\n- tatica: Contrarian\n- cluster: interrupcao_padrao\n- cru: sim",
            "## Hook B\n- id: contrarian\n- tatica: Contrarian\n- cluster: interrupcao_padrao\n- cru: não",
        )
    }
    resultado = rodar(tmp_path, overrides)
    assert len(resultado["reprovacoes"]) == 1
    assert tem_reprovacao_contendo(resultado, "nenhum hook cru: sim")


def test_hook_a_com_fala_diferente_do_bloco_1_reprova(tmp_path):
    overrides = {
        "hooks.md": HOOKS.replace(
            "- fala: Em dois dias você sai da Operação Claude Code com cinco entregas prontas.\n- ancora: dois dias",
            "- fala: Em dois dias você sai da Operação Claude Code com cinco entregas boas.\n- ancora: dois dias",
        )
    }
    resultado = rodar(tmp_path, overrides)
    assert len(resultado["reprovacoes"]) == 1
    assert tem_reprovacao_contendo(resultado, "Hook A tem que ter a MESMA fala do bloco 1")


def test_ancora_do_hook_fora_das_4_primeiras_palavras_reprova(tmp_path):
    overrides = {"hooks.md": HOOKS.replace("- ancora: não precisa", "- ancora: programar")}
    resultado = rodar(tmp_path, overrides)
    assert len(resultado["reprovacoes"]) == 1
    assert tem_reprovacao_contendo(resultado, "Hook C")
    assert tem_reprovacao_contendo(resultado, "âncora do problema/promessa fora das primeiras palavras")


def test_frase_de_apresentacao_no_hook_reprova(tmp_path):
    overrides = {
        "hooks.md": HOOKS.replace(
            "- fala: Você não precisa saber programar pra ter automação rodando no seu negócio essa semana.\n"
            "- ancora: não precisa",
            "- fala: Aqui é o não precisa programar pra ter automação rodando hoje.\n- ancora: não precisa",
        )
    }
    resultado = rodar(tmp_path, overrides)
    assert len(resultado["reprovacoes"]) == 1
    assert tem_reprovacao_contendo(resultado, "Hook C")
    assert tem_reprovacao_contendo(resultado, "frase de apresentação no hook")


# ---------------------------------------------------------------------------
# Marca (secao 9, requisito 6)
# ---------------------------------------------------------------------------


def test_marca_nas_3_primeiras_palavras_reprova(tmp_path):
    overrides = {
        "roteiro.txt": ROTEIRO.replace(
            "Em dois dias você sai da Operação Claude Code com cinco entregas prontas.",
            "Claude dois dias você sai da Operação Claude Code com cinco entregas prontas.",
            1,
        ),
        "hooks.md": HOOKS.replace(
            "- fala: Em dois dias você sai da Operação Claude Code com cinco entregas prontas.\n- ancora: dois dias",
            "- fala: Claude dois dias você sai da Operação Claude Code com cinco entregas prontas.\n- ancora: dois dias",
        ),
    }
    resultado = rodar(tmp_path, overrides)
    assert len(resultado["reprovacoes"]) == 2  # roteiro bloco 1 + Hook A, mesmo achado
    for r in resultado["reprovacoes"]:
        assert "marca começa dentro das 3 primeiras palavras" in r


def test_marcas_sobrepostas_colapsam_no_aviso_mais_longo(tmp_path):
    """"Operação Claude Code", "Claude Code" e "Claude" casam no mesmo
    trecho do bloco 1 (baseline nao alterada, Hook A com logo_ancorado:
    sim): sem colapso, virariam 3 avisos por fonte (roteiro bloco 1 + Hook
    A = 6). Com o colapso por sobreposicao, cada fonte reporta so a marca
    mais longa (1 aviso)."""
    resultado = rodar(tmp_path)
    avisos_marca = [
        a for a in resultado["avisos"] if "com logo ancorado (decisão 11)" in a
    ]
    assert len(avisos_marca) == 2  # roteiro bloco 1 (hook A) + Hook A, uma fonte cada
    for aviso in avisos_marca:
        assert "indice 6: operacao claude code" in aviso
        assert "indice 7" not in aviso


def test_marca_sem_logo_ancorado_reprova(tmp_path):
    """Requisito novo (contrato seção 3, R2.5): sem `logo_ancorado: sim` no
    Hook A, a marca dentro dos 3s do bloco 1/hooks vira REPROVAÇÃO, não
    aviso."""
    hooks_sem_declaracao = HOOKS.replace("- logo_ancorado: sim\n", "")
    resultado = rodar(tmp_path, {"hooks.md": hooks_sem_declaracao})
    assert tem_reprovacao_contendo(resultado, "roteiro bloco 1 (hook A)")
    assert tem_reprovacao_contendo(resultado, "sem logo_ancorado: sim (R2.5)")
    assert not tem_aviso_contendo(resultado, "com logo ancorado (decisão 11)")


def test_marca_nas_3_primeiras_reprova_mesmo_com_logo_ancorado(tmp_path):
    """Marca nas 3 primeiras palavras reprova SEMPRE, mesmo com
    `logo_ancorado: sim` declarado (regra do brief: nunca abre com marca)."""
    overrides = {
        "roteiro.txt": ROTEIRO.replace(
            "Em dois dias você sai da Operação Claude Code com cinco entregas prontas.",
            "Claude dois dias você sai da Operação Claude Code com cinco entregas prontas.",
            1,
        ),
        "hooks.md": HOOKS.replace(
            "- fala: Em dois dias você sai da Operação Claude Code com cinco entregas prontas.\n- ancora: dois dias",
            "- fala: Claude dois dias você sai da Operação Claude Code com cinco entregas prontas.\n- ancora: dois dias",
        ),
    }
    resultado = rodar(tmp_path, overrides)
    reprovacoes_marca = [r for r in resultado["reprovacoes"] if "3 primeiras palavras" in r]
    assert len(reprovacoes_marca) == 2  # roteiro bloco 1 + Hook A
    for r in reprovacoes_marca:
        assert "mesmo com logo ancorado" in r


# ---------------------------------------------------------------------------
# CTA (secao 6, requisito 10)
# ---------------------------------------------------------------------------


def test_cta_pago_sem_verbo_reprova(tmp_path):
    overrides = {
        "roteiro.txt": ROTEIRO.replace(
            "[thales de frente + lettering + logo da occ | LEAD: toca em saiba mais | KEY: GARANTE SEU INGRESSO] "
            "Então aproveita que ainda tem vaga, toca em saiba mais e garante seu ingresso. Vamos embora!",
            "[thales de frente + lettering + logo da occ | LEAD: vaga liberada | KEY: VAGA LIBERADA] "
            "Então tem vaga liberada agora e o link tá na bio pra você conferir. Vamos nessa!",
        ),
        "cta.md": CTA.replace(
            "- fala: Então aproveita que ainda tem vaga, toca em saiba mais e garante seu ingresso. Vamos embora!",
            "- fala: Então tem vaga liberada agora e o link tá na bio pra você conferir. Vamos nessa!",
        ),
        "letterings.md": LETTERINGS.replace(
            "| toca em saiba mais | GARANTE SEU INGRESSO |", "| vaga liberada | VAGA LIBERADA |"
        ),
    }
    resultado = rodar(tmp_path, overrides)
    assert len(resultado["reprovacoes"]) == 1
    assert tem_reprovacao_contendo(resultado, "CTA vago")


def test_cta_carrinho_sem_escassez_reprova(tmp_path):
    overrides = {
        "roteiro.txt": ROTEIRO.replace(
            "[thales de frente + lettering + logo da occ | LEAD: toca em saiba mais | KEY: GARANTE SEU INGRESSO] "
            "Então aproveita que ainda tem vaga, toca em saiba mais e garante seu ingresso. Vamos embora!",
            "[thales de frente + lettering + logo da occ | LEAD: toca em saiba mais | KEY: GARANTE PARTICIPAÇÃO] "
            "Então toca em saiba mais e garante sua participação especial nessa turma de agora. Vamos embora!",
        ),
        "cta.md": CTA.replace(
            "- fala: Então aproveita que ainda tem vaga, toca em saiba mais e garante seu ingresso. Vamos embora!",
            "- fala: Então toca em saiba mais e garante sua participação especial nessa turma de agora. Vamos embora!",
        ),
        "letterings.md": LETTERINGS.replace(
            "| toca em saiba mais | GARANTE SEU INGRESSO |", "| toca em saiba mais | GARANTE PARTICIPAÇÃO |"
        ),
    }
    resultado = rodar(tmp_path, overrides)
    assert len(resultado["reprovacoes"]) == 1
    assert tem_reprovacao_contendo(resultado, "campanha carrinho exige escassez legítima")


def test_cta_frio_com_escassez_reprova(tmp_path):
    # So muda campanha/objetivo pra frio; o CTA da baseline ja tem "vaga" e
    # "ingresso" (escassez), proibida em frio (R6.4).
    overrides = {
        "conceito.md": CONCEITO.replace("campanha: carrinho", "campanha: frio").replace(
            "objetivo: carrinho", "objetivo: frio"
        )
    }
    resultado = rodar(tmp_path, overrides)
    assert len(resultado["reprovacoes"]) == 1
    assert tem_reprovacao_contendo(resultado, "campanha frio proibe escassez, preço ou data")


def test_cta_organico_com_toca_em_reprova(tmp_path):
    overrides = {
        "conceito.md": CONCEITO.replace("modo: pago", "modo: organico"),
        "cta.md": CTA.replace("- modo: pago", "- modo: organico").replace(
            "- tipo: cta", "- tipo: loop\n- loop: fecha o ciclo"
        ),
        "roteiro.txt": ROTEIRO.replace("KEY: GARANTE SEU INGRESSO]", "KEY: GARANTE INGRESSO]"),
        "letterings.md": LETTERINGS.replace(
            "| toca em saiba mais | GARANTE SEU INGRESSO |", "| toca em saiba mais | GARANTE INGRESSO |"
        ),
    }
    resultado = rodar(tmp_path, overrides)
    assert len(resultado["reprovacoes"]) == 1
    assert tem_reprovacao_contendo(resultado, "orgânico proibe")
    assert tem_reprovacao_contendo(resultado, "toca em")


def test_cta_organico_pergunta_sem_interrogacao_reprova(tmp_path):
    nova_fala = "Sera que voce vai perder essa chance incrivel de virar o jogo com o seu negocio."
    overrides = {
        "conceito.md": CONCEITO.replace("modo: pago", "modo: organico"),
        "roteiro.txt": ROTEIRO.replace(
            "[thales de frente + lettering + logo da occ | LEAD: toca em saiba mais | KEY: GARANTE SEU INGRESSO] "
            "Então aproveita que ainda tem vaga, toca em saiba mais e garante seu ingresso. Vamos embora!",
            "[thales de frente + lettering + logo da occ | LEAD: sera que voce | KEY: SERA QUE VOCE] " + nova_fala,
        ),
        "cta.md": CTA.replace("- modo: pago", "- modo: organico")
        .replace("- tipo: cta", "- tipo: pergunta")
        .replace(
            "- fala: Então aproveita que ainda tem vaga, toca em saiba mais e garante seu ingresso. Vamos embora!",
            "- fala: " + nova_fala,
        ),
        "letterings.md": LETTERINGS.replace(
            "| toca em saiba mais | GARANTE SEU INGRESSO |", "| sera que voce | SERA QUE VOCE |"
        ),
    }
    resultado = rodar(tmp_path, overrides)
    assert len(resultado["reprovacoes"]) == 1
    assert tem_reprovacao_contendo(resultado, "tipo pergunta exige fala terminando com ?")


# ---------------------------------------------------------------------------
# Ponte antes do CTA (regra nova do dono da metodologia)
# ---------------------------------------------------------------------------


def test_cta_sem_ponte_reprova(tmp_path):
    """Baseline tem ponte no bloco 9 ("É isso que você constrói no
    evento."); tirando o marcador, o CTA (modo pago, tipo cta) reprova por
    falta de ponte."""
    overrides = {
        "roteiro.txt": ROTEIRO.replace(
            "São dois dias, do zero, na Operação Claude Code. É isso que você constrói no evento.",
            "São dois dias, do zero, com a Operação Claude Code, sem trava nenhuma.",
        )
    }
    resultado = rodar(tmp_path, overrides)
    assert len(resultado["reprovacoes"]) == 1
    assert tem_reprovacao_contendo(resultado, "CTA sem ponte")


def test_cta_com_ponte_no_bloco_anterior_nao_reprova(tmp_path):
    resultado = rodar(tmp_path)
    assert not tem_reprovacao_contendo(resultado, "CTA sem ponte")


def test_campo_ponte_declarado_e_valido_nao_reprova(tmp_path):
    overrides = {
        "cta.md": CTA + '- ponte: bloco 9, "É isso que você constrói no evento"\n',
    }
    resultado = rodar(tmp_path, overrides)
    assert not tem_reprovacao_contendo(resultado, "campo ponte")


def test_campo_ponte_declarado_com_frase_que_nao_bate_reprova(tmp_path):
    overrides = {
        "cta.md": CTA + '- ponte: bloco 9, "isso não está na fala desse bloco"\n',
    }
    resultado = rodar(tmp_path, overrides)
    assert tem_reprovacao_contendo(resultado, "frase do campo ponte não está na fala do bloco citado")


def test_campo_ponte_bloco_inexistente_reprova(tmp_path):
    overrides = {
        "cta.md": CTA + '- ponte: bloco 99, "qualquer coisa"\n',
    }
    resultado = rodar(tmp_path, overrides)
    assert tem_reprovacao_contendo(resultado, "campo ponte cita bloco inexistente")


def test_ponte_com_deslocamento_ate_a_casa_do_cliente_nao_reprova(tmp_path):
    """Marcadores novos de ponte (produto/serviço com visita até a casa do
    cliente, achado do teste3 Casa Medida): "eu levo até", "eu vou até",
    "na sua casa" etc. valem como ponte antes do CTA."""
    overrides = {
        "roteiro.txt": ROTEIRO.replace(
            "São dois dias, do zero, na Operação Claude Code. É isso que você constrói no evento.",
            "São dois dias, do zero, na Operação Claude Code. É esse desenho que eu levo até a "
            "sua casa depois da aula.",
        )
    }
    resultado = rodar(tmp_path, overrides)
    assert not tem_reprovacao_contendo(resultado, "CTA sem ponte")
    assert not tem_reprovacao_contendo(resultado, "CTA sem bloco de oferta")


# ---------------------------------------------------------------------------
# Bloco de oferta obrigatório antes do CTA (item B da correção de gaps,
# regra do dono da metodologia): entre a prova e o CTA precisa existir um
# bloco que nomeie a oferta e diga a entrega.
# ---------------------------------------------------------------------------


def test_baseline_tem_bloco_de_oferta_nao_reprova(tmp_path):
    resultado = rodar(tmp_path)
    assert not tem_reprovacao_contendo(resultado, "CTA sem bloco de oferta")


def test_sem_nome_da_oferta_reprova(tmp_path):
    """Bloco 9 tem entrega ("do zero") mas, sem o nome da marca, não
    nomeia a oferta: reprova."""
    overrides = {
        "roteiro.txt": ROTEIRO.replace(
            "São dois dias, do zero, na Operação Claude Code. É isso que você constrói no evento.",
            "São dois dias, do zero. É isso que você constrói no evento.",
        ),
    }
    resultado = rodar(tmp_path, overrides)
    assert tem_reprovacao_contendo(resultado, "CTA sem bloco de oferta")


def test_sem_marcador_de_entrega_reprova(tmp_path):
    """Bloco 9 nomeia a marca mas não carrega nenhum marcador de
    MARCADORES_DE_OFERTA: reprova."""
    overrides = {
        "roteiro.txt": ROTEIRO.replace(
            "São dois dias, do zero, na Operação Claude Code. É isso que você constrói no evento.",
            "Isso tudo é a Operação Claude Code, no maior estilo possível.",
        ),
    }
    resultado = rodar(tmp_path, overrides)
    assert tem_reprovacao_contendo(resultado, "CTA sem bloco de oferta")


def test_oferta_usa_campo_oferta_do_conceito_quando_declarado(tmp_path):
    """Com `oferta:` declarado em conceito.md, o nome procurado é esse
    campo, não a primeira marca."""
    overrides = {
        "conceito.md": CONCEITO.replace(
            "marcas:\n  - Operacao Claude Code",
            "oferta: Imersao Dois Dias\nmarcas:\n  - Operacao Claude Code",
        ),
        "roteiro.txt": ROTEIRO.replace(
            "São dois dias, do zero, na Operação Claude Code. É isso que você constrói no evento.",
            "São dois dias, do zero, na Imersão Dois Dias. É isso que você constrói no evento.",
        ),
    }
    resultado = rodar(tmp_path, overrides)
    assert not tem_reprovacao_contendo(resultado, "CTA sem bloco de oferta")


def test_oferta_sem_acesso_avisa(tmp_path):
    """Nomeia a oferta e carrega entrega, mas nem o bloco O nem o CTA dizem
    como acessar: avisa (não reprova)."""
    overrides = {
        "roteiro.txt": ROTEIRO.replace(
            "São dois dias, do zero, na Operação Claude Code. É isso que você constrói no evento.",
            "São dois dias, do zero, na Operação Claude Code. Você sai com tudo pronto.",
        ).replace(
            "[thales de frente + lettering + logo da occ | LEAD: toca em saiba mais | KEY: GARANTE SEU INGRESSO] "
            "Então aproveita que ainda tem vaga, toca em saiba mais e garante seu ingresso. Vamos embora!",
            "[thales de frente + lettering + logo da occ | LEAD: garante ingresso | KEY: GARANTE SEU INGRESSO] "
            "Então aproveita que ainda tem vaga e garante seu ingresso. Vamos embora!",
        ),
        "cta.md": CTA.replace(
            "- fala: Então aproveita que ainda tem vaga, toca em saiba mais e garante seu ingresso. Vamos embora!",
            "- fala: Então aproveita que ainda tem vaga e garante seu ingresso. Vamos embora!",
        ).replace(
            "- lettering: LEAD: toca em saiba mais | KEY: GARANTE SEU INGRESSO",
            "- lettering: LEAD: garante ingresso | KEY: GARANTE SEU INGRESSO",
        ),
        "letterings.md": LETTERINGS.replace("| toca em saiba mais |", "| garante ingresso |"),
    }
    resultado = rodar(tmp_path, overrides)
    assert not tem_reprovacao_contendo(resultado, "CTA sem bloco de oferta")
    assert tem_aviso_contendo(resultado, "bloco de oferta não diz como acessar")


def test_oferta_com_acesso_no_cta_nao_avisa(tmp_path):
    """Baseline: o CTA tem "toca em", que já cobre o acesso; sem aviso."""
    resultado = rodar(tmp_path)
    assert not tem_aviso_contendo(resultado, "bloco de oferta não diz como acessar")


# ---------------------------------------------------------------------------
# Marcadores de oferta: só locução de ENTREGA (verbo/preposição), nunca
# substantivo solto do nicho (achado do teste3, produto físico "Casa
# Medida": "projeto", "orçamento" e afins aparecem em qualquer frase do
# ramo de móveis planejados, sem dizer que a pessoa está recebendo algo).
# ---------------------------------------------------------------------------


def test_bloco_com_substantivo_solto_do_nicho_sem_entrega_reprova():
    """"A Casa Medida trabalha assim faz tempo aqui em Curitiba. Cada
    projeto sai do mesmo jeito, sem enrolação nenhuma pra ninguém." nomeia
    a marca ("Casa Medida") mas não carrega nenhuma locução de ENTREGA
    (só o substantivo solto "projeto"): reprova."""
    conceito = gc.Conceito({"modo": "pago", "marcas": ["Casa Medida"]})
    blocos = [
        gc.Bloco(
            numero=1, linha_original="", direcao="", fala=(
                "A Casa Medida trabalha assim faz tempo aqui em Curitiba. Cada projeto sai do "
                "mesmo jeito, sem enrolação nenhuma pra ninguém."
            ),
        ),
        gc.Bloco(numero=2, linha_original="", direcao="", fala="Toca aqui embaixo e marca a sua visita."),
    ]
    cta = gc.Cta({"tipo": "cta", "fala": "Toca aqui embaixo e marca a sua visita."})
    achados = gc.motor.checar_oferta(conceito, blocos, cta)
    assert any(a.nivel == gc.REPROVACAO and "CTA sem bloco de oferta" in a.recado for a in achados)


def test_oferta_real_produto_fisico_com_locucao_de_entrega_nao_reprova():
    """"A visita técnica da Casa Medida é gratuita. Eu meço a sua cozinha
    e monto o projeto em três dimensões com você. O orçamento sai junto,
    e você decide depois." nomeia a oferta E carrega locuções de entrega
    ("eu meço", "monto o projeto", "o orçamento sai", "com você", "você
    decide depois"): passa."""
    conceito = gc.Conceito({"modo": "pago", "oferta": "visita técnica da Casa Medida", "marcas": ["Casa Medida"]})
    blocos = [
        gc.Bloco(
            numero=1, linha_original="", direcao="", fala=(
                "A visita técnica da Casa Medida é gratuita. Eu meço a sua cozinha e monto o "
                "projeto em três dimensões com você. O orçamento sai junto, e você decide depois."
            ),
        ),
        gc.Bloco(numero=2, linha_original="", direcao="", fala="Toca aqui embaixo e marca a sua visita."),
    ]
    cta = gc.Cta({"tipo": "cta", "fala": "Toca aqui embaixo e marca a sua visita."})
    achados = gc.motor.checar_oferta(conceito, blocos, cta)
    assert not any(a.nivel == gc.REPROVACAO for a in achados)


def test_conceito_oferta_usa_campo_proprio_quando_declarado():
    conceito = gc.Conceito({"oferta": "Aula X", "marcas": ["Marca Y"]})
    assert conceito.oferta == "Aula X"


def test_conceito_oferta_cai_pra_primeira_marca_sem_campo():
    conceito = gc.Conceito({"marcas": ["Marca Y", "Marca Z"]})
    assert conceito.oferta == "Marca Y"


def test_conceito_oferta_vazia_sem_marcas_nem_campo():
    conceito = gc.Conceito({})
    assert conceito.oferta == ""


def test_checar_oferta_ignora_modo_organico():
    conceito = gc.Conceito({"modo": "organico", "marcas": ["X"]})
    blocos = [gc.Bloco(numero=1, linha_original="", direcao="", fala="qualquer coisa")]
    cta = gc.Cta({"tipo": "loop"})
    achados = gc.motor.checar_oferta(conceito, blocos, cta)
    assert achados == []


AGENDA_CHEIA_DIR = str(
    Path(__file__).resolve().parents[2] / "exemplos" / "agenda-cheia"
)


def test_pacote_real_agenda_cheia_passa_com_ponte():
    """Pacote versionado do exemplo agenda-cheia (v4): a ponte é "É
    exatamente isso que eu te ensino na aula", no bloco 8, e o bloco 9 (a
    oferta, papel O) fecha antes do CTA (bloco 10). Zero reprovações; três
    avisos assumidos (duração total, densidade do fecho e blocos 9/10
    vizinhos sem insert), custo declarado do bloco de oferta obrigatório.
    Os avisos de "eco de exemplo" (regra nova) não entram nessa conta: o
    próprio agenda-cheia é citado como ilustração em references/*.md e no
    outro exemplo (sem-contratar), então ecoa contra a documentação da
    skill sem ter copiado nada de ninguém."""
    resultado = gc.rodar(AGENDA_CHEIA_DIR)
    assert not tem_reprovacao_contendo(resultado, "CTA sem ponte")
    assert not tem_reprovacao_contendo(resultado, "CTA sem bloco de oferta")
    assert resultado["reprovacoes"] == []
    avisos_sem_eco = [a for a in resultado["avisos"] if "eco de exemplo" not in a]
    assert len(avisos_sem_eco) == 3


def test_pacote_real_agenda_cheia_sem_ponte_reprova(tmp_path):
    """Mutação do pacote real agenda-cheia: tira a ponte do bloco 8 e o
    gate reprova."""
    with open(os.path.join(AGENDA_CHEIA_DIR, "roteiro.txt"), "r", encoding="utf-8") as f:
        roteiro = f.read()
    roteiro_sem_ponte = roteiro.replace(
        "É exatamente isso que eu te ensino na aula.",
        "Sem contratar mais ninguém pra clínica.",
    )
    assert roteiro_sem_ponte != roteiro, "marcador de ponte não encontrado no roteiro.txt do agenda-cheia"

    for nome in os.listdir(AGENDA_CHEIA_DIR):
        origem = os.path.join(AGENDA_CHEIA_DIR, nome)
        destino = os.path.join(str(tmp_path), nome)
        with open(origem, "r", encoding="utf-8") as f:
            conteudo = f.read()
        with open(destino, "w", encoding="utf-8") as f:
            f.write(conteudo)
    with open(os.path.join(str(tmp_path), "roteiro.txt"), "w", encoding="utf-8") as f:
        f.write(roteiro_sem_ponte)

    resultado = gc.rodar(str(tmp_path))
    # Sem o marcador de ponte no bloco 8, a checagem estrutural (bloco
    # anterior sem ponte) OU a checagem do campo "ponte" declarado em
    # cta.md (frase que não bate mais com a fala do bloco) reprova.
    assert tem_reprovacao_contendo(resultado, "CTA sem ponte") or tem_reprovacao_contendo(
        resultado, "frase do campo ponte não está na fala do bloco citado"
    )


# ---------------------------------------------------------------------------
# Hook com pergunta ou paradoxo (regra nova do dono da metodologia)
# ---------------------------------------------------------------------------


def test_nenhum_hook_com_pergunta_ou_paradoxo_avisa(tmp_path):
    """Baseline tem 3 hooks com id de paradoxo (curiosity/contrarian/
    myth_busting); trocando os 3 pra táticas fora da lista e sem "?" na
    fala, avisa."""
    hooks_sem_paradoxo = (
        HOOKS.replace("- id: curiosity", "- id: bold_claim")
        .replace("- tatica: Curiosity", "- tatica: Bold Claim")
        .replace("- cluster: curiosidade", "- cluster: interrupcao_padrao")
        .replace("- id: contrarian", "- id: warning")
        .replace("- tatica: Contrarian", "- tatica: Warning")
        .replace("- id: myth_busting", "- id: shocking_statement")
        .replace("- tatica: Myth Busting", "- tatica: Shocking Statement")
    )
    matriz_sem_paradoxo = (
        MATRIZ.replace("curiosity", "bold_claim")
        .replace("contrarian", "warning")
        .replace("myth_busting", "shocking_statement")
    )
    overrides = {"hooks.md": hooks_sem_paradoxo, "matriz.md": matriz_sem_paradoxo}
    resultado = rodar(tmp_path, overrides)
    assert tem_aviso_contendo(resultado, "nenhum hook com pergunta ou paradoxo")


def test_hook_com_interrogacao_na_fala_nao_avisa_mesmo_sem_tatica_de_paradoxo(tmp_path):
    """"?" na fala de um hook basta, mesmo com as 3 táticas fora da lista
    de paradoxo (ids trocados como no teste anterior, fala do Hook A com
    "?")."""
    hooks_com_interrogacao = (
        HOOKS.replace("- id: curiosity", "- id: bold_claim")
        .replace("- tatica: Curiosity", "- tatica: Bold Claim")
        .replace("- cluster: curiosidade", "- cluster: interrupcao_padrao")
        .replace(
            "- fala: Em dois dias você sai da Operação Claude Code com cinco entregas prontas.\n- ancora: dois dias",
            "- fala: Em dois dias, você sai com cinco entregas prontas?\n- ancora: dois dias",
        )
        .replace("- id: contrarian", "- id: warning")
        .replace("- tatica: Contrarian", "- tatica: Warning")
        .replace("- id: myth_busting", "- id: shocking_statement")
        .replace("- tatica: Myth Busting", "- tatica: Shocking Statement")
    )
    matriz_sem_paradoxo = (
        MATRIZ.replace("curiosity", "bold_claim")
        .replace("contrarian", "warning")
        .replace("myth_busting", "shocking_statement")
    )
    roteiro_com_interrogacao = ROTEIRO.replace(
        "Em dois dias você sai da Operação Claude Code com cinco entregas prontas.",
        "Em dois dias, você sai com cinco entregas prontas?",
    )
    overrides = {
        "hooks.md": hooks_com_interrogacao,
        "matriz.md": matriz_sem_paradoxo,
        "roteiro.txt": roteiro_com_interrogacao,
    }
    resultado = rodar(tmp_path, overrides)
    assert not tem_aviso_contendo(resultado, "nenhum hook com pergunta ou paradoxo")


def test_baseline_tem_paradoxo_nao_avisa(tmp_path):
    resultado = rodar(tmp_path)
    assert not tem_aviso_contendo(resultado, "nenhum hook com pergunta ou paradoxo")


# ---------------------------------------------------------------------------
# Garrafais (secao 4, requisito 9)
# ---------------------------------------------------------------------------


def test_garrafal_em_bloco_com_insert_reprova(tmp_path):
    overrides = {
        "garrafais.md": GARRAFAIS.replace(
            "## G2\n- palavra: VERDADE\n- bloco: 5\n- ancora: negócio de verdade",
            "## G2\n- palavra: TEXTO\n- bloco: 3\n- ancora: texto",
        )
    }
    resultado = rodar(tmp_path, overrides)
    assert len(resultado["reprovacoes"]) == 1
    assert tem_reprovacao_contendo(resultado, "precisa de apresentador sozinho")


def test_garrafal_repetindo_o_key_reprova(tmp_path):
    overrides = {
        "garrafais.md": GARRAFAIS.replace(
            "## G2\n- palavra: VERDADE\n- bloco: 5\n- ancora: negócio de verdade",
            "## G2\n- palavra: SQUAD\n- bloco: 2\n- ancora: squad",
        )
    }
    resultado = rodar(tmp_path, overrides)
    # bloco 2 tem KEY: alem de repetir o KEY, agora tambem reprova por nao
    # ser apresentador sozinho (secao 4, regra nova do garrafal fora do
    # bloco 1).
    assert len(resultado["reprovacoes"]) == 2
    assert tem_reprovacao_contendo(resultado, "garrafal repete o KEY do mesmo bloco")
    assert tem_reprovacao_contendo(resultado, "apresentador sozinho (sem inserção de vídeo e sem KEY)")


def test_garrafal_em_bloco_com_key_fora_do_bloco_1_reprova(tmp_path):
    """Contrato seção 4: fora do bloco 1, o bloco é de apresentador SOZINHO
    (sem inserção de vídeo e sem KEY). Bloco 6 tem KEY (QUIZ QUE FILTRA) e
    não tem palavra em comum com a garrafal, então só a regra nova dispara."""
    overrides = {
        "garrafais.md": GARRAFAIS.replace(
            "## G2\n- palavra: VERDADE\n- bloco: 5\n- ancora: negócio de verdade",
            "## G2\n- palavra: FILTRA\n- bloco: 6\n- ancora: quiz de qualificação",
        )
    }
    resultado = rodar(tmp_path, overrides)
    assert tem_reprovacao_contendo(resultado, "apresentador sozinho (sem inserção de vídeo e sem KEY)")


def test_garrafal_com_palavra_fora_da_fala_reprova(tmp_path):
    overrides = {"garrafais.md": GARRAFAIS.replace("- palavra: VERDADE", "- palavra: AMANHÃ")}
    resultado = rodar(tmp_path, overrides)
    assert len(resultado["reprovacoes"]) == 1
    assert tem_reprovacao_contendo(resultado, "palavra da garrafal não está na fala do bloco")


# ---------------------------------------------------------------------------
# Assets (secao 7, requisito 11)
# ---------------------------------------------------------------------------


def test_asset_faltando_para_uma_ancora_reprova(tmp_path):
    overrides = {
        "assets.md": ASSETS.replace(
            "| 2 | prospecção buscando clientes sozinha | inteiro | doc | comentário do doc, link 1 | sim | |\n",
            "",
        )
    }
    resultado = rodar(tmp_path, overrides)
    assert len(resultado["reprovacoes"]) == 1
    assert tem_reprovacao_contendo(resultado, "sem linha para a âncora do roteiro")


def test_serve_nao_sem_ressalva_reprova(tmp_path):
    overrides = {
        "assets.md": ASSETS.replace(
            "| 3 | quiz de qualificação sendo respondido | inteiro | galeria | GalerIA, variante 5 | sim | |",
            "| 3 | quiz de qualificação sendo respondido | inteiro | galeria | GalerIA, variante 5 | não | |",
        )
    }
    resultado = rodar(tmp_path, overrides)
    assert len(resultado["reprovacoes"]) == 1
    assert tem_reprovacao_contendo(resultado, "serve: não sem ressalva")


def test_origem_criar_sem_referencia_reprova(tmp_path):
    overrides = {
        "assets.md": ASSETS.replace(
            "terminal do Claude Code criando a skill, tipografia grande", "terminal do claude"
        )
    }
    resultado = rodar(tmp_path, overrides)
    assert len(resultado["reprovacoes"]) == 1
    assert tem_reprovacao_contendo(resultado, "origem criar: exige referência com 5+ palavras")


# ---------------------------------------------------------------------------
# Matriz (secao 8, requisito 12)
# ---------------------------------------------------------------------------


def test_matriz_com_11_linhas_reprova(tmp_path):
    overrides = {
        "matriz.md": MATRIZ.replace(
            "| 12 | cinco_entregas_reels_sem_avatar_myth_busting_amarela_v1 | myth_busting | amarela | sem_avatar | não |\n",
            "",
        )
    }
    resultado = rodar(tmp_path, overrides)
    assert len(resultado["reprovacoes"]) == 1
    assert tem_reprovacao_contendo(resultado, "esperadas 12 linhas")


def test_matriz_sem_formato_sem_avatar_reprova(tmp_path):
    overrides = {"matriz.md": MATRIZ.replace("sem_avatar", "avatar_cheio")}
    resultado = rodar(tmp_path, overrides)
    assert len(resultado["reprovacoes"]) == 1
    assert tem_reprovacao_contendo(resultado, "nenhum formato sem avatar em tela")


def test_nome_de_peca_fora_do_padrao_reprova(tmp_path):
    overrides = {
        "matriz.md": MATRIZ.replace(
            "| 1 | cinco_entregas_reels_split_curiosity_laranja_v1 | curiosity | laranja | split | sim |",
            "| 1 | cincoentregas_reels_split_curiosity_laranja_v1 | curiosity | laranja | split | sim |",
        )
    }
    resultado = rodar(tmp_path, overrides)
    assert len(resultado["reprovacoes"]) == 1
    assert tem_reprovacao_contendo(resultado, "nome da peca fora do padrao")


# ---------------------------------------------------------------------------
# Direcoes (secao 2, requisito 13)
# ---------------------------------------------------------------------------


def test_linha_do_roteiro_sem_colchete_reprova(tmp_path):
    overrides = {
        "roteiro.txt": ROTEIRO.replace(
            "[thales de frente pra câmera] E olha, nenhuma dessas entregas exige que você aprenda a "
            "programar, são coisas rodando no seu negócio de verdade.",
            "thales de frente pra câmera] E olha, no seu negócio de verdade, nenhuma dessas entregas "
            "pede que você programe.",
        )
    }
    resultado = rodar(tmp_path, overrides)
    assert len(resultado["reprovacoes"]) == 1
    assert tem_reprovacao_contendo(resultado, "linha sem colchete ou sem direção")


def test_ancora_vaga_reprova(tmp_path):
    overrides = {
        "roteiro.txt": ROTEIRO.replace(
            "inserção de vídeo: claude criando uma skill do zero |", "inserção de vídeo: algo de tecnologia |"
        ),
        "assets.md": ASSETS.replace(
            "| 1 | claude criando uma skill do zero |", "| 1 | algo de tecnologia |"
        ),
    }
    resultado = rodar(tmp_path, overrides)
    assert len(resultado["reprovacoes"]) == 1
    assert tem_reprovacao_contendo(resultado, "âncora de insert vaga demais")


# ---------------------------------------------------------------------------
# Frases (requisito 15)
# ---------------------------------------------------------------------------


def test_frase_com_21_palavras_reprova(tmp_path):
    overrides = {
        "roteiro.txt": ROTEIRO.replace(
            "Todos os seus times de inteligência artificial juntos, rodando sem ninguém puxando cada "
            "etapa manualmente todo dia.",
            "Todos os seus times de inteligência artificial juntos, rodando sem ninguém puxando cada "
            "etapa manualmente todo dia e economizando um tempo enorme em cada semana que passa.",
        )
    }
    resultado = rodar(tmp_path, overrides)
    assert len(resultado["reprovacoes"]) == 1
    assert tem_reprovacao_contendo(resultado, "frase com mais de 20 palavras")


# ---------------------------------------------------------------------------
# Envelhecimento (requisito 16) e antitese (requisito 17)
# ---------------------------------------------------------------------------


def test_data_na_fala_em_campanha_frio_reprova(tmp_path):
    overrides = {
        "conceito.md": CONCEITO.replace("campanha: carrinho", "campanha: frio").replace(
            "objetivo: carrinho", "objetivo: frio"
        ),
        # CTA "seguro" (sem escassez/preco/data), pra isolar so a reprovacao
        # de envelhecimento do bloco 9 (sem essa troca, o CTA da baseline
        # tambem reprovaria por ter "vaga"/"ingresso" em campanha frio).
        "roteiro.txt": ROTEIRO.replace(
            "[thales de frente + lettering + logo da occ | LEAD: toca em saiba mais | KEY: GARANTE SEU INGRESSO] "
            "Então aproveita que ainda tem vaga, toca em saiba mais e garante seu ingresso. Vamos embora!",
            "[thales de frente + lettering + logo da occ | LEAD: toca em saiba mais | KEY: GARANTE PARTICIPAÇÃO] "
            "Então toca em saiba mais e garante sua participação especial nessa turma de agora. Vamos embora!",
        ).replace(
            "São dois dias, do zero, na Operação Claude Code. É isso que você constrói no evento.",
            "São dois dias, do zero, na Operação Claude Code. É isso que você constrói no evento no "
            "dia 15 de outubro de 2026.",
        ),
        "cta.md": CTA.replace(
            "- fala: Então aproveita que ainda tem vaga, toca em saiba mais e garante seu ingresso. Vamos embora!",
            "- fala: Então toca em saiba mais e garante sua participação especial nessa turma de agora. Vamos embora!",
        ),
        "letterings.md": LETTERINGS.replace(
            "| toca em saiba mais | GARANTE SEU INGRESSO |", "| toca em saiba mais | GARANTE PARTICIPAÇÃO |"
        ),
    }
    resultado = rodar(tmp_path, overrides)
    assert len(resultado["reprovacoes"]) == 1
    assert tem_reprovacao_contendo(resultado, "sinal de envelhecimento")


def test_dia_da_medicao_nao_e_data(tmp_path):
    """"no dia da medição"/"no dia da entrega" NÃO são data: "dia" sem um
    número ou mês logo depois. Regressão do teste3 (Casa Medida): a
    versão antiga do bloco 3 caiu no detector de envelhecimento por causa
    disso e teve que ser reescrita."""
    overrides = {
        "conceito.md": CONCEITO.replace("campanha: carrinho", "campanha: frio").replace(
            "objetivo: carrinho", "objetivo: frio"
        ),
        "roteiro.txt": ROTEIRO.replace(
            "Quatro: as suas próprias skills, criadas do zero. E skill é texto, se você sabe escrever "
            "como faz, você sabe montar direitinho.",
            "No dia da medição eu levo o material, e no dia da entrega você já usa a skill pronta.",
        ),
    }
    resultado = rodar(tmp_path, overrides)
    assert not tem_reprovacao_contendo(resultado, "sinal de envelhecimento")
    assert not tem_aviso_contendo(resultado, "sinal de envelhecimento")


def test_dia_seguido_de_numero_continua_data(tmp_path):
    """"dia 15" (dia seguido de número) continua contando como
    envelhecimento: só "dia da"/"dia do" solto que deixou de contar."""
    overrides = {
        "conceito.md": CONCEITO.replace("campanha: carrinho", "campanha: frio").replace(
            "objetivo: carrinho", "objetivo: frio"
        ),
        "roteiro.txt": ROTEIRO.replace(
            "[thales de frente + lettering + logo da occ | LEAD: toca em saiba mais | KEY: GARANTE SEU INGRESSO] "
            "Então aproveita que ainda tem vaga, toca em saiba mais e garante seu ingresso. Vamos embora!",
            "[thales de frente + lettering + logo da occ | LEAD: toca em saiba mais | KEY: GARANTE PARTICIPAÇÃO] "
            "Então toca em saiba mais e garante sua participação especial nessa turma de agora. Vamos embora!",
        ).replace(
            "São dois dias, do zero, na Operação Claude Code. É isso que você constrói no evento.",
            "São dois dias, do zero, na Operação Claude Code. Chega no dia 15 pronto pra começar.",
        ),
        "cta.md": CTA.replace(
            "- fala: Então aproveita que ainda tem vaga, toca em saiba mais e garante seu ingresso. Vamos embora!",
            "- fala: Então toca em saiba mais e garante sua participação especial nessa turma de agora. Vamos embora!",
        ),
        "letterings.md": LETTERINGS.replace(
            "| toca em saiba mais | GARANTE SEU INGRESSO |", "| toca em saiba mais | GARANTE PARTICIPAÇÃO |"
        ),
    }
    resultado = rodar(tmp_path, overrides)
    assert tem_reprovacao_contendo(resultado, "sinal de envelhecimento")


def test_densidade_insert_corpo_acima_do_maximo_avisa(tmp_path):
    """Contrato seção 9 (R3.4): densidade de insert por janela. No pacote
    baseline a janela 'corpo' (3,0 a 15,0s) passa de 55% de tempo com
    insert (medido: 60%); é aviso, não reprovação."""
    resultado = rodar(tmp_path)
    assert resultado["reprovacoes"] == []
    assert tem_aviso_contendo(resultado, "roteiro janela corpo")
    assert tem_aviso_contendo(resultado, "densidade de insert fora da faixa esperada")


def test_densidade_insert_fecho_acima_do_maximo_avisa(tmp_path):
    resultado = rodar(tmp_path)
    assert tem_aviso_contendo(resultado, "roteiro janela fecho")


def test_densidade_insert_janela_hook_isenta(tmp_path):
    """A janela 'hook' (0 a 3s) não entra na medição (aplica_a_partir_de_s: 3.0)."""
    resultado = rodar(tmp_path)
    assert not tem_aviso_contendo(resultado, "roteiro janela hook")


def test_formato_completo_usa_faixa_de_52_a_71s(tmp_path):
    """Com `formato: completo` em conceito.md, a faixa de duração usada
    pelo aviso passa a ser 52 a 71s (references/modelo-mestre.md, tabela
    de tamanho), não a faixa curta de 15 a 30s da esteira. O roteiro
    baseline (~42,6s finais) fica FORA da faixa de 15 a 30s (avisaria sem
    o campo) mas também fora de 52 a 71s: o teste confere que o LIMIAR
    citado no aviso mudou pra 52.0s a 71.0s."""
    overrides = {"conceito.md": CONCEITO + "formato: completo\n"}
    # nao da pra so appendar depois do "---" de fechamento; refaz o front matter
    overrides["conceito.md"] = CONCEITO.replace(
        "aceleracao: 1.45\n---", "aceleracao: 1.45\nformato: completo\n---"
    )
    resultado = rodar(tmp_path, overrides)
    avisos_duracao = [a for a in resultado["avisos"] if "duração total fora da faixa esperada" in a]
    assert len(avisos_duracao) == 1
    assert "52.0s a 71.0s" in avisos_duracao[0]


def test_formato_completo_dentro_da_faixa_nao_avisa():
    """teste3 (Casa Medida): 225 palavras, 53,51s finais, `formato:
    completo`. Dentro de 52 a 71s: sem aviso de duração (checagem direta
    de `checar_janelas_de_insert`, sem montar o pacote inteiro)."""
    conceito = gc.Conceito({"modo": "pago", "campanha": "frio", "formato": "completo"})
    bloco = gc.Bloco(
        numero=1, linha_original="", direcao="", fala="x" * 10,
        duracao_final=53.51, duracao_natural=53.51 * 1.45, inicio_final=0.0,
    )
    from gate_copy.regras.roteiro import checar_janelas_de_insert

    achados = checar_janelas_de_insert(conceito, [bloco])
    avisos_duracao = [a for a in achados if "duração total fora da faixa esperada" in a.recado]
    assert avisos_duracao == []


def test_conceito_formato_padrao_curto_quando_ausente():
    assert gc.Conceito({}).formato == "curto"


def test_conceito_formato_completo_declarado():
    assert gc.Conceito({"formato": "completo"}).formato == "completo"


def test_formato_ausente_mantem_faixa_padrao_de_15_a_30s(tmp_path):
    """Sem o campo `formato`, o comportamento não muda: continua a faixa
    de 15 a 30s (o baseline, ~42,6s, avisa nela, como sempre avisou)."""
    resultado = rodar(tmp_path)
    avisos_duracao = [a for a in resultado["avisos"] if "duração total fora da faixa esperada" in a]
    assert len(avisos_duracao) == 1
    assert "15.0s a 30.0s" in avisos_duracao[0]


def test_antitese_paralela_e_aviso_nao_reprovacao(tmp_path):
    overrides = {
        "roteiro.txt": ROTEIRO.replace(
            "E não é à toa que oito mil pessoas já passaram pelos meus treinamentos ao longo desses anos todos.",
            "Não é sorte. É método, testado com oito mil pessoas nos meus treinamentos ao longo desses anos todos.",
        )
    }
    resultado = rodar(tmp_path, overrides)
    assert resultado["reprovacoes"] == []
    assert tem_aviso_contendo(resultado, "antítese paralela, cara de IA")


# ---------------------------------------------------------------------------
# Eco de exemplo ou estudo de caso (regra nova): a fala do roteiro ou de um
# hook não pode repetir 5 palavras seguidas de um `.md`/`.txt` de
# `references/` ou `exemplos/` da própria skill.
# ---------------------------------------------------------------------------


def test_frase_copiada_do_exemplo_agenda_cheia_avisa_eco():
    """Copiar uma frase de `exemplos/agenda-cheia/roteiro.txt` pro roteiro
    de um cliente novo acusa eco (aviso, não reprovação): o molde de
    estrutura pode inspirar, a frase pronta do exemplo não pode ir junto
    pro cliente. Checagem direta de `checar_eco`, contra o índice real da
    skill (raiz_pacote fora de `exemplos/`: nada é excluído)."""
    from gate_copy.regras.roteiro import checar_eco

    bloco = gc.Bloco(
        numero=1, linha_original="", direcao="", fala=(
            "Cliente na cadeira, WhatsApp tocando. Quem espera vai marcar em outra barbearia."
        ),
    )
    achados = checar_eco([bloco], [])
    assert achados, "esperava pelo menos um AVISO de eco"
    assert all(a.nivel == gc.AVISO for a in achados)
    assert any("agenda-cheia" in a.recado for a in achados)


def test_frase_original_do_cliente_nao_avisa_eco():
    """Frase inédita, nunca escrita em nenhum exemplo/referência da
    skill: sem eco."""
    from gate_copy.regras.roteiro import checar_eco

    bloco = gc.Bloco(
        numero=1, linha_original="", direcao="", fala=(
            "A tinturaria do bairro Água Verde entrega sua roupa passada em quarenta minutos."
        ),
    )
    achados = checar_eco([bloco], [])
    assert achados == []


def test_pacote_dentro_de_exemplos_nao_ecoa_contra_si_mesmo():
    """Rodar o gate diretamente no exemplo `agenda-cheia` não pode acusar
    eco do agenda-cheia contra ele mesmo: `raiz_pacote` exclui os próprios
    arquivos do pacote sendo avaliado do índice de eco."""
    resultado = gc.rodar(AGENDA_CHEIA_DIR)
    avisos_eco_do_proprio_pacote = [
        a for a in resultado["avisos"]
        if "frase com eco de exemplo ou estudo de caso" in a and "exemplos/agenda-cheia/" in a
    ]
    assert avisos_eco_do_proprio_pacote == []


# ---------------------------------------------------------------------------
# Insumo faltando (R8.4, requisito do conceito.md ausente)
# ---------------------------------------------------------------------------


def test_conceito_ausente_recusa_pacote_nomeando_arquivo(tmp_path):
    resultado = rodar(tmp_path, remover=["conceito.md"])
    assert len(resultado["reprovacoes"]) == 1
    assert "conceito.md" in resultado["reprovacoes"][0]


def test_arquivo_obrigatorio_faltando_recusa_pacote_nomeando_arquivo(tmp_path):
    resultado = rodar(tmp_path, remover=["matriz.md"])
    assert len(resultado["reprovacoes"]) == 1
    assert "matriz.md" in resultado["reprovacoes"][0]


# ---------------------------------------------------------------------------
# --taticas (item 8 da tarefa): catálogo de táticas custom sobrescreve o
# catálogo embutido de 29 táticas.
# ---------------------------------------------------------------------------


def test_taticas_customizadas_sobrescrevem_embutidas():
    """Um `taticas_hook.yaml` com um id que NÃO existe no catálogo embutido
    passa a validar quando passado via `taticas=` pra `checar_hooks_md`; sem
    catálogo custom, o mesmo id reprova (unitário, isolado da matriz)."""
    from gate_copy.leitura import Conceito, Hook
    from gate_copy.regras.hook import checar_hooks_md

    conceito = Conceito(dados={"objetivo": "carrinho", "palavras_por_segundo": 2.9, "aceleracao": 1.45})
    hook_a = Hook(
        nome="Hook A",
        dados={
            "id": "tatica_nova_do_julio",
            "cluster": "curiosidade",
            "cru": "sim",
            "fala": "Em dois dias você sai da operação com cinco entregas prontas.",
            "ancora": "dois dias",
            "lettering": "nenhum",
        },
    )
    achados_sem_catalogo = checar_hooks_md(conceito, [], [hook_a])
    assert any("id de tática inexistente" in a.recado for a in achados_sem_catalogo)

    taticas_custom = [{"id": "tatica_nova_do_julio", "nome": "Tática Nova", "cluster": "curiosidade"}]
    achados_com_catalogo = checar_hooks_md(conceito, [], [hook_a], taticas=taticas_custom)
    assert not any("id de tática inexistente" in a.recado for a in achados_com_catalogo)


def test_cli_carregar_taticas_opcional_le_lista_do_yaml(tmp_path):
    caminho = os.path.join(str(tmp_path), "taticas_hook.yaml")
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(
            "taticas_hook:\n"
            "  taticas:\n"
            "    - id: minha_tatica\n"
            "      nome: Minha Tática\n"
            "      cluster: curiosidade\n"
        )
    resultado = gc.cli._carregar_taticas_opcional(caminho)
    assert resultado == [{"id": "minha_tatica", "nome": "Minha Tática", "cluster": "curiosidade"}]


def test_cli_carregar_taticas_opcional_sem_arquivo_devolve_none():
    assert gc.cli._carregar_taticas_opcional(None) is None
    assert gc.cli._carregar_taticas_opcional("/caminho/que/nao/existe.yaml") is None


# ---------------------------------------------------------------------------
# Numerais (requisito 4 da tarefa): algarismo casa com extenso na fala
# ---------------------------------------------------------------------------


def test_numeral_simples_casa_com_extenso():
    fala = gc.palavras_normalizadas("5 entregas prontas")
    assert gc.todas_palavras_na_fala("5 ENTREGAS PRONTAS", fala) == []


def test_numeral_dois_dias_casa_com_extenso():
    fala = gc.palavras_normalizadas("Em dois dias você sai com tudo pronto")
    assert gc.numero_esta_na_fala("2", fala) is True


def test_numeral_composto_oito_mil_casa_com_extenso():
    fala = gc.palavras_normalizadas("mais de oito mil pessoas confiam")
    assert gc.todas_palavras_na_fala("8 MIL", fala) == []


def test_numeral_ausente_da_fala_reporta_faltando():
    fala = gc.palavras_normalizadas("três coisas incriveis pra você")
    assert gc.todas_palavras_na_fala("5 COISAS", fala) == ["5"]


def test_hifen_casa_com_e_sem_hifen():
    assert gc.normalizar("segunda-feira") == gc.normalizar("segunda feira")


def test_numeral_onze_da_noite_casa_com_extenso():
    fala = gc.palavras_normalizadas("são onze da noite")
    assert gc.todas_palavras_na_fala("11 DA NOITE", fala) == []


def test_numeral_quarenta_e_oito_mil_casa_com_extenso():
    fala = gc.palavras_normalizadas("mais de quarenta e oito mil pessoas confiam")
    assert gc.todas_palavras_na_fala("48 MIL", fala) == []


def test_numeral_duzentas_clinicas_casa_com_extenso():
    fala = gc.palavras_normalizadas("já são duzentas clínicas usando")
    assert gc.todas_palavras_na_fala("200 CLÍNICAS", fala) == []


def test_numeral_11h_casa_com_onze():
    fala = gc.palavras_normalizadas("a live começa às onze da noite")
    assert gc.token_esta_na_fala(gc.normalizar("11h"), fala) is True


# ---------------------------------------------------------------------------
# CLI (subprocess): exit code e --json
# ---------------------------------------------------------------------------


def test_cli_exit_code_0_no_pacote_valido(tmp_path):
    escrever_pacote(str(tmp_path))
    resultado = subprocess.run(
        [sys.executable, GATE_PATH, str(tmp_path)],
        capture_output=True,
        text=True,
    )
    assert resultado.returncode == 0
    assert "REPROVAÇÕES" not in resultado.stdout


def test_cli_exit_code_1_no_pacote_mutado(tmp_path):
    escrever_pacote(str(tmp_path), remover=["conceito.md"])
    resultado = subprocess.run(
        [sys.executable, GATE_PATH, str(tmp_path)],
        capture_output=True,
        text=True,
    )
    assert resultado.returncode == 1
    assert "REPROVAÇÕES" in resultado.stdout


def test_cli_json_no_pacote_valido(tmp_path):
    escrever_pacote(str(tmp_path))
    resultado = subprocess.run(
        [sys.executable, GATE_PATH, str(tmp_path), "--json"],
        capture_output=True,
        text=True,
    )
    assert resultado.returncode == 0
    dados = json.loads(resultado.stdout)
    assert dados["reprovacoes"] == []
    assert len(dados["blocos"]) == 10


def test_cli_json_no_pacote_mutado(tmp_path):
    escrever_pacote(str(tmp_path), remover=["conceito.md"])
    resultado = subprocess.run(
        [sys.executable, GATE_PATH, str(tmp_path), "--json"],
        capture_output=True,
        text=True,
    )
    assert resultado.returncode == 1
    dados = json.loads(resultado.stdout)
    assert len(dados["reprovacoes"]) == 1
    assert "conceito.md" in dados["reprovacoes"][0]


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))


def test_oferta_dois_blocos_antes_do_cta_com_insert_passa(tmp_path):
    """O bloco de oferta pode ter insert e ficar dois blocos antes do CTA
    (o que é e o que será feito num bloco, o que ganha no seguinte): a
    janela é por posição, os 3 blocos antes do CTA, nunca 'depois do último
    insert'. Reproduz o exemplo sem-contratar."""
    roteiro = ROTEIRO.replace(
        "São dois dias, do zero, na Operação Claude Code. É isso que você constrói no evento.",
        "São dois dias, do zero. É isso que você constrói no evento.",
    )
    linhas = roteiro.strip().splitlines()
    oferta = (
        "[inserção de vídeo: tela da aula com o squad sendo montado | LEAD: na prática | KEY: OPERAÇÃO CLAUDE CODE] "
        "Na Operação Claude Code eu te mostro, na prática, como montar o seu squad do zero. "
        "Você sai de lá com ele rodando, mesmo sem saber código."
    )
    ganho = "[thales de frente pra câmera] E sai de lá com o seu já rodando, mesmo sem entender nada de código."
    linhas = linhas[:-1] + [oferta, ganho, linhas[-1]]
    overrides = {"roteiro.txt": "\n".join(linhas) + "\n"}
    resultado = rodar(tmp_path, overrides)
    assert not tem_reprovacao_contendo(resultado, "CTA sem bloco de oferta")
