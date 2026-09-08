# Táticas de hook (biblioteca R1.4)

Tática de hook é o MOLDE da primeira frase: o mecanismo psicológico que faz a pessoa parar, não o assunto do anúncio. A R1.4 exige que todo hook tenha tática NOMEADA, escolhida antes de escrever a fala, porque hook sem tática declarada não dá pra testar nem pra trocar quando o número cai (R2.8): sem nome, três variações viram três palpites do mesmo jeito.

A biblioteca reúne 29 táticas em 8 clusters, vindas das duas listas de referência de mercado (uma por hit rate, outra por spend use ratio). O que o gate valida é o CLUSTER, e o cluster depende do objetivo:

| objetivo | clusters liberados |
|---|---|
| tráfego frio (pago ou orgânico) | `interrupcao_padrao`, `curiosidade` |
| carrinho, lote ou prazo | `interrupcao_padrao`, `curiosidade`, `promocional` |

Em frio, promoção antes do problema é marca antes da promessa. Os outros cinco clusters (`prova`, `demonstracao`, `educacional`, `narrativa`, `direto`) são vocabulário de trabalho: servem pro corpo da peça, pro orgânico de meio de funil e pra remarketing declarado, nunca pra abrir tráfego frio sem o cliente aprovar antes.

Todo hook, de qualquer cluster, tem que ter:

1. Problema ou promessa nomeado nas 4 primeiras palavras (R2.6 pede até 1,2s de fala; em ritmo de 2,5 a 3 palavras por segundo, isso são 3 ou 4 palavras).
2. Nenhuma marca, logo ou nome de produto nas 3 primeiras palavras (R2.5 proíbe marca nos 3 primeiros segundos).
3. Nenhuma apresentação nas duas primeiras frases: "eu sou o", "meu nome é", "aqui é da" e qualquer saudação estão fora (R2.6).
4. Até 5s de fala natural (14 palavras a 2,9 por segundo; o gate arredonda pra cima, então 15
   ainda passa).
5. Um dos 3 hooks do conceito é CRU (R1.5): escrito como nota de voz, com "ó", "olha", "cara", pausa de fala, e sem lettering de abertura.
6. **Ao menos um dos 3 hooks do conceito é pergunta ou paradoxo.** O gate avisa quando nenhum é.

## Pergunta paradoxal: a forma que mais segura

A tática nomeia o mecanismo; a **forma** da frase decide se ele funciona. E a forma que mais segura
é a **pergunta paradoxal**: uma frase que junta duas coisas que não deveriam andar juntas, e que a
pessoa não consegue deixar passar sem resolver.

Afirmação correta e previsível é o erro mais comum de hook. "Cada cliente que espera resposta no
WhatsApp já foi marcar em outra clínica" está certa, e é exatamente por isso que ela não segura
ninguém: quem tem clínica já sabe, concorda com a cabeça e continua rolando o feed. Não sobrou
nada pra descobrir.

O paradoxo obriga a parar e **fazer a conta**, e o corpo da peça inteiro é a resposta dessa conta.
É isso que compra os segundos seguintes.

Três exemplos na voz da casa:

- "Sua clínica perde cliente justamente na hora que está mais cheia? Pensa comigo." (cheia deveria
  ser bom, e a frase diz que é ali que ela perde)
- "Quanto mais gente você contrata, mais tarde o time entrega? Não é acaso." (contratar deveria
  acelerar, e a frase diz que atrasa)
- "Você paga por anúncio e o problema tá acontecendo depois do clique." (o gasto está num lugar, o
  problema está em outro)

Como montar uma: pegue o resultado que o público persegue, pegue o momento em que ele acha que
está indo bem, e mostre que é ali que a perda acontece. Depois entregue a explicação no corpo, na
ordem: causa, mecanismo, prova.

Duas armadilhas: paradoxo não é antítese paralela ("não é X, é Y" continua banido, ver
`references/voz-e-anti-ia.md`), e a pergunta precisa ser respondível pela peça. Pergunta que a
peça não responde é isca, e isca queima o perfil.

### As perguntas reais da casa

Calibração contra treze anúncios já escritos e gravados (`references/calibracao-jheni.md`). O
número entre parênteses é o anúncio de origem. Duas coisas a aprender com elas.

**Primeira: quando a pergunta abre, ela pergunta o TAMANHO de uma perda que a pessoa nunca contou.**

- "Quantas vendas a sua empresa perdeu esse mês por causa do mal atendimento no whatsapp?" (AD3)
- "Adivinha quanto eu pago de hospedagem pra tudo que eu publico? ZERO." (AD11, pergunta com a
  resposta colada, e a resposta é que não fecha a conta)
- "Tá vendo esse sisteminha aqui em cima?" (AD4, pergunta demonstrativa: aponta a tela e obriga a
  olhar)

**Segunda, e é a mais importante: no material da casa a pergunta é motor de CORPO, não de abertura.**
Dos treze anúncios, só um abre com pergunta, mas **doze** têm pergunta no corpo, sempre em um de
três lugares:

| lugar | o que a pergunta faz | exemplos reais |
|---|---|---|
| **virada** | interrompe a lista e força a conta antes do mecanismo | "Mas afinal, será que somos gênios da tecnologia por ter construído tudo isso?" (AD6); "Aonde nós vamos parar? É o fim das agências?" (AD8); "A pergunta certa é: como se manter relevante no mercado de marketing apesar da IA?" (AD9) |
| **antes do exemplo** | compra o bloco seguinte por duas palavras | "Quer um exemplo?" (AD2, AD9); "Sabe porque?" (AD12); "Quer saber a verdade?" (AD2) |
| **ponte pro CTA** | vira pergunta de adesão, e o "Então" costura no clique | "Topa aprender a criar seu primeiro time de I.A junto comigo?" (AD13); "Quer aprender a fazer isso na prática? Então seja rápido." (AD11) |

**O que isso muda na prática**: a regra de que um dos três hooks é pergunta ou paradoxo continua de
pé, porque é o hook que segura o dedo. Mas escrever pergunta só no bloco 1 e nenhuma no corpo é
metade do trabalho. A peça inteira ganha ritmo quando a pergunta reaparece na virada e na ponte, e
o `references/metodo-de-copy.md` cobra isso no checklist de estrutura.

Honestidade sobre a fonte: 16 das 29 táticas vêm nomeadas da especificação original; as outras 13 completam a lista com o vocabulário corrente de tática de hook, e nas tabelas abaixo aparecem com **não** na coluna "na spec". Nenhuma decisão de gate depende delas: os dois clusters inteiramente da spec são `interrupcao_padrao` e `promocional`. O terceiro cluster liberado em frio, `curiosidade`, não é inteiro da spec: `curiosity` é, `question` não. Ou seja, em tráfego frio o `question` é o único nome que carrega essa ressalva.

### Sobre os exemplos abaixo

Todos os exemplos usam a oferta e as provas do exemplo real da skill (`exemplos/cinco-entregas/`),
e nenhum deles estica o que o preset de oferta autoriza. Duas leituras que valem pra qualquer
preset que você monte:

- o volume de gente é **"mais de oito mil pessoas já passaram pelo treinamento"**. É passagem pelo
  treinamento, **não resultado obtido**: por isso o `social_proof` diz "já passaram" e não "já
  montaram time de I.A desse jeito", que seria prova de resultado que ninguém autorizou;
- o número de economia é do **time de vídeo**, não de um time qualquer: o `price_anchor` diz **de
  quem é o número**. O exemplo fala em "quarenta e oito mil" redondo, e não em "mais de quarenta e
  oito mil", só pra a âncora caber nas 4 primeiras palavras dentro do teto de 14. Citar **menos**
  do que o preset autoriza nunca infla o claim; citar mais, sempre.

Quando você escrever com outra oferta, o preset dela (`references/modelo-preset-oferta.md`) é que
manda, e cada número do hook aponta pra uma linha dele.

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
| `testimonial` | Testimonial | usa o caso de uma pessoa nomeada | "Olha, uma aluna montou uma skill que minera anúncio sozinha." **(cru)** | "uma aluna montou", palavras 2 a 4 | **não** |
| `social_proof` | Social Proof | usa o volume de gente que já fez | "Mais de oito mil pessoas já passaram por esse treinamento comigo." | "oito mil", palavras 3 e 4 | **não** |
| `statistic` | Statistic | abre com o número que resume o resultado | "Vinte vídeos por mês viraram cem, com o mesmo time." | "vinte vídeos", palavras 1 e 2 | **não** |
| `authority` | Authority | ancora em quem faz a coisa por dentro | "Roda na minha empresa todo dia, e eu vou te mostrar." | "roda na minha empresa", palavras 1 a 4 | **não** |

## demonstracao

Corpo da peça, orgânico de meio e remarketing declarado. Não abre frio. É aqui que mora o **hook demonstrativo**: quando existe tela pra mostrar, a tela abre a peça e a prova vem antes da promessa.

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
| `storytelling` | Storytelling | conta o caso de alguém do começo ao resultado | "Um aluno montou uma skill que lê o WhatsApp dele inteiro." | "aluno montou", palavras 2 e 3 | sim |
| `relatability` | Relatability | descreve a cena exata do dia da pessoa | "Cara, sexta à noite e você ainda fazendo o que dá pra automatizar." **(cru)** | "sexta à noite", palavras 2 a 4 | **não** |

## direto

Remarketing e carrinho, quando a pessoa já sabe o que é. Não abre frio.

| id | tática | o que faz | exemplo na voz da casa | âncora | na spec |
|---|---|---|---|---|---|
| `call_to_action_first` | Call to Action First | pede a ação na primeira linha, com a promessa colada | "Ó, garante os dois dias e sai com cinco coisas rodando." **(cru)** | "dois dias", palavras 4 e 5 | sim |

Observação sobre `direto`: é a única tática em que a promessa não cabe nas 4 primeiras palavras, porque o verbo de ação ocupa a abertura. Por isso ela não vale pra frio, onde a R2.6 é gate.

---

## Como montar o trio de um conceito

Regra 3-2-2: cada conceito sai em 3 hooks, 2 legendas e 2 formatos. O hook é o eixo que mais move resultado, então:

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
- Apresentação: nenhuma tem saudação nem "eu sou o" (R2.6).
- Cru: C é a nota de voz, com "olha" e pausa de fala, e não leva lettering de abertura (R1.5).
- Ids distintos: `curiosity`, `warning`, `listicle`. Em frio, C precisa ser trocada por uma tática de `interrupcao_padrao` ou `curiosidade`, porque `listicle` é educacional. A versão frio de C: "Ó, cinco coisas prontas em dois dias, rodando no teu negócio." com `bold_claim`.
