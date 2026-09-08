# Exemplo real: `cinco_entregas`

**Este exemplo reproduz uma peça REAL, gravada, aprovada e no ar.** Ele reconstrói o anúncio
"cinco entregas" da Escola de Automação, gravado na voz do apresentador da casa e aprovado pelo
cliente. Por reproduzir uma peça de campo, ele passa com **zero reprovações mas carrega 13 avisos
assumidos**, entre eles uma duração final de **40,67s** (a faixa publicada é 15 a 30s) e uma
densidade de insert de **99%** na janela do corpo (a faixa é 45 a 55%).

**Se você quer o exemplo LIMPO, ele é o outro:** `exemplos/agenda-cheia/`. Aquele é fictício, tem
seis blocos, e passa com zero reprovações e um único aviso declarado. Use ele para aprender o
formato.

Use **este** para entender outra coisa: por que uma peça aprovada pode carregar aviso, e como
declarar cada aviso em vez de esconder. Aviso não é reprovação, e peça de campo raramente cabe
inteira na régua. O que não se admite é o aviso passar despercebido.

O anúncio gravado, como estava, NÃO passaria no gate. Cada diferença listada abaixo é uma regra de
copy sendo aplicada, não gosto.

## Os números da conta

`palavras_por_segundo: 2.9` e `aceleracao: 1.45` (decisão 23), então:

```
duração natural = palavras / 2,9
duração final   = natural / 1,45  =  palavras / 4,205
```

Mínimos da seção 9 do contrato, convertidos em palavras:

| exigência | duração final | palavras |
|---|---|---|
| bloco com insert | 3,5s | 15 |
| bloco com KEY em placa `h1`, `h2` ou `h4` (KEY de 2 palavras) | 2,8s | 12 |
| bloco com KEY em coluna ou carimbo (KEY de 2 palavras) | 3,5s | 15 |
| bloco com KEY em `seta_cta` (KEY de 2 palavras) | 2,8s | 12 |
| cada palavra do KEY além da segunda | mais 0,25s | mais 1 |
| bloco de CTA | mínimo 3,0s | 13 |
| bloco de CTA | máximo 5,0s (aviso) | máximo 21 |
| bloco sem insert e sem KEY | máximo 6,0s | máximo 25 |
| blocos vizinhos sem insert, somados (aviso) | máximo 6,0s | máximo 25 |

Os mínimos por forma são: placa 2,8s, coluna 3,5s, carimbo 3,5s, `seta_cta` 2,8s. O teto do CTA é
de 5,0s.

## A sequência de papéis

Declarada no `conceito.md`:

```
sequencia: H,P,P,P,M,P,P,P,O+T,C
```

É a sequência quente de `references/metodo-de-copy.md` (`H P O T C`) expandida pela enumeração: em
vez de uma prova, cinco, uma por entrega, cada uma com o próprio insert. O bloco 5 é o `M`, a virada
que transforma a lista em resultado ("já na segunda-feira você tem coisa rodando"), e o bloco 8 é a
prova social. A oferta e a ponte dividem o bloco 9 (`O+T`), e o CTA fecha.

Repare que `P` repetido é o normal numa peça de contagem regressiva: é ela que dá o ritmo. O preço
disso está no aviso 13, a densidade de insert estourada no corpo.

## Conferência bloco a bloco

Medida pelo gate e conferida à mão. A coluna `papel` diz o que o bloco FAZ na argumentação; a coluna
`forma` diz o que aparece na TELA.

| bloco | papel | palavras | natural (s) | final (s) | insert | KEY | forma | mínimo exigido (s) | passa |
|---|---|---|---|---|---|---|---|---|---|
| 1 | H | 13 | 4,48 | 3,09 | não | 5 ENTREGAS PRONTAS | placa_h2 | 3,05 (placa 2,80 + 0,25 da terceira palavra) | sim |
| 2 | P | 16 | 5,52 | 3,80 | sim | UM SQUAD | placa_h1 | 3,50 (insert; a placa pedia 2,80) | sim |
| 3 | P | 21 | 7,24 | 4,99 | sim | SKILLS DO ZERO | placa_h2 | 3,50 (insert; a placa pedia 3,05) | sim |
| 4 | P | 16 | 5,52 | 3,80 | sim | PROSPECÇÃO SOZINHA | coluna | 3,50 (insert e coluna empatados) | sim |
| 5 | M | 18 | 6,21 | 4,28 | não | nenhum | nenhuma | máximo 6,00 | sim |
| 6 | P | 16 | 5,52 | 3,80 | sim | QUIZ QUE FILTRA | placa_h4 | 3,50 (insert; a placa pedia 3,05) | sim |
| 7 | P | 17 | 5,86 | 4,04 | sim | PÁGINA NO AR | placa_h1 | 3,50 (insert; a placa pedia 3,05) | sim |
| 8 | P | 16 | 5,52 | 3,80 | sim | 8 MIL | carimbo | 3,50 (insert e carimbo empatados) | sim |
| 9 | O+T | 22 | 7,59 | 5,23 | não | nenhum | nenhuma | máximo 6,00 | sim |
| 10 | C | 16 | 5,52 | 3,80 | não | GARANTE SEU INGRESSO | seta_cta | 3,05 (seta_cta 2,80 + 0,25 da terceira palavra) | sim |

Total: **171 palavras, 40,67s finais**. Nenhuma frase passa de 14 palavras (o teto de reprovação
é 20, valor de partida do brief, porque a R5.2 não publica número).

## O que mudou em relação ao anúncio gravado, e por quê

### 1. Bloco 1: "cinco coisas prontas" virou "cinco entregas prontas"

O KEY é `5 ENTREGAS PRONTAS` e a fala gravada dizia "cinco coisas prontas". A regra é que toda
palavra do KEY é dita na fala, senão o lettering vira uma segunda mensagem em vez de reforço do
que está sendo dito. Uma palavra trocada resolve.

### 2. Bloco 1 perdeu a segunda frase e perdeu o insert

O Hook A é a fala do bloco 1 inteira, e hook tem teto de 14 palavras (5,0s de fala natural). A
fala gravada tinha 21 palavras com o "E eu vou começar pela que muda tudo". Cortada, o bloco fica
com 13 palavras.

Só que 13 palavras dão 3,09s finais, abaixo dos 3,5s que um bloco com insert exige. As duas
regras se cruzam, e a saída é tirar o insert do bloco 1: ele passa a ser **apresentador de frente
com lettering e a garrafal 2 DIAS atrás**, que é exatamente o que a decisão 10 já tinha desenhado
pro gancho (P1 no topo, garrafal no fundo). O insert do squad desce pro **bloco 2**, que é o bloco
que fala do squad. O asset ficou mais bem casado do que estava.

### 3. Os KEYs ficam como o cliente aprovou, e a fala vai buscá-los

O contrato aceita no máximo 2 palavras no KEY (3 no CTA), e a conta é de palavras de
**conteúdo**: algarismo e palavra funcional (de, do, da, no, na, que, e, um, uma, pra, com, sem)
não entram. Com essa régua, os KEYs aprovados passam inteiros:

| bloco | KEY | conta | palavras de conteúdo |
|---|---|---|---|
| 3 | SKILLS DO ZERO | 2 | skills, zero ("do" é funcional) |
| 6 | QUIZ QUE FILTRA | 2 | quiz, filtra ("que" é funcional) |
| 7 | PÁGINA NO AR | 2 | página, ar ("no" é funcional) |
| 2 | UM SQUAD | 1 | squad ("um" é funcional) |
| 8 | 8 MIL | 1 | mil (o algarismo não conta) |

O que mudou, então, não foi o KEY: foi a fala, que passou a dizer o KEY em sequência, pra o
lettering ser reforço do que está sendo dito e não uma segunda mensagem.

- **Bloco 6.** O gravado dizia "um quiz de qualificação que filtra quem entra e manda o lead
  pronto pro seu WhatsApp": 15 palavras numa frase só, e o KEY quebrado no meio de "quiz de
  qualificação que filtra". A fala nova é *"Dois: um quiz que filtra quem entra. E manda o lead
  pronto direto pro seu WhatsApp."* O "de qualificação" sai da fala e continua vivo na âncora do
  asset (`quiz de qualificação sendo respondido`), que é onde o arquivo é casado.
- **Bloco 7.** O gravado dizia "a sua página profissional no ar", com "profissional" separando
  "página" de "no ar". A fala nova é *"E um: a sua página no ar. Profissional, publicada e
  hospedada pelo Claude, sem você pagar hospedagem."* O adjetivo não se perdeu, só mudou de
  lugar.
- **Bloco 3.** Nada a fazer: a fala gravada já diz "as suas próprias skills, criadas do zero",
  com "skills" e "do zero" dentro dela.

### 4. Bloco 8: "8 mil" virou "oito mil", e o bloco ganhou lettering

Número vai por extenso na fala e em algarismo no lettering (voz da casa; algarismo na fala é
aviso no gate). O bloco era o único com insert e sem LEAD nem KEY; a decisão 16 aprovou o carimbo
"8 MIL", então ele entra como `LEAD: já passaram | KEY: 8 MIL`. A prova continua sendo só a
autorizada no preset de oferta: mais de oito mil pessoas.

### 5. Bloco 10: a fala passa a dizer o KEY

A decisão 7 trocou o KEY do CTA pra "GARANTE SEU INGRESSO", mas a voz gravada dizia "toca em
saiba mais pra se inscrever". Ficava lettering falando uma coisa e voz falando outra. A fala nova
diz o KEY inteiro: *"Então aproveita que ainda tem vaga, toca em saiba mais e garante seu
ingresso. Vamos embora!"*. O LEAD acompanha e vira "toca em saiba mais" (o "toque em" antigo era
resto do par "toque em / SAIBA MAIS"). A direção também passa a dizer `logo da operação` em vez
de `logo da occ`, porque o contrato procura a palavra `logo` e o nome do evento é o que está
sendo dito na fala do bloco 1 (decisão 11).

### 6. Bloco 5 perdeu a antítese paralela

A fala gravada era *"nenhuma dessas é aprender sobre I.A. São coisas rodando no seu negócio já na
segunda-feira"*. Isso é o padrão "não é X. É Y.", que tem cara de IA e é aviso no gate. A fala
nova é afirmação seca, sem negar antes de afirmar: *"E presta atenção: já na segunda-feira você
tem coisa rodando no seu negócio. Sem esperar ninguém pra isso."* O bloco continua sem insert e
sem KEY, com 18 palavras (abaixo do teto de 25), que é onde a garrafal G2 SEGUNDA-FEIRA vive: a
âncora "segunda-feira" segue na fala, que é o que a garrafal exige.

### 7. Frases longas foram partidas, sem inventar nada

Frase acima de 14 palavras é aviso, acima de 20 reprova. Os blocos 4, 6, 8 e 9 tinham uma frase
só, comprida. Foram partidas em duas, e onde faltava palavra pro mínimo do insert entrou uma
frase curta na voz do apresentador, sem número, prazo, preço ou prova nova (tudo dentro do preset
de oferta):

- bloco 4: *"Três: uma prospecção rodando sozinha. Buscando cliente pra você todo santo dia,
  sempre no mesmo horário."* (16 palavras, com folga sobre os 15 do insert)
- bloco 6: *"...que filtra quem entra. E manda o lead pronto pro seu WhatsApp."*
- bloco 8: *"E olha, não é à toa. Mais de oito mil pessoas já passaram pelos meus treinamentos."*
- bloco 9: *"São dois dias, do zero, mesmo que você nunca tenha criado uma automação."* (a segunda frase deste bloco é a ponte, ver a mudança 12)

### 8. Rodízio de formas: o mapa aprovado entra inteiro

"Placa" não é uma forma: o rodízio são os TRÊS estilos de placa, `h1`, `h2` e `h4`, mais as duas
alternativas (`coluna` e `carimbo`) e a `seta_cta` do fechamento. A regra de não repetir em bloco
vizinho vale sobre esse domínio, então h1 seguida de h2 é rodízio funcionando, não repetição. E
forma repetida em vizinho é **aviso**, não reprovação.

Com essa leitura, a sequência aprovada pelo cliente passa como está, e é ela que este pacote usa:

```
1 placa_h2  ->  2 placa_h1  ->  3 placa_h2  ->  4 coluna  ->  6 placa_h4  ->  7 placa_h1  ->  8 carimbo  ->  10 seta_cta
```

O gancho (bloco 1) é a `h2` da L0, que a decisão 10 já tinha desenhado e que não entra no rodízio
do corpo. As duas `h1` (blocos 2 e 7) ficam a quatro letterings de distância uma da outra, e as
duas `h2` (blocos 1 e 3) têm a `h1` do bloco 2 entre elas. O carimbo fica no bloco 8, que tem
insert: carimbo é lettering de APOIO e só entra em bloco com insert, porque ele existe pra marcar
onde a peça está quando o insert já é o assunto.

### 9. Hooks B e C foram reescritos

Os dois hooks propostos no material original abriam com a antítese paralela ("isso aqui não é
aprender I.A. É coisa rodando..."), e o C ainda tinha 19 palavras. Os novos:

| hook | id | fala | palavras | âncora |
|---|---|---|---|---|
| A | curiosity | Em dois dias você sai da Operação Claude Code com cinco entregas prontas. | 13 | dois dias (palavras 2 e 3) |
| B | contrarian | Estudar I.A não põe nada rodando no seu negócio, e você já sabe disso. | 14 | estudar I.A (palavras 1 e 2) |
| C | bold_claim | Ó, cinco coisas prontas em dois dias, rodando no teu negócio. | 11 | cinco coisas prontas (palavras 2 a 4) |

Os três ids são distintos. Todos abaixo de 14 palavras, todos com a âncora de problema ou
promessa dentro das 4 primeiras palavras, nenhum abrindo com marca nas 3 primeiras palavras,
nenhum com antítese paralela. O C é o hook cru do R1.5: `lettering: nenhum`, sem avatar em tela,
marcador de fala real ("Ó").

O C é `bold_claim` e não `myth_busting`: a promessa contável da oferta dita de uma vez ("cinco
coisas prontas") crava mais do que derrubar a crença de que I.A exige programador, e ela põe a
âncora nas palavras 2 a 4 sem depender de pergunta retórica. Os dois ids estão no mesmo cluster
`interrupcao_padrao`, então a troca não mexe na regra de cluster por objetivo (R1.4). O nome das
peças em `matriz.md` acompanhou: as quatro que citavam `myth_busting` passam a citar
`bold_claim`.

### 10. `objetivo: carrinho`, não `frio`

O material original declarava objetivo `frio` junto com campanha `carrinho`. Como o lote está
aberto, o objetivo do pacote é `carrinho`, o que libera o cluster `promocional` além de
`interrupcao_padrao` e `curiosidade`. Quem libera a escassez "ainda tem vaga" no CTA é o campo
`campanha`; o `objetivo` só governa o cluster do hook.

### 11. Assets: origem declarada linha a linha

`assets.md` segue as decisões 34 e 35: o insert é feito com o que foi PASSADO, e só onde não
havia nada pronto a esteira cria (e propõe antes). Por isso squad = `galeria` (banco de assets da
casa, variante 2, decisão 18), prospecção e pipoca = `doc`, terminal e quiz = `criar:ui_html`
(mockups aprovados na decisão 16) e página = `criar:captura` (decisão 19). Enquadramento `inteiro` em todos
(decisão 15).

O asset da prospecção entra com `serve: não` e ressalva: ele veio borrado da origem. Pela decisão
35 a copy NÃO troca o asset por conta própria e NÃO esconde o defeito com desfoque ou véu
(decisões 21 e 31): usa como veio e registra a ressalva pra quem produziu.

### 12. O bloco 9 ganhou a ponte pro CTA

O gravado ia da quebra de objeção direto pro CTA: *"São dois dias, do zero. Mesmo que você nunca
tenha criado uma automação na vida."* e, no bloco seguinte, *"toca em saiba mais"*. Entre a
objeção e o pedido de clique não havia nada dizendo **o que o clique entrega**, e isso reprova.

A fala nova fecha o bloco 9 com a ponte: *"São dois dias, do zero, mesmo que você nunca tenha
criado uma automação. **É isso que a gente monta junto no evento.**"* A frase nomeia o que a pessoa
leva, amarra na objeção que acabou de ser derrubada e diz onde acontece. Só então o CTA pede a
ação.

O bloco passou de 15 para 22 palavras (5,23s finais, ainda abaixo do teto de 25 palavras de
apresentador sozinho), e `cta.md` ganhou o campo `- ponte: bloco 9, "É isso que a gente monta junto
no evento"`, que declara onde a ponte mora.

## Os 13 avisos que este pacote assume, de propósito

Aviso não reprova. Estes são os treze que o gate levanta, declarados aqui para ninguém achar que
passaram despercebidos. Rodando `python3 scripts/gate_copy.py exemplos/cinco-entregas`, são esses e
mais nada: **zero reprovações**.

### 1 e 2. Marca dentro das 12 primeiras palavras, com o logo ancorado declarado

Dois avisos, um no bloco 1 do roteiro e outro no Hook A. "Operação Claude Code" começa na palavra
7, ou seja fora das 3 primeiras (que reprovam sempre) mas dentro dos 3s finais. Sem declaração isso
**reprovaria** (R2.5); o que baixa para aviso é a decisão 11, e ela precisa estar escrita: o Hook A
leva `- logo_ancorado: sim` em `hooks.md`, porque a peça aprovada roda com o logo da Operação
ancorado no instante em que o nome é dito. Quem monta confere a âncora; a copy deixa o gancho do
jeito que a decisão 10 desenhou, com lettering e garrafal.

### 3 a 7. Cinco LEADs que não estão na fala

Os LEADs "entrega cinco", "entrega quatro", "entrega três", "entrega dois" e "entrega um" (blocos
2, 3, 4, 6 e 7) usam a palavra "entrega", que a fala daqueles blocos não diz: a fala conta "Cinco:
um squad", "Quatro: as suas próprias skills" e assim por diante. É o contador da contagem
regressiva, e LEAD fora da fala é aviso, não reprovação. A alternativa seria escrever "entrega
cinco" na fala de cada bloco, o que soaria a locução e custaria palavras que o mínimo do insert
precisa.

### 8, 9 e 10. Três assets com origem `criar:*`

O terminal e o quiz são `criar:ui_html`, a página é `criar:captura`. O gate avisa em toda criação
própria, porque ela tem que ser proposta ao cliente antes de ser produzida. Os três já têm
aprovação registrada (decisões 16 e 19), e a linha de `assets.md` diz qual.

### 11. Blocos 9 e 10 somam 9,04s sem insert

O teto de dois blocos vizinhos sem insert é 6,0s. São a quebra de objeção final e o CTA, que por
desenho não levam insert: a garrafal G3 vive no bloco 9, a **ponte** fecha esse mesmo bloco, e o
fechamento é logo, legenda e CTA juntos. Cortar fala de um dos dois tiraria a ponte ou derrubaria o
bloco abaixo do mínimo do lettering.

### 12. Duração final de 40,67s

As 171 palavras dão 40,67s finais (171 / 4,205). A faixa publicada é a de pago frio, 15 a 30s.
Faixa própria existe só para `frio` e `remarketing`: `carrinho` e `lote`, que é o caso desta peça,
não têm faixa declarada e usam a de frio como referência. A peça aprovada tem 41,48s, ou seja a
referência de campo desta oferta também está fora da faixa de frio. Por isso o número aqui é aviso
assumido, não erro de escrita.

### 13. Densidade de insert de 99% na janela do corpo

A faixa é de 45% a 55% do tempo de cada janela coberto por insert, medida a partir de 3,0s. No
corpo (3 a 15s) os blocos 2, 3 e 4 são todos de insert e estão colados: 11,91s dos 12,0s da janela,
ou seja **cerca de 99%**. No fecho (15s ao fim) dá 12,35s de 24,0s, **51,4%**, dentro da faixa.

A peça aprovada tem a mesma estrutura de contagem regressiva com os inserts em sequência, então
isso é medição registrada, não defeito da peça. **A correção é de copy e vale para a próxima
leva**: intercalar um bloco de apresentador entre as entregas, para a janela do corpo respirar. É
exatamente o tipo de decisão que o `scripts/planejar_blocos.py` mostra antes de você escrever, e
que o exemplo `exemplos/agenda-cheia/` resolve na origem.

**Uma reprovação que este pacote NÃO leva, e vale dizer por quê**: ele tem **ponte** antes do CTA.
O bloco 9 fecha com *"É isso que a gente monta junto no evento"*, que liga a quebra de objeção ao
que o clique entrega, e o campo `- ponte: bloco 9, "..."` de `cta.md` declara onde ela está. O
anúncio gravado não tinha essa frase: saltava da objeção direto pro "toca em saiba mais", e isso
**reprova** (não avisa). Foi a última mudança aplicada nesta reconstrução.

## Como conferir

```bash
cd ~/.claude/skills/copy-criativos
python3 scripts/gate_copy.py exemplos/cinco-entregas
```

Saída esperada: **13 avisos, zero reprovações**, código de saída 0.
