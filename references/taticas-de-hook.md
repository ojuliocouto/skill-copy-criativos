# Táticas de hook (biblioteca R1.4)

Tática de hook é o MOLDE da primeira frase: o mecanismo psicológico que faz a pessoa parar, não o assunto do anúncio. A R1.4 exige que todo hook tenha tática NOMEADA, escolhida antes de escrever a fala, porque hook sem tática declarada não dá pra testar nem pra trocar quando o número cai (R2.8): sem nome, três variações viram três palpites do mesmo jeito.

A biblioteca é a união das duas listas da Motion 2026 (25 por hit rate mais 25 por spend use ratio), 29 táticas em 8 clusters. O que o gate valida é o CLUSTER, e o cluster depende do objetivo:

| objetivo | clusters liberados |
|---|---|
| tráfego frio (pago ou orgânico) | `interrupcao_padrao`, `curiosidade` |
| carrinho, lote ou prazo | `interrupcao_padrao`, `curiosidade`, `promocional` |

Em frio, promoção antes do problema é marca antes da promessa. Os outros cinco clusters (`prova`, `demonstracao`, `educacional`, `narrativa`, `direto`) são vocabulário de trabalho: servem pro corpo da peça, pro orgânico de meio de funil e pra remarketing declarado, nunca pra abrir tráfego frio sem passar pelo Júlio.

Todo hook, de qualquer cluster, tem que ter:

1. Problema ou promessa nomeado nas 4 primeiras palavras (R2.6 pede até 1,2s de fala; em ritmo de 2,5 a 3 palavras por segundo, isso são 3 ou 4 palavras).
2. Nenhuma marca, logo ou nome de produto nas 3 primeiras palavras (R2.5 proíbe marca nos 3 primeiros segundos).
3. Nenhuma apresentação nas duas primeiras frases: "eu sou o Thales", "aqui é da Escola" e saudação estão fora (R2.6).
4. No máximo 14 palavras, pra caber em até 5 segundos de fala.
5. Um dos 3 hooks do conceito é CRU (R1.5): escrito como nota de voz, com "ó", "olha", "cara", pausa de fala, e sem lettering de abertura.

Honestidade sobre a fonte: a spec nomeia 16 das 29 táticas. As outras 13 completam a união com o vocabulário corrente de tática de hook e estão marcadas `citada_na_spec: false` no `config/taticas_hook.yaml`; nas tabelas abaixo elas aparecem com **não** na coluna "na spec". Antes do lote piloto, conferir esses 13 nomes contra o relatório da Motion e trocar o que não bater. Nenhuma decisão de gate depende deles: os dois clusters 100% da spec são `interrupcao_padrao` e `promocional`. O terceiro cluster liberado em frio, `curiosidade`, NÃO é inteiro da spec: `curiosity` é da spec, mas `question` está marcada `citada_na_spec: false`. Ou seja, em tráfego frio o `question` é o único nome que ainda depende da conferência contra o relatório da Motion.

Todo exemplo abaixo usa só números e provas de `oferta-occ.md`. Nada inventado, e nada esticado
além do que o preset autoriza:

- o volume de gente é **"mais de 8 mil pessoas já passaram pelo treinamento"**. É passagem pelo
  treinamento, não resultado obtido: por isso o `social_proof` diz "já passaram" e não "já
  montaram time de I.A desse jeito", que seria prova de resultado que ninguém autorizou;
- os **"mais de R$48.000 por ano"** são a economia do **time de vídeo** (Ads Machine, que saiu de
  10 a 20 vídeos por mês pra 100), não de um time qualquer: o `price_anchor` diz de quem é o
  número. O exemplo fala em "quarenta e oito mil" redondo, e não em "mais de quarenta e oito
  mil", só pra a âncora caber nas 4 primeiras palavras dentro do teto de 14; citar menos do que o
  preset autoriza nunca infla o claim.

---

## interrupcao_padrao

Liberado em tráfego frio e em carrinho. É o cluster padrão de abertura de ad frio.

| id | tática | o que faz | exemplo na voz da casa | âncora | na spec |
|---|---|---|---|---|---|
| `confession` | Confession | admite um erro próprio pra baixar a guarda de quem assiste | "Ó, fiz na mão, por meses, o que a máquina faz sozinha." **(cru)** | "na mão", palavras 3 e 4 | sim |
| `contrarian` | Contrarian | contraria o que o público assume como verdade | "Aprender I.A. não põe um real no seu caixa." | "não põe", palavras 3 e 4 | sim |
| `shocking_statement` | Shocking Statement | afirma algo que assusta e obriga a checar | "Seu concorrente já tem um time inteiro trabalhando de madrugada." | "concorrente já", palavras 2 e 3 | sim |
| `warning` | Warning | avisa de um risco que a pessoa está correndo agora | "Cuidado: contratar mais gente pra tarefa que a máquina já faz." | "contratar mais gente", palavras 2 a 4 | sim |
| `myth_busting` | Myth Busting | derruba uma crença repetida do nicho | "Saber programar virou mito. Eu monto tudo sem uma linha." | "programar virou mito", palavras 2 a 4 | sim |
| `bold_claim` | Bold Claim | crava uma promessa grande e específica | "Cinco entregas prontas em dois dias, funcionando no seu negócio." | "cinco entregas prontas", palavras 1 a 3 | sim |
| `reverse_psychology` | Reverse Psychology | desqualifica parte do público pra atrair o resto | "Não monta time de I.A. quem gosta de trabalhar dobrado." | "monta time", palavras 2 e 3 | sim |

## curiosidade

Liberado em tráfego frio e em carrinho.

| id | tática | o que faz | exemplo na voz da casa | âncora | na spec |
|---|---|---|---|---|---|
| `curiosity` | Curiosity | abre um laço e adia o fechamento pro corpo da peça | "Em dois dias você sai com cinco coisas prontas. Começo pela que muda tudo." | "dois dias", palavras 2 e 3 | sim |
| `question` | Question | pergunta direta que a pessoa responde na cabeça | "Ó, seu dia inteiro some em tarefa repetida, você percebeu isso?" **(cru)** | "seu dia", palavras 2 e 3 | **não** |

## promocional

Liberado só em carrinho, lote ou prazo. Em frio, reprova.

| id | tática | o que faz | exemplo na voz da casa | âncora | na spec |
|---|---|---|---|---|---|
| `newness` | Newness | vende o fato de ser novo, formato ou coisa que não existia | "Saiu agora: cinco entregas prontas em dois dias de imersão." | "cinco entregas", palavras 3 e 4 | sim |
| `price_anchor` | Price Anchor | ancora num custo grande pra reposicionar o preço | "Quarenta e oito mil por ano é o que o time de vídeo economiza." | "quarenta e oito mil", palavras 1 a 4 | sim |
| `urgency` | Urgency | põe prazo ou limite explícito na decisão | "Ó, ainda tem vaga pra imersão de dois dias. Vai fechar." **(cru)** | "tem vaga", palavras 3 e 4 | sim |
| `fomo` | FOMO | mostra o grupo que já está dentro | "Mais de oito mil já passaram por isso, você ficou de fora." | "oito mil", palavras 3 e 4 | sim |
| `event_announcement` | Event Announcement | anuncia o evento como acontecimento com data | "Dois dias de imersão montando seus times de I.A. na prática." | "dois dias", palavras 1 e 2 | sim |

## prova

Corpo da peça, orgânico de meio e remarketing declarado. Não abre frio.

| id | tática | o que faz | exemplo na voz da casa | âncora | na spec |
|---|---|---|---|---|---|
| `testimonial` | Testimonial | usa o caso de uma pessoa nomeada | "Olha, a Rafaele montou uma skill que minera anúncio sozinha." **(cru)** | "Rafaele montou", palavras 3 e 4 | **não** |
| `social_proof` | Social Proof | usa o volume de gente que já fez | "Mais de oito mil pessoas já passaram por esse treinamento comigo." | "oito mil", palavras 3 e 4 | **não** |
| `statistic` | Statistic | abre com o número que resume o resultado | "Vinte vídeos por mês viraram cem, com o mesmo time." | "vinte vídeos", palavras 1 e 2 | **não** |
| `authority` | Authority | ancora em quem faz a coisa por dentro | "Roda na minha empresa todo dia, e eu vou te mostrar." | "roda na minha empresa", palavras 1 a 4 | **não** |

## demonstracao

Corpo da peça, orgânico de meio e remarketing declarado. Não abre frio. É aqui que mora o hook demonstrativo do método da Jheni: quando existe tela, a tela abre e a prova vem antes da promessa.

| id | tática | o que faz | exemplo na voz da casa | âncora | na spec |
|---|---|---|---|---|---|
| `demonstration` | Demonstration | mostra a coisa funcionando já no primeiro frame | "Ó, prospecção rodando sozinha aqui na tela, ninguém do time tocou." **(cru)** | "prospecção rodando", palavras 2 e 3 | **não** |
| `before_after` | Before and After | põe o estado antigo e o novo com número real | "Vinte vídeos por mês era o teto. Hoje saem cem." | "vinte vídeos", palavras 1 e 2 | **não** |
| `comparison` | Comparison | compara o custo ou o esforço de dois caminhos | "Freelancer, ferramenta e salário pra fazer o que a skill faz." | "freelancer, ferramenta e salário", palavras 1 a 4 | **não** |
| `unboxing` | Unboxing | abre do zero na frente de quem assiste | "Vou abrir do zero e montar a primeira skill na tua frente." | "do zero", palavras 3 e 4 | **não** |

## educacional

Corpo da peça e orgânico. Não abre frio.

| id | tática | o que faz | exemplo na voz da casa | âncora | na spec |
|---|---|---|---|---|---|
| `reasons_why` | Reasons Why | promete os motivos por trás de um problema conhecido | "Automação quebra toda semana por três motivos, e o terceiro dói." | "automação quebra", palavras 1 e 2 | sim |
| `how_to` | How To | promete o passo a passo de uma coisa específica | "Como colocar prospecção pra rodar sozinha sem escrever uma linha de código." | "prospecção", palavra 3 | **não** |
| `listicle` | Listicle | anuncia uma lista contável de entregas ou erros | "Olha, cinco coisas prontas, rodando, uma por uma, no teu negócio." **(cru)** | "cinco coisas prontas", palavras 2 a 4 | **não** |
| `problem_solution` | Problem Solution | nomeia a dor e promete a saída na mesma frase | "Tarefa repetida come o dia do seu time. Isso tem solução." | "tarefa repetida", palavras 1 e 2 | **não** |

## narrativa

Corpo da peça e orgânico. Não abre frio.

| id | tática | o que faz | exemplo na voz da casa | âncora | na spec |
|---|---|---|---|---|---|
| `storytelling` | Storytelling | conta o caso de alguém do começo ao resultado | "O Ricardo montou uma skill que lê o WhatsApp dele inteiro." | "Ricardo montou", palavras 2 e 3 | sim |
| `relatability` | Relatability | descreve a cena exata do dia da pessoa | "Cara, sexta à noite e você ainda fazendo o que dá pra automatizar." **(cru)** | "sexta à noite", palavras 2 a 4 | **não** |

## direto

Remarketing e carrinho, quando a pessoa já sabe o que é. Não abre frio.

| id | tática | o que faz | exemplo na voz da casa | âncora | na spec |
|---|---|---|---|---|---|
| `call_to_action_first` | Call to Action First | pede a ação na primeira linha, com a promessa colada | "Ó, garante os dois dias e sai com cinco coisas rodando." **(cru)** | "dois dias", palavras 4 e 5 | sim |

Observação sobre `direto`: é a única tática em que a promessa não cabe nas 4 primeiras palavras, porque o verbo de ação ocupa a abertura. Por isso ela não vale pra frio, onde a R2.6 é gate.

---

## Como montar o trio de um conceito

Regra 3-2-2 do Léo: cada conceito sai em 3 hooks, 2 legendas e 2 formatos. O hook é o eixo que mais move resultado, então:

- Os 3 hooks têm ids DIFERENTES. Dois hooks do mesmo id colidem no nome da peça e viram a mesma variação com outra fala.
- Em frio, os 3 saem de `interrupcao_padrao` ou `curiosidade`.
- Ao menos 1 dos 3 é cru (R1.5): nota de voz, sem lettering de abertura.
- Cada fala passa pela conferência antes de virar áudio: contar palavras (máximo 14), achar a âncora nas 4 primeiras palavras, checar que não abre com marca e que não tem antítese paralela.

### Trio de exemplo: conceito "cinco entregas em dois dias"

| # | fala | tática | âncora | por que |
|---|---|---|---|---|---|
| A | "Em dois dias você sai com cinco coisas prontas. Começo pela que muda tudo." | `curiosity` | "dois dias", palavras 2 e 3 | a promessa inteira aparece e o laço fica aberto no "que muda tudo" |
| B | "Cuidado: contratar mais gente pra tarefa que a máquina já faz." | `warning` | "contratar mais gente", palavras 2 a 4 | ataca o custo que o dono já sente antes de citar qualquer entrega |
| C | "Olha, cinco coisas prontas, rodando, uma por uma, no teu negócio." **(cru)** | `listicle` | "cinco coisas prontas", palavras 2 a 4 | mesma promessa em nota de voz, sem lettering, pra testar o efeito do tratamento |

Conferência das três falas:

- Contagem: A tem 14 palavras, B tem 11, C tem 11. Todas dentro do teto.
- Âncora: A nas palavras 2 e 3, B nas 2 a 4, C nas 2 a 4. Todas dentro das 4 primeiras.
- Marca: nenhuma abre com "Operação Claude Code", "Claude" ou "Escola". A primeira menção de produto fica pro corpo, depois dos 3s (R2.5).
- Antítese paralela: nenhuma usa "não é X, é Y", "todo mundo X, ninguém Y" nem "enquanto uns X, outros Y".
- Apresentação: nenhuma tem saudação nem "eu sou o Thales" (R2.6).
- Cru: C é a nota de voz, com "olha" e pausa de fala, e não leva lettering de abertura (R1.5).
- Ids distintos: `curiosity`, `warning`, `listicle`. Em frio, C precisa ser trocada por uma tática de `interrupcao_padrao` ou `curiosidade`, porque `listicle` é educacional. A versão frio de C: "Ó, cinco coisas prontas em dois dias, rodando no teu negócio." com `bold_claim`.
