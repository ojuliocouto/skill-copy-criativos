---
name: copy-criativos
description: "Escreve a COPY de criativos em vídeo (anúncio pago e peça orgânica: Reels, Shorts, TikTok, Stories, feed) já no formato anotado que uma esteira de montagem consome: roteiro bloco a bloco com direção de insert, LEAD e KEY, mais hooks com tática nomeada, garrafais, letterings, CTA por modo, origem dos assets e a matriz 3x2x2. A copy sai da mão do copywriter pronta pra virar peça sem retrabalho de edição. Triggers: copy de criativo, roteiro de anúncio em vídeo, roteiro anotado, hooks, matriz de criativos, pacote de copy, /copy-criativos."
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
pairs-with:
  - skill: creative-method-creator
    reason: "optional: true. Escolhe conceito e ângulo antes desta skill. Se você não tem essa skill instalada, use references/angulos-e-estrutura.md, que traz a mesma biblioteca de ângulos e a estrutura invisível."
  - skill: creative-studio
    reason: "optional: true. Esteira de montagem que consome o roteiro.txt deste pacote sem reescrever uma palavra. Sem ela, o pacote continua sendo copy pronta pra produção manual, e o gate roda com os limiares embutidos."
---

# Copy de criativos em vídeo

Esta skill escreve a copy de UM CONCEITO por vez e entrega um PACOTE (um diretório com 8
arquivos), não um texto solto. O arquivo central é o `roteiro.txt`, no formato anotado
`[direção | LEAD: <lead> | KEY: <key>] fala`. A fronteira é essa: a copy termina no
`roteiro.txt`; quem monta o vídeo começa nele e nunca reescreve uma palavra.

A regra de ouro: **a copy escolhe as palavras que vão virar tela (garrafal, KEY, ênfase da
legenda) e as coloca na fala; nunca o contrário.** Lettering que a voz não diz é decoração, e
garrafal escolhida por caber está proibida.

Esta skill é autossuficiente. Tudo que ela precisa está dentro deste diretório: as regras, os
números, o gate, os dois exemplos e os modelos. Ela não depende de nenhuma outra skill nem de
nenhum repositório externo.

---

## Quem é quem e o que é o quê

O material desta skill nasceu de uma operação real, e alguns nomes aparecem nas regras como fonte
histórica. Você não precisa conhecer nenhuma dessas pessoas para usar a skill.

| nome | o que é | o que fazer com isso |
|---|---|---|
| **Júlio** | dono da metodologia e da esteira de montagem original | onde uma regra diz que ele aprovou ou rejeitou algo, leia "**o cliente que aprova**". No seu projeto, quem aprova é o seu cliente |
| **Léo** | gestor de tráfego da operação original | dele vêm a regra **3-2-2** (cada conceito sai em 3 hooks, 2 legendas, 2 formatos) e a **biblioteca dos 78 ângulos**, que está inteira em `references/angulos-e-estrutura.md` |
| **Thales** | apresentador das peças de exemplo | a régua de **2,9 palavras por segundo** foi medida na voz dele. **Remeça na voz do seu apresentador** e ajuste `palavras_por_segundo` no `conceito.md`: todos os mínimos de bloco saem desse número |
| **Jheni** | copywriter da operação original | dela vem o método de **hook demonstrativo**: quando existe tela pra mostrar, a tela abre a peça e a prova vem antes da promessa |
| **Escola de Automação** e **Operação Claude Code** | a empresa e o evento das peças de exemplo | são o cliente e a oferta do exemplo `exemplos/cinco-entregas/`. No seu projeto, troque pelo seu |
| **GalerIA** | o banco de assets daquela casa | aparece como valor de `origem: galeria` em `assets.md`. Leia como "o banco de assets do cliente" |
| **esteira**, **creative-studio** | o motor de montagem que consome o `roteiro.txt` | **opcional**. Sem ele, o pacote continua válido: é copy pronta, com direção de tela declarada, para quem for editar |
| **decisão N** | registro numerado de decisões do piloto da esteira | o número serve só de rastreio. O texto relevante de cada uma já está em `references/regras-da-tela.md`; você não precisa procurar o registro original |

Em todo o resto deste arquivo, "o cliente" significa quem aprova a copy do seu lado.

---

## Pré-requisitos

- **Claude Code** com esta skill em `~/.claude/skills/copy-criativos/`.
- **Python 3.9 ou mais novo.** O `/usr/bin/python3` que vem no macOS serve.
- **`pyyaml` é opcional.** Sem ele, o gate roda normalmente com os limiares e o catálogo de
  táticas **embutidos** no código. Instale só se você tiver a esteira e quiser apontar os arquivos
  de configuração dela com `--gates` e `--taticas`:
  ```bash
  python3 -m pip install --user pyyaml
  ```
- **Um preset de oferta.** É o que autoriza cada número e cada prova da peça. Se o cliente não
  tiver um, monte com ele usando `references/modelo-preset-oferta.md`.

Confira que o gate roda antes de escrever qualquer coisa:

```bash
cd ~/.claude/skills/copy-criativos
python3 scripts/gate_copy.py exemplos/agenda-cheia
```

Tem que sair o resumo por bloco e **um único aviso** (densidade de 58% na janela do fecho), sem
nenhuma reprovação. Se sair um erro de import, resolva isso agora: gate quebrado significa entrega
sem prova.

---

## O que precisa existir antes (onboarding)

Confira, nesta ordem, e recuse o pedido nomeando o que falta:

1. **Brief com os 4 campos obrigatórios**: avatar (pra quem), promessa (uma frase), modo
   (`pago` ou `organico`) e canal (`reels`, `stories`, `feed_4x5`, `feed_1x1`, `tiktok`,
   `shorts`). Em modo pago, também a campanha (`frio`, `captacao`, `perpetuo_frio`, `carrinho`,
   `lote`, `remarketing`): é ela que decide se o CTA pode ter escassez e preço (R6.4).
2. **Conceito e ângulo**: um ângulo da biblioteca dos 78 e uma estrutura invisível, os dois em
   `references/angulos-e-estrutura.md`. Sem ângulo declarado, escolha um com o cliente antes de
   escrever: ângulo é decisão de estratégia, não de redação.
3. **Oferta e provas autorizadas**: **peça o preset de oferta ao cliente, ou monte com ele usando
   `references/modelo-preset-oferta.md`**. Número, nome de cliente, prova ou preço fora do preset
   não existe. Nunca invente. Um preset preenchido de exemplo está em
   `references/preset-oferta-exemplo.md`.
4. **Assets passados**: o que o cliente já entregou pro conceito (arquivo no Drive, gravação de
   tela, print, banco de assets). Se o brief vier em **Google Doc com comentários, leia todos os
   comentários** antes de escrever: cada link dentro de um comentário é um asset daquele bloco,
   então um comentário com N links são N assets. Nunca associe asset a bloco "pelo sentido da
   frase": case pela âncora do comentário.
5. **Onde a peça vai ser montada** (opcional): se existir uma esteira de montagem, diga na entrega
   contra qual configuração o gate rodou. Sem esteira, o gate roda com os limiares embutidos e a
   entrega declara isso.

Quando faltar 1 ou 2, pare e peça. Quando faltar 3 ou 4, escreva com placeholders
`[PROVA A CONFIRMAR]` e `origem: criar:...`, e diga isso na entrega. Nunca escreva "algo de
tecnologia" no lugar de um asset: direção vaga reprova no gate.

---

## Ler antes de escrever uma linha

Tudo dentro deste diretório:

| arquivo | o que tem |
|---|---|
| `references/metodo-de-copy.md` | **leia primeiro.** O MÉTODO: as 3 camadas, o diagnóstico do avatar (temperatura e nível de consciência), a anatomia do anúncio em papéis de bloco, as sequências válidas e o checklist de estrutura. `regras-da-tela.md` diz o que a tela aguenta; este diz o que a copy faz |
| `references/regras-da-tela.md` | a lista completa do que a edição faz com o seu texto, uma linha por regra, com o número de origem. É a fonte das regras resumidas abaixo |
| `references/formato-do-pacote.md` | o contrato dos 8 arquivos, campo a campo, e a tabela de números do gate (seção 9) |
| `references/taticas-de-hook.md` | as 29 táticas de hook por cluster, com exemplo, e a regra de cluster por objetivo |
| `references/angulos-e-estrutura.md` | os 78 ângulos em 5 categorias e os 8 elementos da estrutura invisível |
| `references/voz-e-anti-ia.md` | a voz falada BR e o gate anti-IA: o que está banido e o teste de voz alta |
| `references/modelo-preset-oferta.md` | o modelo em branco do preset de oferta |
| `references/preset-oferta-exemplo.md` | um preset preenchido, fictício, que alimenta o exemplo limpo |
| `references/calibracao-jheni.md` | **calibração**: os anúncios já escritos e gravados da casa, ad a ad, com os moldes de hook, de enumeração, de mecanismo, de ponte e de CTA que o método importou. Material interno, e o que sai dele para o método é molde, nunca conteúdo |

E os dois exemplos, que têm papéis diferentes:

- **`exemplos/agenda-cheia/`: o exemplo LIMPO.** Peça fictícia de nove blocos que passa no gate com
  **zero reprovações e zero avisos**. É o que você imita quando está aprendendo o formato. O
  `README.md` de lá mostra a tabela de blocos, as contas que fecharam a peça, e as duas correções
  que trouxeram o pacote até aqui: a v1 reprovada pelo dono da metodologia (hook genérico e CTA sem
  ponte) e a v3 remontada com os moldes de `references/calibracao-jheni.md` (enumeração com um
  insert por item, respiro entre os itens, mecanismo nomeado e ponte com molde).
- **`exemplos/cinco-entregas/`: o exemplo REAL.** Reconstrução de uma peça de verdade, aprovada e
  no ar, com dez blocos. Passa com zero reprovações, mas carrega **13 avisos assumidos** (entre
  eles duração de 40,67s e densidade de insert de 99% na janela do corpo), porque a peça real é assim
  e a copy não mente sobre ela. É o que você lê quando quer entender por que uma peça aprovada
  pode carregar aviso, e como declarar isso.

---

## O pacote (a saída)

```
<saida>/<conceito>/
  conceito.md      ângulo, avatar, promessa, modo, canal, campanha, marcas, brief resumido
  roteiro.txt      o roteiro anotado, um bloco por linha
  hooks.md         3 hooks com tática nomeada (um cru), regra 3-2-2
  garrafais.md     as 2 ou 3 palavras de maior carga de copy, com a frase âncora
  letterings.md    LEAD e KEY por bloco, com a palavra âncora e a forma
  cta.md           fechamento por modo
  assets.md        origem e enquadramento de cada insert
  matriz.md        as 12 peças nomeadas: {conceito}_{canal}_{formato}_{hook}_{legenda}_v{n}
```

**Diretório de saída padrão: `./copy/<conceito>/`**, relativo ao diretório de trabalho atual. Se
o cliente pedir outro lugar, use o que ele pedir. Se existir uma esteira `creative-studio`
instalada e o fluxo for entregar direto nela, o padrão de lá é `~/creative-studio/copy/<conceito>/`
(caminho **opcional**, só quando a esteira existe).

Cada arquivo tem formato fixo (ver `references/formato-do-pacote.md`); o gate lê exatamente
aquilo.

---

## As regras de escrita que vêm da tela

Resumo. O detalhe, com a origem de cada número, está em `references/regras-da-tela.md`.

Números de partida: **2,9 palavras por segundo** de fala natural e entrega acelerada a **1,45x**.
Tudo abaixo é em tempo FINAL, que é onde a montagem mede. A conversão única é
`palavras = segundos finais x 4,205`.

> As 2,9 palavras por segundo foram medidas na voz de um apresentador específico. **Meça na voz do
> seu** (conte as palavras de um minuto de fala natural gravada) e ajuste `palavras_por_segundo`
> no `conceito.md`. Todos os mínimos abaixo se recalculam a partir desse número.

| regra | número | por quê |
|---|---|---|
| bloco com insert | 15 palavras ou mais (3,5s finais) | o b-roll roda em 1,0x e precisa de tempo; bloco curto não comporta insert |
| bloco com KEY em placa (`h1`, `h2` ou `h4`) | 12 palavras ou mais (2,8s) | tempo de leitura do lettering |
| bloco com KEY em coluna ou carimbo | 15 palavras ou mais (3,5s) | a coluna obriga o olho a girar, o carimbo é pequeno |
| bloco com KEY em `seta_cta` | 12 palavras ou mais (2,8s) | permanência mínima da seta do CTA |
| forma do lettering | `placa_h1`, `placa_h2`, `placa_h4`, `coluna`, `carimbo`, `seta_cta` | o rodízio são os três estilos de placa mais as duas formas alternativas. "Placa" não é forma única: h1 depois de h2 é rodízio funcionando. Sequência de referência: h2 no gancho, depois h1, h2, coluna, h4, h1, carimbo, seta_cta |
| carimbo | só em bloco que tem insert | é lettering de APOIO: marca onde a peça está quando o insert já é o assunto |
| bloco de CTA | 13 palavras ou mais (3,0s) e no máximo 21 (5,0s) | janela final do CTA (R6.3); acima de 21 palavras é aviso |
| bloco sem insert e sem KEY | 25 palavras no máximo (6,0s) | bloco único acima disso REPROVA (R3.3) |
| blocos vizinhos sem insert | somados, 25 palavras no máximo (6,0s), mesmo com KEY | AVISA, porque o lettering cobre só parte do bloco |
| peça pago frio e orgânico | 15 a 30s finais = 64 a 126 palavras | R6.1; remarketing 6 a 15s = 26 a 63 palavras |
| peça de carrinho ou lote | sem faixa própria: usa a de frio como referência, e o número vira aviso | as faixas declaradas são só `frio` e `remarketing` |
| hook | até 14 palavras (5s naturais); problema ou promessa nas 4 primeiras palavras | R1.3 e R2.6 |
| hook, forma | **ao menos um dos 3 hooks é pergunta ou paradoxo** que a pessoa precise resolver | afirmação previsível não faz ninguém parar; o gate AVISA quando nenhum dos três tem |
| ponte antes do CTA | **obrigatória.** O bloco anterior ao CTA, ou a primeira frase do CTA, diz o que o clique entrega e amarra isso na prova que acabou de aparecer | benefício e depois "toca em saiba mais" do nada REPROVA: o clique fica sem objeto |
| marca, produto, evento | marca dentro das 12 primeiras palavras do bloco 1 ou de qualquer hook REPROVA, salvo hook com `- logo_ancorado: sim` em `hooks.md`, que vira aviso; nas 3 primeiras palavras reprova sempre | R2.5; o teto das 3 palavras é regra de brief ("nunca abre com marca"), valor de partida |
| frase | até 14 palavras de conforto, 20 é o teto | valor de partida: acima de 14 avisa, acima de 20 reprova |
| KEY | até 2 palavras de conteúdo, substantivo forte, todas ditas na fala | legível em corpo pequeno; o CTA aceita 3 (verbo + objeto) |
| LEAD | contexto curto, até 4 palavras, itálico | é o "entrega cinco" acima do "UM SQUAD" |
| garrafal | 2 ou 3 por peça, no máximo 2 no gancho; dita na fala; nunca repete o KEY do bloco; fora do bloco 1, só em bloco sem insert E sem KEY | ela vive entre o fundo e a pessoa. Zero ou uma garrafal AVISA; acima de três REPROVA |
| números | por extenso na fala ("oito mil"), algarismo no lettering ("8 MIL", "2 DIAS") | voz falada; a ênfase forte da legenda tem gatilho de número |
| conteúdo que envelhece | data, preço, edição e lote numerado só em `carrinho` e `lote` | R6.4 |
| um insert por bloco | e o bloco DIZ o que a tela mostra ("Cinco: um squad" pede tela de squad) | o casamento com o arquivo é por âncora exata, nunca pelo sentido |
| espalhar os inserts | 45 a 55% do tempo de cada janela com insert, a partir de 3,0s | R3.4; janelas de corpo (3 a 15s) e fecho (15s ao fim). Blocos de insert colados estouram a janela do corpo |
| direção do bloco | vem da copy e não se troca | se o asset não tem o movimento que a fala descreve, quem monta produz o movimento; o bloco nunca vira apresentador por causa do asset |
| voz | falada BR, frase curta, sem antítese paralela, sem saudação, sem apresentação | `references/voz-e-anti-ia.md` |

**Nota sobre a tabela de mínimos**: os valores acima são para **KEY de 2 palavras**. Cada palavra
a mais no KEY soma **0,25s**, ou seja, **uma palavra** a mais de fala. Exemplo: `SKILLS DO ZERO`
tem 3 palavras de tempo, então o mínimo da placa vai de 2,8s para **3,05s** (13 palavras em vez de
12).

**Como contar o KEY, que são duas contas diferentes:**

1. **Para o limite de 2 palavras**, contam só as palavras de **conteúdo**: algarismo e palavra
   funcional (de, do, da, no, na, em, que, e, um, uma, pra, com, sem) não entram.
2. **Para o tempo de leitura**, contam **todas as palavras não numéricas** do KEY, inclusive as
   funcionais.

Exemplo: `SKILLS DO ZERO` vale **2** para o limite (skills, zero) e **3** para o tempo (skills,
do, zero), o que dá mínimo de **3,05s**.

### A ponte antes do CTA

Antes de pedir a ação, a peça precisa dizer **o que o clique entrega**, ligado à prova ou ao
benefício que acabou de aparecer na tela. Essa frase é a **ponte**, e ela mora no fim do bloco
anterior ao CTA ou na primeira frase do próprio CTA.

Sem ponte, a peça mostra a prova e no bloco seguinte manda clicar, e quem assiste não sabe o que
ganha com isso. Isso reprova no gate.

Marcadores que o gate procura: "é isso que", "é esse ... que eu monto com você", "eu te mostro",
"na aula", "no treinamento", "na mentoria". Exemplo, colado no fim do bloco da prova:

> "A Dra. Renata ligou o dela e dobrou os agendamentos em um mês, sem contratar ninguém. **É esse
> atendente que eu monto com você na aula.**"

Declare a ponte em `cta.md` com o campo `- ponte: bloco N, "frase"`.

### Fechamento por modo (R6.3 a R6.5)

- **Pago, carrinho ou lote**: verbo de ação + escassez legítima. "Toca em saiba mais e garante seu
  ingresso, ainda tem vaga."
- **Pago, frio, captação ou perpétuo**: verbo de ação, sem escassez, sem preço, sem data.
- **Orgânico**: nunca link nem clique. Loop (a última frase casa com a primeira), pergunta pra
  comentário ou pedido de envio ("manda pra quem...").

### Assets

O insert é feito com o que foi **PASSADO**. Só quando não há nada pronto pro bloco é que a peça
cria (captura real de tela primeiro, depois UI fiel em HTML, depois gerado), sempre direcionada
pela fala e **proposta ao cliente antes**. Asset horizontal ou borrado é o que mais derruba a
peça, mas asset do briefing é intocável: a copy marca `serve: não` com a ressalva em `assets.md`,
nunca troca por conta. Enquadramento padrão `inteiro`; `foco` só leve.

Imagem parada serve como insert: declare a origem com o sufixo **`:imagem`** (por exemplo
`drive:imagem`). O gate aceita e **avisa**, porque quem monta vai precisar dar movimento ao asset
(deslize lento no próprio arquivo, sem desfoque nem véu).

---

## Processo

### Passo 0: planejar os blocos ANTES de escrever

Rode o planejador com a forma da peça que você pretende escrever. Ele diz quantas palavras cabem
em cada bloco e se a densidade de insert por janela fecha, **antes** de você gastar redação numa
estrutura que não fecha:

```bash
cd ~/.claude/skills/copy-criativos
python3 scripts/planejar_blocos.py --modo pago --campanha frio --blocos "L,L,I,A,I,C"
```

Três planos de partida que costumam fechar: **`L,L,I,A,I,C`** (a ponte vai na última frase do
bloco de insert que vem antes do CTA), **`L,L,I,A,I,P,C`** (a ponte como bloco próprio, quando
sobra duração) e **`L,L,I,A,I,I,A,I,C`** (enumeração de três itens com um insert por item e
respiro entre eles, que é o desenho do exemplo `exemplos/agenda-cheia/`). O planejador recusa um
plano em que o bloco antes do `C` não seja `P` nem `I`.

Na enumeração, o bloco sem insert **entre** os itens não é decoração: sem ele a densidade de insert
da janela do corpo vai a 77%, contra a faixa de 45 a 55%. É onde cabem a identificação e a frase de
continuação ("não para por aí").

Interface:

| flag | o que é |
|---|---|
| `--modo` | `pago` ou `organico` |
| `--campanha` | `frio`, `captacao`, `perpetuo_frio`, `carrinho`, `lote`, `remarketing` |
| `--blocos` | a forma da peça, um símbolo por bloco, separados por vírgula: **`I`** insert, **`L`** lettering em placa, **`LC`** lettering em coluna ou carimbo, **`A`** apresentador sozinho, **`P`** ponte (apresentador sozinho ligando o corpo ao CTA), **`C`** CTA. O planejador exige **`P` ou `I` imediatamente antes do `C`**: são os dois tipos de bloco que comportam a fala da ponte |
| `--palavras` | opcional: a contagem real de palavras de cada bloco, para simular um roteiro já contado em vez do mínimo |

A saída traz, por bloco, o **mínimo e o máximo de palavras**, a **linha do tempo** (início e fim
de cada bloco em segundos finais) e a **densidade de insert por janela**. Se o planejador disser
que a janela do corpo estoura, mude a forma da peça agora: intercale um bloco de apresentador
entre dois inserts, ou tire um insert. Depois de escrito, mexer nisso custa a peça inteira.

As duas contas que **não dá para acertar no papel** são exatamente essas: a densidade por janela e
o teto de dois blocos vizinhos sem insert. Elas dependem da linha do tempo acumulada, e é por isso
que este passo vem antes de escrever, não depois.

### Passo 1: ler o brief e o conceito

Conferir os 5 itens do onboarding. Recusar sem avatar, promessa, modo e canal.

### Passo 2: montar a SEQUÊNCIA DE PAPÉIS e depois a tabela de blocos

**Primeiro a sequência, sempre.** Antes de escrever fala, escreva a fila de papéis que a peça vai
seguir, do `references/metodo-de-copy.md` (seções 3 e 4): `H` hook, `D` dor ou diagnóstico, `P`
prova com insert, `M` mecanismo ou virada, `I` identificação, `O` oferta, `T` ponte, `C` CTA.

As sequências de partida, por temperatura:

| temperatura | sequência |
|---|---|
| frio, problema primeiro | `H D P M T C` |
| frio, demonstração primeiro (existe tela pra mostrar) | `H P I M T C` |
| quente, carrinho ou lote | `H P O T C` |

Papéis podem repetir (`P` várias vezes numa peça de enumeração) e podem dividir bloco: escreva
`P+T` ou `O+T` quando a ponte é a última frase de outro bloco. **`T` vem sempre imediatamente antes
de `C`**, e a peça tem ao menos um `P`.

Declare a sequência escolhida no campo `sequencia` do `conceito.md`.

**Só então a tabela de blocos**, e antes de polir qualquer coisa. Colunas: `bloco | papel | fala |
palavras | final | mínimo exigido | passa | insert | LEAD | KEY | forma`. Repare que `papel` e
`forma` são alfabetos diferentes: `papel` diz o que o bloco faz na argumentação, `forma` diz o que
aparece na tela. **O cliente aprova bloco a bloco**; só depois de aprovado é que o
texto vira `roteiro.txt`.

Rode o **checklist de estrutura** da seção 5 do `references/metodo-de-copy.md` ainda nesta tabela,
antes de escrever mais uma linha. Os quatro itens que mais derrubam peça:

1. **Tem prova concreta?** Tela real da coisa funcionando, ou caso com nome, número e contexto.
2. **O mecanismo está nomeado?** Aponte a frase que diz por que isso funciona quando o resto não
   funciona. Sem ela, a promessa vira pedido de fé.
3. **A ponte existe?** Aponte qual frase, de qual bloco, diz o que o clique entrega e amarra isso na
   prova. Se você não consegue apontar, a peça salta do benefício para o "toca em saiba mais" e
   reprova.
4. **O gancho combina 2 elementos e abre algo que a pessoa precise resolver?** Afirmação com que ela
   já concorda não faz ninguém parar.

### Passo 3: gerar os 3 hooks

Com tática nomeada (`references/taticas-de-hook.md`): cluster de interrupção ou curiosidade em
frio; promocional liberado só em carrinho, lote ou prazo. **Ao menos um dos três é pergunta ou
paradoxo** que a pessoa precise resolver na cabeça (o gate avisa quando nenhum é). Um dos três é
**cru** (nota de voz, sem
lettering, sem apresentador em tela). Ids distintos. Mostre os três em tabela (`hook | tática |
cluster | fala | palavras | âncora | cru`) e peça a escolha ou o mix. O Hook A é a fala do bloco 1;
B e C entram antes do bloco 1 na montagem.

### Passo 4: fechar garrafais, letterings e CTA

Nos arquivos próprios, com a âncora da fala em cada um. Preencher `assets.md` (origem de cada
insert) e `matriz.md` (12 nomes).

### Passo 5: rodar o gate

```bash
cd ~/.claude/skills/copy-criativos
python3 scripts/gate_copy.py <caminho do pacote>
```

Adicione `--json` para saída legível por máquina. Código de saída 1 significa pelo menos uma
reprovação.

Se você tiver a esteira instalada, pode apontar a configuração dela (as duas flags são
**opcionais**; sem elas o gate usa os limiares e o catálogo de táticas embutidos):

```bash
python3 scripts/gate_copy.py <pacote> \
  --gates <config da esteira>/gates.yaml \
  --taticas <config da esteira>/taticas_hook.yaml
```

Quando rodar sem elas, **diga isso na entrega**.

#### O que REPROVA

- `conceito.md` faltando, ou campo obrigatório dele faltando.
- Bloco com insert abaixo de 3,5s finais (15 palavras).
- Bloco com KEY abaixo do tempo de leitura da forma declarada.
- Bloco de CTA abaixo de 3,0s (13 palavras), ou CTA vago, ou CTA incoerente com o modo e a
  campanha (escassez, preço ou data fora de carrinho e lote).
- **Ponte ausente antes do CTA**: nem o bloco anterior nem a primeira frase do CTA dizem o que o
  clique entrega.
- Bloco único sem insert e sem KEY acima de 6,0s (25 palavras).
- Âncora de problema ou promessa fora das 4 primeiras palavras do hook.
- Marca nas 3 primeiras palavras, sempre; nas 12 primeiras sem `logo_ancorado: sim`.
- Frase de apresentação ("eu sou o", "meu nome é", "aqui é o") nas duas primeiras frases.
- Hook acima de 14 palavras, ou cluster de hook fora do objetivo, ou ids repetidos, ou nenhum hook
  cru.
- Frase acima de 20 palavras.
- Direção de insert vaga: âncora com menos de 3 palavras, ou com "algo", "genérico", "qualquer",
  "imagens de", "vídeo de".
- Palavra de KEY que não está na fala do bloco.
- KEY acima de 2 palavras de conteúdo (3 no CTA).
- **Mais de três garrafais** na peça.
- Garrafal com a palavra fora da fala, ou repetindo o KEY do mesmo bloco, ou fora do bloco 1 num
  bloco que tem insert ou KEY.
- Asset sem origem, com origem inválida, ou com `serve: não` sem ressalva.
- Matriz incompleta ou fora do padrão de nome.
- Conteúdo que envelhece (data, preço, edição, lote numerado) fora de `carrinho` e `lote`.

#### O que AVISA

- **Forma de lettering repetida em bloco vizinho.**
- **Carimbo em bloco que não tem insert.**
- **Zero ou uma garrafal** na peça (o alvo são 2 ou 3).
- **Nenhum dos três hooks é pergunta ou paradoxo.**
- Blocos vizinhos sem insert somando mais de 6,0s.
- Densidade de insert fora de 45 a 55% em alguma janela.
- CTA acima de 5,0s (21 palavras).
- Primeiro insert fora da janela de 5 a 10s; segundo fora de 12 a 20s.
- Duração total fora da faixa do modo e da campanha.
- Marca dentro das 12 primeiras palavras COM `logo_ancorado: sim`.
- Antítese paralela ("não é X. É Y." e variantes).
- Algarismo na fala.
- LEAD que não está na fala do bloco.
- Frase acima de 14 palavras.
- Conteúdo que envelhece dentro de `carrinho` ou `lote`.
- Origem de asset `criar:*` (precisa de proposta ao cliente antes).
- Origem de asset com sufixo `:imagem` (imagem parada; quem monta dá o movimento).

Corrigir e rodar de novo até **zero reprovações**. Aviso fica registrado na entrega, não se
esconde.

### Passo 6: entregar o pacote

Caminho do diretório, a tabela final de blocos, os 3 hooks, os avisos que ficaram e contra qual
configuração o gate rodou. Nada de "pronto" sem o output do gate colado na entrega.

---

## Auditoria antes de entregar (além do gate)

- [ ] Cada bloco diz o que a tela mostra? Direção de insert específica, escrita pra quem vai buscar
  ou criar o asset?
- [ ] Toda palavra de KEY, LEAD e garrafal está na fala, no bloco certo?
- [ ] O hook nomeia problema ou promessa nas 4 primeiras palavras e não abre com marca?
- [ ] Ao menos um dos três hooks é pergunta ou paradoxo, e o gancho combina 2 elementos?
- [ ] A peça tem prova concreta e mecanismo nomeado? (checklist da seção 5 do `metodo-de-copy.md`)
- [ ] A promessa está calibrada pela temperatura (frio: resultado e prazo; quente: probabilidade e
  esforço)?
- [ ] Existe ponte antes do CTA, ligada à prova ou ao benefício do bloco anterior?
- [ ] CTA bate com o modo e a campanha?
- [ ] Nenhum número ou prova fora do preset da oferta?
- [ ] Zero travessão, acentuação completa, voz falada BR, nenhuma frase com cara de IA?
  (`references/voz-e-anti-ia.md`)
- [ ] O gate rodou e o output está na entrega?

---

## O que esta skill NÃO faz

- Não edita vídeo, não escolhe arquivo de asset, não renderiza nada.
- Não escolhe conceito nem ângulo do zero: isso é decisão de estratégia, com o cliente, usando
  `references/angulos-e-estrutura.md`.
- Não escreve copy longa (página, VSL, e-mail).
- Não inventa prova, número, cliente ou demonstração.

## Handoff

Entregar no chat: caminho do pacote, tabela de blocos, os 3 hooks, output do gate, avisos que
ficaram. Quem monta o vídeo segue lendo `<saida>/<conceito>/roteiro.txt` e os demais arquivos do
pacote.
