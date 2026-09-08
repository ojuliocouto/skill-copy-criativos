#!/usr/bin/env python3
"""Limiares numéricos, catálogo embutido de táticas/formatos, verbos de ação
aceitos no CTA e mapa de numerais por extenso. Tudo o que o gate compara
contra um número ou um domínio fixo mora aqui (seção 9 do contrato, salvo
onde citado). `--gates` sobrescreve o que existir no `gates.yaml` da
esteira via `aplicar_gates`.

Compatibilidade: Python 3.9 (sem `X | None`; `from __future__ import
annotations` mais `Optional[X]`).
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Tuple

# LIMIARES: cada chave comenta a origem na secao 9 (ou na secao citada).
# `--gates` sobrescreve os que existirem no gates.yaml da esteira.
LIMIARES: Dict[str, Any] = {
    # tabela secao 9, linha "bloco com KEY em placa/coluna/carimbo"
    "lettering_permanencia_min_ms": {
        "placa": 2800,
        "coluna": 3500,
        "carimbo": 3500,
        "seta_cta": 2800,
    },
    "lettering_leitura_por_palavra_extra_ms": 250,
    "lettering_palavras_de_graca": 2,
    # secao 3, R2.6
    "hook_problema_nomeado_ate_s": 1.2,
    # secao 3, R2.5 / decisao 11
    "hook_logo_proibido_ate_s": 3.0,
    # tabela secao 9, "bloco sem insert e sem KEY"
    "retencao_avatar_sozinho_max_s": 6.0,
    # tabela secao 9, "primeiro/segundo insert" (R3.2)
    "retencao_insert_1_ini_s": 5.0,
    "retencao_insert_1_fim_s": 10.0,
    "retencao_insert_2_ini_s": 12.0,
    "retencao_insert_2_fim_s": 20.0,
    "retencao_insert_2_exigido_acima_de_s": 15.0,
    # secao 3, "ate 14 palavras" (R1.2 a R1.5)
    "diversidade_hook_fala_max_s": 5.0,
    # tabela secao 9, "bloco com insert"
    "insert_min_s": 3.5,
    # tabela secao 9, "bloco de CTA"
    "cta_min_s": 3.0,
    # secao 6, teto do bloco de CTA (aviso, nao reprovacao); origem
    # config/modos/pago.yaml -> fechamento.janela_final_max_s; nao existe em
    # gates.yaml, entao nao tem entrada em _MAPA_GATES.
    "cta_max_s": 5.0,
    # secao 9, "densidade de insert por janela" (R3.4, aviso); origem
    # gates.yaml -> retencao.densidade_insert e retencao.janelas.
    "retencao_densidade_insert_min": 0.45,
    "retencao_densidade_insert_max": 0.55,
    "retencao_janela_corpo_ini_s": 3.0,
    "retencao_janela_corpo_fim_s": 15.0,
    "retencao_janela_fecho_ini_s": 15.0,
    # tabela secao 9, "frase"
    "frase_max_palavras": 20,
    "frase_aviso_palavras": 14,
    # tabela secao 9, "duracao total" (R6.1, so aviso)
    "duracao_total_pago_min_s": 15.0,
    "duracao_total_pago_max_s": 30.0,
    "duracao_total_remarketing_min_s": 6.0,
    "duracao_total_remarketing_max_s": 15.0,
    "duracao_total_organico_min_s": 15.0,
    "duracao_total_organico_max_s": 30.0,
}

# Mapa de chaves com ponto (como vem em --gates) para o caminho em LIMIARES.
# Cada entrada e (caminho_no_limiares_tupla, ajuste).
_MAPA_GATES = {
    "dinamica.lettering.permanencia_min_ms.placa": ("lettering_permanencia_min_ms", "placa"),
    "dinamica.lettering.permanencia_min_ms.coluna": ("lettering_permanencia_min_ms", "coluna"),
    "dinamica.lettering.permanencia_min_ms.carimbo": ("lettering_permanencia_min_ms", "carimbo"),
    "dinamica.lettering.permanencia_min_ms.seta_cta": ("lettering_permanencia_min_ms", "seta_cta"),
    "dinamica.lettering.leitura_por_palavra_extra_ms": ("lettering_leitura_por_palavra_extra_ms", None),
    "dinamica.lettering.palavras_de_graca": ("lettering_palavras_de_graca", None),
    "hook.problema_nomeado_ate_s": ("hook_problema_nomeado_ate_s", None),
    "hook.logo_proibido_ate_s": ("hook_logo_proibido_ate_s", None),
    "retencao.avatar_sozinho_max_s": ("retencao_avatar_sozinho_max_s", None),
    "retencao.insert_1.ini_s": ("retencao_insert_1_ini_s", None),
    "retencao.insert_1.fim_s": ("retencao_insert_1_fim_s", None),
    "retencao.insert_2.ini_s": ("retencao_insert_2_ini_s", None),
    "retencao.insert_2.fim_s": ("retencao_insert_2_fim_s", None),
    "retencao.insert_2.exigido_acima_de_s": ("retencao_insert_2_exigido_acima_de_s", None),
    "diversidade.hook_fala_max_s": ("diversidade_hook_fala_max_s", None),
    "retencao.densidade_insert.min": ("retencao_densidade_insert_min", None),
    "retencao.densidade_insert.max": ("retencao_densidade_insert_max", None),
}


def _valor_em(dados: Any, caminho: str) -> Any:
    atual = dados
    for parte in caminho.split("."):
        if not isinstance(atual, dict) or parte not in atual:
            return None
        atual = atual[parte]
    return atual


def aplicar_gates(limiares: Dict[str, Any], gates_dados: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """Sobrescreve, em uma copia de `limiares`, o que existir em `gates_dados`."""
    resultado = dict(limiares)
    resultado["lettering_permanencia_min_ms"] = dict(limiares["lettering_permanencia_min_ms"])
    if not gates_dados:
        return resultado
    for caminho, (chave, subchave) in _MAPA_GATES.items():
        valor = _valor_em(gates_dados, caminho)
        if valor is None:
            continue
        if subchave:
            resultado[chave][subchave] = valor
        else:
            resultado[chave] = valor

    # `retencao.janelas` e uma lista de {nome, ini_s, fim_s}, sem caminho de
    # ponto fixo: procura as janelas "corpo" e "fecho" pelo nome (secao 9,
    # "densidade de insert por janela"). A janela "hook" fica isenta
    # (aplica_a_partir_de_s), entao nao tem limiar proprio.
    janelas = _valor_em(gates_dados, "retencao.janelas")
    if isinstance(janelas, list):
        for janela in janelas:
            if not isinstance(janela, dict):
                continue
            nome = janela.get("nome")
            if nome == "corpo":
                if janela.get("ini_s") is not None:
                    resultado["retencao_janela_corpo_ini_s"] = janela["ini_s"]
                if janela.get("fim_s") is not None:
                    resultado["retencao_janela_corpo_fim_s"] = janela["fim_s"]
            elif nome == "fecho":
                if janela.get("ini_s") is not None:
                    resultado["retencao_janela_fecho_ini_s"] = janela["ini_s"]
    return resultado


# 29 taticas da Motion (copiadas de config/taticas_hook.yaml da creative-studio;
# id, nome e cluster, sem os campos de honestidade da fonte).
TATICAS_EMBUTIDAS: Tuple[Dict[str, str], ...] = (
    {"id": "confession", "nome": "Confession", "cluster": "interrupcao_padrao"},
    {"id": "contrarian", "nome": "Contrarian", "cluster": "interrupcao_padrao"},
    {"id": "shocking_statement", "nome": "Shocking Statement", "cluster": "interrupcao_padrao"},
    {"id": "warning", "nome": "Warning", "cluster": "interrupcao_padrao"},
    {"id": "myth_busting", "nome": "Myth Busting", "cluster": "interrupcao_padrao"},
    {"id": "bold_claim", "nome": "Bold Claim", "cluster": "interrupcao_padrao"},
    {"id": "reverse_psychology", "nome": "Reverse Psychology", "cluster": "interrupcao_padrao"},
    {"id": "curiosity", "nome": "Curiosity", "cluster": "curiosidade"},
    {"id": "question", "nome": "Question", "cluster": "curiosidade"},
    {"id": "newness", "nome": "Newness", "cluster": "promocional"},
    {"id": "price_anchor", "nome": "Price Anchor", "cluster": "promocional"},
    {"id": "urgency", "nome": "Urgency", "cluster": "promocional"},
    {"id": "fomo", "nome": "FOMO", "cluster": "promocional"},
    {"id": "event_announcement", "nome": "Event Announcement", "cluster": "promocional"},
    {"id": "testimonial", "nome": "Testimonial", "cluster": "prova"},
    {"id": "social_proof", "nome": "Social Proof", "cluster": "prova"},
    {"id": "statistic", "nome": "Statistic", "cluster": "prova"},
    {"id": "authority", "nome": "Authority", "cluster": "prova"},
    {"id": "demonstration", "nome": "Demonstration", "cluster": "demonstracao"},
    {"id": "before_after", "nome": "Before and After", "cluster": "demonstracao"},
    {"id": "comparison", "nome": "Comparison", "cluster": "demonstracao"},
    {"id": "unboxing", "nome": "Unboxing", "cluster": "demonstracao"},
    {"id": "reasons_why", "nome": "Reasons Why", "cluster": "educacional"},
    {"id": "how_to", "nome": "How To", "cluster": "educacional"},
    {"id": "listicle", "nome": "Listicle", "cluster": "educacional"},
    {"id": "problem_solution", "nome": "Problem Solution", "cluster": "educacional"},
    {"id": "storytelling", "nome": "Storytelling", "cluster": "narrativa"},
    {"id": "relatability", "nome": "Relatability", "cluster": "narrativa"},
    {"id": "call_to_action_first", "nome": "Call to Action First", "cluster": "direto"},
)

# Clusters liberados por objetivo (R1.4): frio so interrupcao_padrao e
# curiosidade; carrinho ganha promocional tambem.
CLUSTERS_LIBERADOS = {
    "frio": {"interrupcao_padrao", "curiosidade"},
    "carrinho": {"interrupcao_padrao", "curiosidade", "promocional"},
}

# Formatos do motor (config/formatos.yaml da creative-studio), so id e
# avatar_em_tela, que e o que R7.1/R7.5 checam na matriz.
FORMATOS_EMBUTIDOS: Tuple[Dict[str, Any], ...] = (
    {"id": "avatar_cheio", "avatar_em_tela": True},
    {"id": "split", "avatar_em_tela": True},
    {"id": "sem_avatar", "avatar_em_tela": False},
    {"id": "noticia", "avatar_em_tela": False},
    {"id": "alerta", "avatar_em_tela": False},
    {"id": "podcast_mesa", "avatar_em_tela": True},
)

# Verbos de acao aceitos no CTA (secao 6, mesma lista de
# edl/construtor.VERBOS_DE_ACAO da esteira).
VERBOS_DE_ACAO: Tuple[str, ...] = (
    "toca", "toque", "clica", "clique", "aperta", "aperte", "acessa", "acesse",
    "entra", "entre", "inscreve", "inscreva", "inscrever", "garante", "garanta",
    "garantir", "baixa", "baixe", "assiste", "assista", "chama", "chame",
    "manda", "mande", "comenta", "comente", "salva", "salve", "arrasta",
    "arraste", "pega", "pegue", "aproveita", "aproveite", "cadastra",
    "cadastre", "responde", "responda", "vem", "venha", "corre", "corra",
)

# Numerais: algarismo -> variantes por extenso (secao 4). Palavra por extenso
# multipla ("vinte e quatro") casa como sequencia contigua na fala.
NUMERAIS: Dict[str, Tuple[str, ...]] = {
    "1": ("um", "uma"),
    "2": ("dois", "duas"),
    "3": ("tres",),
    "4": ("quatro",),
    "5": ("cinco",),
    "6": ("seis",),
    "7": ("sete",),
    "8": ("oito",),
    "9": ("nove",),
    "10": ("dez",),
    "12": ("doze",),
    "15": ("quinze",),
    "20": ("vinte",),
    "24": ("vinte e quatro",),
    "30": ("trinta",),
    "48": ("quarenta e oito",),
    "50": ("cinquenta",),
    "100": ("cem",),
    "1000": ("mil",),
}

# Secao 5: as 3 placas do rodizio (placa_h1/h2/h4) mais coluna, carimbo e
# seta_cta. "placa" sozinha NAO e mais uma forma valida (o pacote tem que
# declarar h1, h2 ou h4).
FORMAS_LETTERING = {"placa_h1", "placa_h2", "placa_h4", "coluna", "carimbo", "seta_cta"}

# Categoria de permanencia minima (secao 9): as 3 placas usam a mesma
# permanencia_min_ms.placa; as demais formas usam a propria chave.
CATEGORIA_PERMANENCIA_LETTERING = {
    "placa_h1": "placa",
    "placa_h2": "placa",
    "placa_h4": "placa",
    "coluna": "coluna",
    "carimbo": "carimbo",
    "seta_cta": "seta_cta",
}
# Marcadores de ponte (regra do dono da metodologia): frase que liga o que
# foi mostrado no corpo da peça ao que o clique do CTA entrega. Checados no
# bloco imediatamente anterior ao CTA (ou na primeira frase do próprio
# CTA), normalizados (sem acento, minúsculas) na hora da comparação.
MARCADORES_DE_PONTE: Tuple[str, ...] = (
    # marcadores originais
    "é isso que", "é exatamente isso", "é esse", "é essa", "é exatamente esse",
    "é exatamente essa", "foi assim que", "por isso que eu", "é o que eu",
    "eu te mostro", "vou te mostrar", "te mostro", "eu monto com você",
    "a gente monta", "na aula", "no treinamento", "na mentoria", "no evento",
    "na imersão", "dentro d",
    # calibração pelos ads reais (references/calibracao-jheni.md, seção 2):
    # a ponte dela ou aponta o que acabou de aparecer na tela ("é
    # exatamente isso que"), ou nomeia o mecanismo ("isso só é
    # possível"), ou vira pergunta de adesão ("topa aprender", "quer
    # aprender"), ou nomeia o lugar da entrega ("num treinamento", "na
    # operação").
    "é exatamente isso que", "e é isso que", "são soluções como essa",
    "esse é o tipo de conteúdo", "isso só é possível", "só é possível quando",
    "é o que eu vou te ensinar", "eu vou te ensinar", "vou te ensinar",
    "eu te ensino", "te ensino", "vou te mostrar na prática",
    "fazer isso na prática", "topa aprender", "quer aprender",
    "quer transformar", "você precisa se inscrever", "eu tenho um convite",
    "num treinamento", "numa imersão", "na operação", "na nova edição",
)

CORES_GARRAFAL = {"casa", "quente", "teal_do_fundo", "rosado_do_fundo"}
ENQUADRAMENTOS_ASSET = {"inteiro", "foco"}
ORIGENS_ASSET_FIXAS = {"doc", "galeria", "drive", "gravacao"}
ORIGENS_ASSET_CRIAR = {"criar:captura", "criar:ui_html", "criar:gerado"}
