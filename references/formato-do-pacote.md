# Formato do pacote de copy (contrato entre `copy-criativos` e `creative-studio`)

Este arquivo é o CONTRATO. O `scripts/gate_copy.py` lê exatamente o que está descrito aqui, e a
`creative-studio` consome o `roteiro.txt` sem nenhuma conversão. Quem escrever fora deste
formato reprova no gate antes de chegar na esteira.

Um pacote = um diretório por CONCEITO, com estes 8 arquivos:

```
<saida>/<conceito>/
  conceito.md      cabeçalho do conceito (front matter YAML + brief resumido)
  roteiro.txt      o roteiro anotado, no formato da esteira (a fronteira entre copy e edição)
  hooks.md         os 3 hooks da matriz (regra 3-2-2 do Léo, R1.2 a R1.5)
  garrafais.md     as 2 ou 3 palavras garrafais e a frase âncora de cada uma (decisão 8)
  letterings.md    LEAD e KEY por bloco, com a âncora da fala e a forma sugerida
  cta.md           fechamento por modo (R6.3 a R6.5)
  assets.md        origem e enquadramento de cada insert (decisões 12, 15, 34 e 35)
  matriz.md        as 12 peças nomeadas (R7.1)
```

Regras gerais dos arquivos `.md` de dados (`hooks`, `garrafais`, `cta`): os campos são linhas
`- chave: valor`, uma por linha, dentro de seções `## ...`. O gate lê chave e valor com
`chave: valor` e ignora negrito. `letterings.md`, `assets.md` e `matriz.md` são tabelas
markdown. Nada de travessão em nenhum arquivo. PT-BR com acento.

Sem `conceito.md` o gate recusa o pacote inteiro (R8.4: insumo faltando é recusa nomeada).

---

## 1. `conceito.md`

Front matter YAML entre `---`, depois o brief resumido em texto livre.

```markdown
---
conceito: cinco_entregas
angulo: Tour / O que tem dentro (categoria Produto, biblioteca dos 78)
estrutura_invisivel: gancho curiosidade + promessa; benefício funcional em lista; quebra de objeção de conhecimento; credibilidade por prova social; CTA com escassez real
avatar: dono de negócio que estuda I.A e ainda não tem nada rodando
apresentador: Thales Laray
promessa: sair da Operação Claude Code com cinco entregas prontas em dois dias
modo: pago
canal: reels
campanha: carrinho
objetivo: carrinho
marcas:
  - Operação Claude Code
  - Claude Code
  - Claude
palavras_por_segundo: 2.9
aceleracao: 1.45
---

Brief: <o que o Júlio passou, em 3 a 6 linhas: oferta, prova autorizada, assets entregues>
```

Campos e domínios:

| campo | obrigatório | domínio |
|---|---|---|
| `conceito` | sim | `snake_case`, sem acento, vira o prefixo do nome das peças |
| `angulo` | sim | nome do ângulo da biblioteca dos 78 e a categoria |
| `estrutura_invisivel` | sim | a combinação dos 8 elementos, em texto |
| `avatar` | sim | pra quem a peça fala |
| `apresentador` | sim | quem fala (Thales, Júlio, ou `nenhum` em peça só de narração) |
| `promessa` | sim | uma frase |
| `modo` | sim | `pago` ou `organico` |
| `canal` | sim | `reels`, `stories`, `feed_4x5`, `feed_1x1`, `tiktok`, `shorts` |
| `campanha` | sim | `frio`, `captacao`, `perpetuo_frio`, `carrinho`, `lote`, `remarketing` |
| `objetivo` | não | `frio` ou `carrinho`; sem ele o gate deriva: `carrinho` e `lote` viram `carrinho`, o resto vira `frio` |
| `marcas` | sim | lista dos nomes que R2.5 proíbe nos 3 primeiros segundos (marca, produto, evento) |
| `palavras_por_segundo` | não | padrão 2.9 (medido no ad21v2: 174 palavras em 60,155s de voz natural) |
| `aceleracao` | não | padrão 1.45 (decisão 23) |

---

## 2. `roteiro.txt`

É o formato que `creative_studio/inserts/fontes.ler_marcacoes` lê. Uma linha por bloco. TODA
linha começa com a direção entre colchetes e segue com a fala. Linha em branco é ignorada. Não
existe comentário: uma linha sem colchete vira fala solta e reprova no gate.

```
[inserção de vídeo: <âncora do asset> | LEAD: <lead> | KEY: <KEY>] fala do bloco
[inserção de vídeo: <âncora do asset>] fala do bloco
[thales de frente pra câmera] fala do bloco
[thales de frente + lettering | LEAD: <lead> | KEY: <KEY>] fala do bloco
[thales de frente + lettering + logo da operação | LEAD: <lead> | KEY: <KEY>] fala do CTA
```

Como a esteira lê cada parte:

- O primeiro campo é a DIREÇÃO. Se começa com `inserção de vídeo:`, o que vem depois dos dois
  pontos é a ÂNCORA do asset, e o casamento com o arquivo é por igualdade da âncora, nunca pelo
  sentido. Escrever a âncora em minúsculas, curta e específica ("quiz de qualificação sendo
  respondido", nunca "algo de tecnologia").
- `LEAD:` e `KEY:` são campos separados por `|`. `KEY` vira o lettering grande; `LEAD` é o
  contexto em itálico acima dele. Bloco sem `KEY` não gera lettering.
- A palavra `logo` na direção gera o evento de logo (R2.5 proíbe antes de 3,0s; a decisão 11
  libera o logo do EVENTO quando o nome está sendo dito na fala).
- A esteira ancora cada bloco buscando a FALA no alinhamento da voz, da frase inteira pra
  trás. Logo, a fala escrita tem que ser a fala gravada, palavra por palavra.
- A direção "pipoca" ou "sequência" significa vários assets encadeados, nunca imagem parada.

O bloco 1 é o hook A. Os hooks B e C (`hooks.md`) entram ANTES do bloco 1 na montagem; o corpo
continua o mesmo.

---

## 3. `hooks.md`

```markdown
# Hooks: cinco_entregas

## Hook A
- id: curiosity
- tatica: Curiosity
- cluster: curiosidade
- cru: não
- fala: Em dois dias você sai da Operação Claude Code com cinco entregas prontas. E eu vou começar pela que muda tudo.
- ancora: dois dias
- palavras: 21
- lettering: LEAD: em dois dias | KEY: 5 ENTREGAS PRONTAS
- garrafal: 2 DIAS
- insert: squad de times de i.a rodando no claude
- por que: <uma ou duas linhas>

## Hook B
...

## Hook C
- cru: sim
- lettering: nenhum
...
```

| campo | regra |
|---|---|
| `id` | id da tática em `references/taticas-de-hook.md` (29 da Motion); os 3 ids são distintos |
| `tatica`, `cluster` | nome e cluster da mesma tabela; o cluster tem que estar liberado pro `objetivo` (frio: `interrupcao_padrao` e `curiosidade`; carrinho: os dois mais `promocional`) |
| `cru` | `sim` ou `não`; ao menos um `sim` (R1.5); hook cru tem `lettering: nenhum` |
| `fala` | até 5,0s de fala natural (`diversidade.hook_fala_max_s`), ou seja, até 14 palavras a 2,9 p/s; o Hook A tem a MESMA fala do bloco 1 do roteiro |
| `ancora` | a palavra ou par de palavras que nomeia o PROBLEMA ou a PROMESSA; tem que aparecer na fala dentro das primeiras 4 palavras (1,2s a 2,9 p/s, R2.6) |
| `lettering` | `LEAD: ... \| KEY: ...` ou `nenhum` |
| `logo_ancorado` | opcional, `sim` ou `não`; `sim` declara que a marca dita dentro dos 3s entra com o logo do EVENTO ancorado na fala (decisão 11) |
| `garrafal` | opcional; quando existe, a palavra tem que estar na fala |
| `insert` | âncora de `assets.md` ou `nenhum` |

O que reprova em qualquer hook: marca dentro das primeiras 12 palavras (3s finais a 1,45x, R2.5)
sem `logo_ancorado: sim`; marca entre as 3 primeiras palavras mesmo com logo ancorado ("nunca
abre com marca", regra do brief, valor de partida sem medição própria); frase de apresentação
("eu sou o", "meu nome é", "aqui é o") nas duas primeiras frases; cluster fora do objetivo; mais
de 14 palavras. O que avisa: marca dentro dos 3s COM `logo_ancorado: sim` (fica registrado, a
esteira confere a âncora); antítese paralela ("não é X. É Y.") tem cara de IA.

---

## 4. `garrafais.md`

```markdown
# Garrafais: cinco_entregas

## G1
- palavra: 2 DIAS
- bloco: 1
- ancora: dois dias
- cor: casa
- papel: o número da promessa, abre a peça marcando o preço em tempo

## G2
- palavra: SEGUNDA-FEIRA
- bloco: 5
- ancora: segunda-feira
- cor: quente
- papel: a virada de argumento, quando o que foi listado vira resultado
```

Regras (decisão 8, `MAPA-GARRAFAIS.md`): a `palavra` é dita na `ancora`, e a âncora está na
fala do `bloco`; a palavra não repete o KEY do mesmo bloco; fora do bloco 1, o bloco é de
apresentador SOZINHO (sem `inserção de vídeo` e sem KEY, porque a garrafal exige 80ms de folga
do lettering e o mapa do piloto só a usa em janela sem lettering), porque a garrafal vive entre o fundo e a pessoa;
no máximo 2 no gancho (bloco 1) e 2 ou 3 na peça; `cor` em `casa`, `quente`, `teal_do_fundo`,
`rosado_do_fundo`. Número na garrafal vai em algarismo ("2 DIAS") e na fala por extenso ("dois
dias"): o gate casa os dois.

---

## 5. `letterings.md`

```markdown
# Letterings: cinco_entregas

| bloco | LEAD | KEY | âncora na fala | forma | palavras do KEY |
|---|---|---|---|---|---|
| 1 | em dois dias | 5 ENTREGAS PRONTAS | prontas | placa | 2 |
| 2 | entrega cinco | UM SQUAD | squad | placa | 2 |
| 10 | toca em saiba mais | GARANTE SEU INGRESSO | garante | seta_cta | 3 |
```

Regras: cada linha corresponde a um bloco do roteiro com `KEY`, com LEAD e KEY IDÊNTICOS aos do
roteiro (o roteiro manda; a tabela é a leitura); toda palavra do KEY está na fala do bloco
(algarismo casa com o número por extenso); KEY com no máximo 2 palavras de CONTEÚDO (o tempo de leitura da seção 9 conta toda palavra, como o motor) (algarismo e palavra funcional como de, do, da, no, na, em, que, e, um, uma, pra, com, sem não contam: "SKILLS DO ZERO" e "PÁGINA NO AR" valem 2),
exceto o KEY do CTA, que aceita 3 (verbo + objeto, decisão 7); `forma` em `placa_h1`, `placa_h2`,
`placa_h4` (os três estilos de placa do rodízio `dinamica.lettering.rodizio`), `coluna`,
`carimbo`, `seta_cta`; a mesma forma nunca em dois blocos vizinhos com lettering (`repetir_vizinho:
false`, decisão 13, e a sequência aprovada em `MAPA-LETTERINGS.md`: h2, h1, h2, coluna, h4, h1,
carimbo, seta_cta); `carimbo` é lettering de apoio, só em bloco com insert; LEAD com até 4 palavras. LEAD fora da fala é aviso, não reprovação.

---

## 6. `cta.md`

```markdown
# CTA: cinco_entregas

- modo: pago
- campanha: carrinho
- tipo: cta
- fala: Então aproveita que ainda tem vaga, toca em saiba mais e garante seu ingresso. Vamos embora!
- verbo_de_acao: toca, garante
- escassez: ainda tem vaga
- lettering: LEAD: toca em saiba mais | KEY: GARANTE SEU INGRESSO
- logo: Operação Claude Code, nome dito na fala do bloco anterior
```

| modo e campanha | `tipo` | exige | proíbe |
|---|---|---|---|
| pago, carrinho ou lote | `cta` | verbo de ação da lista da esteira + escassez legítima (vaga, ingresso, lote, prazo, última) | CTA vago |
| pago, frio, captação, perpétuo frio | `cta` | verbo de ação | escassez, preço, data, prazo (R6.4) |
| pago, remarketing | `cta` | verbo de ação | nada a mais; oferta permitida |
| orgânico | `loop`, `envio` ou `pergunta` | pergunta termina com `?`; envio tem "manda pra", "marca", "compartilha"; loop declara a frase que casa com o início | "toca em", "clica", "link", "saiba mais", "bio", "arrasta" (R6.5) |

A `fala` do CTA é a fala do ÚLTIMO bloco do roteiro. Verbos de ação aceitos (mesma lista de
`edl/construtor.VERBOS_DE_ACAO` da esteira): toca, toque, clica, clique, aperta, aperte, acessa,
acesse, entra, entre, inscreve, inscreva, inscrever, garante, garanta, garantir, baixa, baixe,
assiste, assista, chama, chame, manda, mande, comenta, comente, salva, salve, arrasta, arraste,
pega, pegue, aproveita, aproveite, cadastra, cadastre, responde, responda, vem, venha, corre,
corra.

---

## 7. `assets.md`

```markdown
# Assets: cinco_entregas

| # | âncora (do roteiro) | enquadramento | origem | referência | serve | ressalva |
|---|---|---|---|---|---|---|
| 1 | squad de times de i.a rodando no claude | inteiro | galeria | GalerIA, variante 2 (gráficos subindo) | sim | |
| 2 | claude criando uma skill do zero | inteiro | criar:ui_html | terminal do Claude Code criando a skill, tipografia acima de 22px | sim | proposta: mockup HTML fiel do terminal, aprovar antes |
| 3 | prospecção buscando clientes sozinha | inteiro | doc | comentário do doc, link 1 | não | asset horizontal com blur; usar como veio (decisão 35) e registrar aqui |
```

Regras: uma linha por `inserção de vídeo` do roteiro, com a âncora IDÊNTICA; `enquadramento` em
`inteiro` (padrão, decisão 15) ou `foco` (leve, até 1,25x; a ressalva diz o que a fala cita);
`origem` em `doc`, `galeria`, `drive`, `gravacao` (o que foi PASSADO, decisão 34) ou
`criar:captura`, `criar:ui_html`, `criar:gerado` (só quando não há nada pronto pro bloco;
`referência` descreve a proposta, que o Júlio aprova antes); `serve` em `sim` ou `não`; quando
`não`, a `ressalva` é obrigatória e a copy NÃO troca o asset por conta (decisão 35: asset do
briefing é intocável, a ressalva vai pro relatório). Asset horizontal ou borrado é o que mais
derruba a peça (decisões 12, 15, 21, 30, 31): é o caso típico de `serve: não`.

---

## 8. `matriz.md`

```markdown
# Matriz: cinco_entregas

- conceito: cinco_entregas
- canal: reels
- hooks: curiosity, contrarian, myth_busting
- legendas: laranja, amarela
- formatos: split, sem_avatar

| # | peça | hook | legenda | formato | avatar em tela |
|---|---|---|---|---|---|
| 1 | cinco_entregas_reels_split_curiosity_laranja_v1 | curiosity | laranja | split | sim |
| ... | | | | | |
| 12 | cinco_entregas_reels_sem_avatar_myth_busting_amarela_v1 | myth_busting | amarela | sem_avatar | não |
```

Regras (R1.2, R7.1, R7.5): 12 linhas = 3 hooks x 2 legendas x 2 formatos; nome no padrão
`{conceito}_{canal}_{formato}_{hook}_{legenda}_v{n}`; `hooks` iguais aos ids de `hooks.md`;
`formatos` entre `avatar_cheio`, `split`, `sem_avatar`, `noticia`, `alerta`, `podcast_mesa`,
sendo ao menos um SEM avatar em tela (`sem_avatar`, `noticia`, `alerta`); `legendas` são texto
livre (padrão `laranja` e `amarela`).

---

## 9. O que o gate mede no roteiro (resumo dos números)

Duração natural do bloco = palavras / `palavras_por_segundo`. Duração FINAL = natural /
`aceleracao`. Tudo medido em duração final, que é onde a esteira mede (a EDL nasce depois da
aceleração).

| o que | limiar | origem | veredito |
|---|---|---|---|
| bloco com insert | duração final >= 3,5s | decisões 29 e 30 (b-roll em 1,0x precisa de tempo) | reprova |
| bloco com KEY em placa | duração final >= 2,8s + 0,25s por palavra além da segunda | `dinamica.lettering.permanencia_min_ms`, decisão 29 | reprova |
| bloco com KEY em coluna ou carimbo | duração final >= 3,5s + 0,25s por palavra extra | idem | reprova |
| bloco de CTA | duração final >= 3,0s | `fechamento.janela_final_min_s` | reprova |
| bloco de CTA | duração final <= 5,0s (21 palavras) | `fechamento.janela_final_max_s` | aviso |
| bloco com KEY em `seta_cta` | duração final >= 2,8s | `permanencia_min_ms.seta_cta` | reprova |
| bloco sem insert e sem KEY | duração final <= 6,0s | R3.3, `retencao.avatar_sozinho_max_s` | reprova |
| blocos vizinhos sem insert (mesmo com KEY) | soma final <= 6,0s | R3.3 (a spec fala em "sem insert nem elemento"; o lettering cobre só parte do bloco, então a soma é aviso) | aviso |
| densidade de insert por janela | 45% a 55% do tempo com insert nas janelas 3 a 15s e 15s ao fim | R3.4, `retencao.densidade_insert` | aviso |
| hook (bloco 1) | âncora de problema ou promessa nas 4 primeiras palavras | R2.6, `hook.problema_nomeado_ate_s: 1.2` | reprova |
| marca | não nas 12 primeiras palavras (3s finais) do bloco 1 nem de nenhum hook | R2.5, `hook.logo_proibido_ate_s` | reprova sem `logo_ancorado: sim`; aviso com |
| marca | nunca nas 3 primeiras palavras, mesmo com logo ancorado | brief ("nunca abre com marca"), valor de partida | reprova |
| frase | nenhuma com mais de 20 palavras | brief (legenda de 2 linhas, R5.2 não publica número); valor de partida | reprova |
| frase | acima de 14 palavras | idem | aviso |
| envelhecimento | data, preço, edição, lote numerado na fala ou lettering | decisão 19 e R6.4 | reprova fora de `carrinho` e `lote`; aviso dentro |
| algarismo na fala | "8 mil" na fala | voz da casa: por extenso na fala, algarismo no lettering | aviso |
| antítese paralela | "não é X. É Y." | `feedback-antitese-paralela-cara-de-ia` | aviso |
| direção vaga | âncora com menos de 3 palavras, ou com "algo", "genérico", "qualquer", "imagens de", "vídeo de" | esteira casa por âncora exata | reprova |
| primeiro insert | começa entre 5 e 10s finais | R3.2 | aviso |
| segundo insert | começa entre 12 e 20s finais quando a peça passa de 15s | R3.2 | aviso |
| duração total | pago frio e orgânico 15 a 30s finais; remarketing 6 a 15s; carrinho e lote não têm faixa em `pago.yaml` e usam a de frio como referência | R6.1 (avisa, não reprova) | aviso |
