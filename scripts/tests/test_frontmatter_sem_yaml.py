"""TDD: gate de copy tem que rodar num Mac limpo sem `pyyaml` instalado.

Cobre:
1. `frontmatter.ler_front_matter` (parser proprio, sem `yaml`) devolve o MESMO
   dicionario que `yaml.safe_load` pro front matter real do exemplo
   `cinco-entregas/conceito.md`.
2. `cli._carregar_yaml_opcional` nao quebra quando `yaml` nao esta instalado:
   imprime aviso em stderr e segue com os limiares/taticas embutidos.

Roda com: /usr/bin/python3 -m pytest ~/.claude/skills/copy-criativos/scripts/tests -q
"""

from __future__ import annotations

import os
import re
import sys

import pytest

SCRIPTS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, SCRIPTS_DIR)

from gate_copy import frontmatter  # noqa: E402

EXEMPLO_CONCEITO = os.path.expanduser(
    "~/.claude/skills/copy-criativos/exemplos/cinco-entregas/conceito.md"
)


def _extrair_bloco_front_matter(texto: str) -> str:
    m = re.search(r"^---\s*\n(.*?)\n---\s*\n", texto, re.DOTALL | re.MULTILINE)
    assert m, "conceito.md de exemplo sem front matter"
    return m.group(1)


def test_parser_proprio_bate_com_yaml_no_exemplo_real():
    yaml = pytest.importorskip("yaml")
    with open(EXEMPLO_CONCEITO, "r", encoding="utf-8") as f:
        texto = f.read()
    bloco = _extrair_bloco_front_matter(texto)

    dados_yaml = yaml.safe_load(bloco)
    # Chama o parser proprio diretamente (contorna o `if yaml:` de dentro de
    # ler_front_matter), pra provar que os dois caminhos dao o mesmo mapa.
    dados_proprio = frontmatter._ler_front_matter_proprio(bloco)

    assert dados_proprio == dados_yaml


def test_ler_front_matter_usa_yaml_quando_disponivel():
    pytest.importorskip("yaml")
    bloco = "chave: valor\nnumero: 3\n"
    assert frontmatter.ler_front_matter(bloco) == {"chave": "valor", "numero": 3}


def test_parser_proprio_escalares_e_lista():
    bloco = (
        "conceito: cinco_entregas\n"
        "palavras_por_segundo: 2.9\n"
        "aceleracao: 1.45\n"
        "ativo: true\n"
        "pausado: false\n"
        "aprovado: sim\n"
        "reprovado: nao\n"
        'titulo: "com aspas duplas"\n'
        "subtitulo: 'com aspas simples'\n"
        "marcas:\n"
        "  - Operacao Claude Code\n"
        "  - Claude Code\n"
        "  - Claude\n"
    )
    dados = frontmatter._ler_front_matter_proprio(bloco)
    assert dados["conceito"] == "cinco_entregas"
    assert dados["palavras_por_segundo"] == 2.9
    assert dados["aceleracao"] == 1.45
    assert dados["ativo"] is True
    assert dados["pausado"] is False
    assert dados["aprovado"] is True
    assert dados["reprovado"] is False
    assert dados["titulo"] == "com aspas duplas"
    assert dados["subtitulo"] == "com aspas simples"
    assert dados["marcas"] == ["Operacao Claude Code", "Claude Code", "Claude"]


def test_ler_conceito_funciona_sem_yaml(monkeypatch, tmp_path):
    """Simula Mac sem pyyaml instalado: `import yaml` tem que falhar dentro
    de `leitura.py` e o gate segue funcionando com o parser proprio."""
    monkeypatch.setitem(sys.modules, "yaml", None)
    # remove modulos ja importados que dependem de yaml pra forcar reimport
    for nome in list(sys.modules):
        if nome == "gate_copy" or nome.startswith("gate_copy."):
            monkeypatch.delitem(sys.modules, nome, raising=False)

    import gate_copy as gc

    conceito = gc.ler_conceito(EXEMPLO_CONCEITO)
    assert conceito.get("conceito") == "cinco_entregas"
    assert conceito.pps == 2.9
    assert conceito.aceleracao == 1.45
    assert conceito.marcas == ["Operação Claude Code", "Claude Code", "Claude"]


def test_cli_roda_sem_pyyaml_com_gates_padrao(monkeypatch, tmp_path, capsys):
    """`--gates`/`--taticas` (ou o padrao da esteira) apontando pra um YAML
    real, mas `yaml` ausente: cli imprime aviso e segue com o embutido, nunca
    quebra."""
    monkeypatch.setitem(sys.modules, "yaml", None)
    for nome in list(sys.modules):
        if nome == "gate_copy" or nome.startswith("gate_copy."):
            monkeypatch.delitem(sys.modules, nome, raising=False)

    import gate_copy as gc

    gates_yaml = tmp_path / "gates.yaml"
    gates_yaml.write_text("gates: {}\n", encoding="utf-8")

    pacote = os.path.expanduser("~/.claude/skills/copy-criativos/exemplos/cinco-entregas")
    rc = gc.main([pacote, "--gates", str(gates_yaml)])

    captured = capsys.readouterr()
    assert "pyyaml nao instalado" in captured.err.lower() or "pyyaml não instalado" in captured.err.lower()
    assert rc == 0
