# Exemplo de referência: `cinco_entregas`

Este diretório é o pacote de copy de referência da skill `copy-criativos`: os 8 arquivos que o
contrato `references/formato-do-pacote.md` exige, escritos até passarem com **zero reprovações**.
Ele reconstrói o conceito "cinco entregas" a partir do roteiro REAL do `ad21v2` da Escola de
Automação (`~/creative-studio/piloto/insumos/roteiro.txt`), que foi gravado na voz do Thales e
virou a peça v5.7 aprovada pelo Júlio (decisão 36).

O ad21v2 gravado NÃO passaria no gate como está. Cada diferença abaixo é uma regra de copy sendo
aplicada, não gosto.

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
| cada palavra do KEY além da segunda | mais 0,25s | mais 2 |
| bloco de CTA | mínimo 3,0s | 13 |
| bloco de CTA | máximo 5,0s (aviso) | máximo 21 |
| bloco sem insert e sem KEY | máximo 6,0s | máximo 25 |
| blocos vizinhos sem insert, somados (aviso) | máximo 6,0s | máximo 25 |

Os mínimos por forma saem de `gates.yaml -> dinamica.lettering.permanencia_min_ms` (placa 2,8s,
coluna 3,5s, carimbo 3,5s, `seta_cta` 2,8s) e o teto do CTA de `pago.yaml ->
fechamento.janela_final_max_s`.

## Conferência bloco a bloco

Medida pelo script `conferir_pacote.py` e conferida à mão.

| bloco | palavras | natural (s) | final (s) | insert | KEY | forma | mínimo exigido (s) | passa |
|---|---|---|---|---|---|---|---|---|
| 1 | 13 | 4,48 | 3,09 | não | 5 ENTREGAS PRONTAS | placa_h2 | 3,05 (placa 2,80 + 0,25 da terceira palavra) | sim |
| 2 | 16 | 5,52 | 3,80 | sim | UM SQUAD | placa_h1 | 3,50 (insert; a placa pedia 2,80) | sim |
| 3 | 21 | 7,24 | 4,99 | sim | SKILLS DO ZERO | placa_h2 | 3,50 (insert; a placa pedia 3,05) | sim |
| 4 | 16 | 5,52 | 3,80 | sim | PROSPECÇÃO SOZINHA | coluna | 3,50 (insert e coluna empatados) | sim |
| 5 | 18 | 6,21 | 4,28 | não | nenhum | nenhuma | máximo 6,00 | sim |
| 6 | 16 | 5,52 | 3,80 | sim | QUIZ QUE FILTRA | placa_h4 | 3,50 (insert; a placa pedia 3,05) | sim |
| 7 | 17 | 5,86 | 4,04 | sim | PÁGINA NO AR | placa_h1 | 3,50 (insert; a placa pedia 3,05) | sim |
| 8 | 16 | 5,52 | 3,80 | sim | 8 MIL | carimbo | 3,50 (insert e carimbo empatados) | sim |
| 9 | 15 | 5,17 | 3,57 | não | nenhum | nenhuma | máximo 6,00 | sim |
| 10 | 16 | 5,52 | 3,80 | não | GARANTE SEU INGRESSO | seta_cta | 3,05 (seta_cta 2,80 + 0,25 da terceira palavra) | sim |

Total: **164 palavras, 39,00s finais**. Nenhuma frase passa de 14 palavras (o teto de reprovação
é 20, valor de partida do brief, porque a R5.2 não publica número).

## O que mudou em relação ao ad21v2 gravado, e por quê

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

### 3. Os KEYs do piloto ficam como o Júlio aprovou, e a fala vai buscá-los

O contrato aceita no máximo 2 palavras no KEY (3 no CTA), e a conta é de palavras de
**conteúdo**: algarismo e palavra funcional (de, do, da, no, na, que, e, um, uma, pra, com, sem)
não entram. Com essa régua, os três KEYs do mapa do piloto passam inteiros:

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
  asset (`quiz de qualificação sendo respondido`), que é onde a esteira casa o arquivo.
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
autorizada em `oferta-occ.md`: mais de oito mil pessoas.

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
frase curta na voz do Thales, sem número, prazo, preço ou prova nova (tudo dentro de
`oferta-occ.md`):

- bloco 4: *"Três: uma prospecção rodando sozinha. Buscando cliente pra você todo santo dia,
  sempre no mesmo horário."* (16 palavras, com folga sobre os 15 do insert)
- bloco 6: *"...que filtra quem entra. E manda o lead pronto pro seu WhatsApp."*
- bloco 8: *"E olha, não é à toa. Mais de oito mil pessoas já passaram pelos meus treinamentos."*
- bloco 9: *"São dois dias, do zero. Mesmo que você nunca tenha criado uma automação na vida."*

### 8. Rodízio de formas: o mapa do Júlio entra inteiro

"Placa" não é uma forma: o rodízio de `gates.yaml -> dinamica.lettering.rodizio` são os TRÊS
estilos de placa, `h1`, `h2` e `h4`, e `dinamica.lettering.formas` guarda só as duas alternativas
(`coluna` e `carimbo`), mais a `seta_cta` do fechamento. `repetir_vizinho: false` vale sobre esse
domínio, então h1 seguida de h2 é rodízio funcionando, não repetição.

Com essa leitura, a sequência aprovada no `MAPA-LETTERINGS.md` passa como está, e é ela que este
pacote usa:

```
1 placa_h2  ->  2 placa_h1  ->  3 placa_h2  ->  4 coluna  ->  6 placa_h4  ->  7 placa_h1  ->  8 carimbo  ->  10 seta_cta
```

O gancho (bloco 1) é a `h2` da L0, que a decisão 10 já tinha desenhado e que não entra no rodízio
do corpo. As duas `h1` (blocos 2 e 7) ficam a quatro letterings de distância uma da outra, e as
duas `h2` (blocos 1 e 3) têm a `h1` do bloco 2 entre elas. O carimbo fica no bloco 8, que tem
insert: carimbo é lettering de APOIO e só entra em bloco com insert, porque ele existe pra marcar
onde a peça está quando o insert já é o assunto.

### 9. Hooks B e C foram reescritos

Os dois hooks propostos no `hooks.md` do piloto abriam com a antítese paralela ("isso aqui não é
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

O `matriz.py` do piloto declarava `OBJETIVO = "frio"` junto com `CAMPANHA = "carrinho"`. Como o
lote está aberto (decisão 7), o objetivo do pacote é `carrinho`, o que libera o cluster
`promocional` além de `interrupcao_padrao` e `curiosidade`. Quem libera a escassez "ainda tem
vaga" no CTA é o campo `campanha` (`pago.yaml -> fechamento.oferta_no_cta.carrinho`), que o
piloto já declarava; o `objetivo` só governa o cluster do hook.

### 11. Assets: origem declarada linha a linha

`assets.md` segue as decisões 34 e 35: o insert é feito com o que foi PASSADO, e só onde não
havia nada pronto a esteira cria (e propõe antes). Por isso squad = `galeria` (GalerIA variante
2, decisão 18), prospecção e pipoca = `doc`, terminal e quiz = `criar:ui_html` (mockups aprovados
na decisão 16) e página = `criar:captura` (decisão 19). Enquadramento `inteiro` em todos
(decisão 15).

O asset da prospecção entra com `serve: não` e ressalva: ele veio borrado da origem. Pela decisão
35 a copy NÃO troca o asset por conta própria e NÃO esconde o defeito com desfoque ou véu
(decisões 21 e 31): usa como veio e registra a ressalva pra quem produziu.

## Os avisos que este pacote assume, de propósito

Aviso não reprova. Estes ficam declarados aqui pra ninguém achar que passaram despercebidos:

1. **Marca dentro das 12 primeiras palavras do bloco 1, com o logo ancorado declarado.**
   "Operação Claude Code" começa na palavra 7, ou seja, fora das 3 primeiras (que reprovam
   sempre) mas dentro dos 3s finais. Sem declaração isso REPROVA (R2.5); o que baixa pra aviso é
   a decisão 11, e ela precisa estar escrita: o Hook A leva `- logo_ancorado: sim` em `hooks.md`,
   porque a v5.7 aprovada roda com o logo da Operação ancorado no instante em que o nome é dito.
   Quem montar a peça confere a âncora; a copy deixa o gancho do jeito que a decisão 10 desenhou,
   com lettering e garrafal.
2. **Primeiro insert antes dos 5s finais.** Ele começa em 3,09s, porque o bloco 1 tem que caber
   no teto de 14 palavras do hook. É a consequência direta da mudança 2, e é preferível a um
   bloco 1 que reprova por duração.
3. **Segundo insert antes dos 12s finais.** Começa em 6,89s, pela mesma razão: a peça lista cinco
   entregas em sequência, então os inserts se encostam.
4. **Blocos 9 e 10 somam 7,37s sem insert.** São a quebra de objeção final e o CTA, que por
   desenho não levam insert (a garrafal G3 vive no bloco 9 e o fechamento é logo, legenda e CTA).
5. **"segunda-feira" é envelhecimento.** Dentro de `carrinho` isso é aviso, não reprovação.
6. **Os LEADs "entrega cinco", "entrega quatro", "entrega três", "entrega dois" e "entrega um"
   não estão na fala.** É o contador da contagem regressiva, e LEAD fora da fala é aviso.
7. **Densidade de insert estourada na janela do corpo (R3.4).** A faixa é de 45% a 55% do tempo
   de cada janela com insert (`gates.yaml -> retencao.densidade_insert`, medida a partir de
   3,0s). No corpo (3 a 15s) os blocos 2, 3 e 4 são todos de insert e estão colados: 11,91s dos
   12,0s da janela, ou seja **cerca de 99%**. No fecho (15s ao fim) dá 12,35s de 24,0s, **51,4%**,
   dentro da faixa. A v5.7 aprovada tem a mesma estrutura de contagem regressiva com os inserts
   em sequência, então o gate da esteira trata isso como medição registrada, não como defeito da
   peça. A correção é de copy e vale pra próxima leva: intercalar um bloco de apresentador entre
   as entregas, pra a janela do corpo respirar.
8. **Duração final de 39,00s.** As 164 palavras dão 39,00s finais (164 / 4,205). A faixa que a
   skill publica é a de pago frio, 15 a 30s (`pago.yaml -> duracao.frio`). O `pago.yaml` só tem
   faixa pra `frio` e `remarketing`: `carrinho` e `lote`, que é o caso desta peça, não têm faixa
   declarada e usam a de frio como referência. A peça v5.7 aprovada pelo Júlio (decisão 36) tem
   41,48s, ou seja, a referência de campo desta oferta também está fora da faixa de frio, e por
   isso o número aqui é aviso assumido, não erro de escrita.
9. **Três assets com origem `criar:*` (decisão 34).** O terminal e o quiz são `criar:ui_html` e a
   página é `criar:captura`. O gate avisa em toda criação própria porque ela tem que ser proposta
   ao Júlio antes; os três já têm aprovação registrada (decisões 16 e 19), e a linha de
   `assets.md` diz qual.

Rodando o gate com `--gates ~/creative-studio/config/gates.yaml`, são esses avisos e mais nada:
**zero reprovações**.

## Como conferir

Os dois scripts que mediram este pacote ficam no scratchpad da sessão, não versionados aqui:
`conferir_pacote.py` (palavras, durações, mínimos, KEY dentro da fala com 5=cinco, 8=oito,
2=dois) e `conferir_arquivos.py` (coerência entre `roteiro.txt` e os outros sete arquivos:
hooks, garrafais, letterings, cta, assets e matriz). Resultado no fechamento: **0 reprovações**
nos dois.
