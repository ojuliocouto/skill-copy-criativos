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

Três exemplos, em três nichos diferentes:

- clínica: "Sua clínica perde cliente justamente na hora que está mais cheia? Pensa comigo."
  (cheia deveria ser bom, e a frase diz que é ali que ela perde)
- móveis planejados: "Quanto mais caro o planejado, mais espaço sobrando na sua cozinha?" (caro
  deveria significar bem resolvido, e a frase diz o contrário)
- contabilidade: "Você paga contador todo mês e descobre o imposto errado só em abril." (o gasto
  está num lugar, o problema está em outro)

Como montar uma: pegue o resultado que o público persegue, pegue o momento em que ele acha que
está indo bem, e mostre que é ali que a perda acontece. Depois entregue a explicação no corpo, na
ordem: causa, mecanismo, prova.

Duas armadilhas: paradoxo não é antítese paralela ("não é X, é Y" continua banido, ver
`references/voz-e-anti-ia.md`), e a pergunta precisa ser respondível pela peça. Pergunta que a
peça não responde é isca, e isca queima o perfil.

### Perguntas do estudo de caso

As perguntas abaixo vêm de **um produto só**: os treze anúncios do estudo de caso
(`references/calibracao-jheni.md`), escritos para um curso de I.A para empresário. O número entre
parênteses é o anúncio de origem. Elas estão aqui pelo **lugar** onde a pergunta aparece, não pelo
assunto: nenhuma delas se copia para outra oferta.

**Primeira: quando a pergunta abre, ela pergunta o TAMANHO de uma perda que a pessoa nunca contou.**

- "Quantas vendas a sua empresa perdeu esse mês por causa do mal atendimento no whatsapp?" (AD3)
- "Adivinha quanto eu pago de hospedagem pra tudo que eu publico? ZERO." (AD11, pergunta com a
  resposta colada, e a resposta é que não fecha a conta)
- "Tá vendo esse sisteminha aqui em cima?" (AD4, pergunta demonstrativa: aponta a tela e obriga a
  olhar)

**Segunda, e é a mais importante: naquele material a pergunta é motor de CORPO, não de abertura.**
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

## Os quatro nichos dos exemplos

Os exemplos das 29 táticas alternam entre quatro nichos fictícios, para deixar claro que a tática é
o molde e o nicho é só a roupa. A mesma tática serve para qualquer produto ou serviço.

| sigla | nicho | natureza |
|---|---|---|
| **CE** | clínica de estética com atendente automático no WhatsApp | serviço local com tela para mostrar |
| **MP** | loja de móveis planejados | produto físico com antes e depois |
| **CT** | escritório de contabilidade para pequenas empresas | serviço sem produto visível |
| **CF** | curso online de confeitaria | infoproduto de outra área |

Onde entraria um número, os exemplos escrevem **`[prova do preset]`**: número, caso e porcentagem
só existem com uma linha do preset de oferta (`references/modelo-preset-oferta.md`) autorizando.
Quando você preencher o placeholder, **reconte as palavras** do hook e reconfira a âncora: o teto
é 14 palavras e a âncora tem que ficar nas 4 primeiras.

---

## interrupcao_padrao

Liberado em tráfego frio e em carrinho. É o cluster padrão de abertura de ad frio.

| id | tática | o que faz | exemplo | nicho | âncora | na spec |
|---|---|---|---|---|---|---|
| `confession` | Confession | admite um erro próprio pra baixar a guarda de quem assiste | "Ó, respondi cliente de madrugada por dois anos. Perdi agenda do mesmo jeito." **(cru)** | CE | "respondi cliente", palavras 2 e 3 | sim |
| `contrarian` | Contrarian | contraria o que o público assume como verdade | "Planejado caro não resolve cozinha pequena. Resolve projeto antes da chapa." | MP | "planejado caro", palavras 1 e 2 | sim |
| `shocking_statement` | Shocking Statement | afirma algo que assusta e obriga a checar | "Seu concorrente paga menos imposto que você fazendo exatamente a mesma coisa." | CT | "concorrente paga menos", palavras 2 a 4 | sim |
| `warning` | Warning | avisa de um risco que a pessoa está correndo agora | "Cuidado: cobrar doce pelo preço do ingrediente é trabalhar de graça." | CF | "cobrar doce", palavras 2 e 3 | sim |
| `myth_busting` | Myth Busting | derruba uma crença repetida do nicho | "Responder rápido virou mito. Sua agenda vaza no horário que ninguém atende." | CE | "responder rápido", palavras 1 e 2 | sim |
| `bold_claim` | Bold Claim | crava uma promessa grande e específica | "Sua cozinha inteira projetada e orçada numa visita, sem compromisso." | MP | "cozinha inteira projetada", palavras 2 a 4 | sim |
| `reverse_psychology` | Reverse Psychology | desqualifica parte do público pra atrair o resto | "Não troca de contador quem gosta de descobrir imposto em abril." | CT | "troca de contador", palavras 2 a 4 | sim |

## curiosidade

Liberado em tráfego frio e em carrinho.

| id | tática | o que faz | exemplo | nicho | âncora | na spec |
|---|---|---|---|---|---|---|
| `curiosity` | Curiosity | abre um laço e adia o fechamento pro corpo da peça | "Tem uma etapa da receita que decide o preço final. Não é o ingrediente." | CF | "etapa da receita", palavras 2 a 4 | sim |
| `question` | Question | pergunta direta que a pessoa responde na cabeça | "Ó, quantos agendamentos sua clínica perdeu essa semana sem ninguém perceber?" **(cru)** | CE | "quantos agendamentos", palavras 2 e 3 | **não** |

## promocional

Liberado só em carrinho, lote ou prazo. Em frio, reprova.

| id | tática | o que faz | exemplo | nicho | âncora | na spec |
|---|---|---|---|---|---|---|
| `newness` | Newness | vende o fato de ser novo, formato ou coisa que não existia | "Saiu agora: projeto e orçamento no mesmo dia, na sua casa." | MP | "projeto e orçamento", palavras 3 a 5 | sim |
| `price_anchor` | Price Anchor | ancora num custo grande pra reposicionar o preço | "[prova do preset] por ano é o que essa empresa pagava de imposto a mais." | CT | "[prova do preset]", palavras 1 em diante | sim |
| `urgency` | Urgency | põe prazo ou limite explícito na decisão | "Ó, a turma de confeitaria fecha essa semana. Depois só na próxima." **(cru)** | CF | "turma de confeitaria", palavras 3 a 5 | sim |
| `fomo` | FOMO | mostra o grupo que já está dentro | "[prova do preset] clínicas já atendem sozinhas de madrugada. A sua não." | CE | "[prova do preset] clínicas", palavras 1 em diante | sim |
| `event_announcement` | Event Announcement | anuncia o evento como acontecimento com data | "Mutirão de projetos nesse fim de semana, com o projetista na loja." | MP | "mutirão de projetos", palavras 1 a 3 | sim |

## prova

Corpo da peça, orgânico de meio e remarketing declarado. Não abre frio.

| id | tática | o que faz | exemplo | nicho | âncora | na spec |
|---|---|---|---|---|---|---|
| `testimonial` | Testimonial | usa o caso de uma pessoa nomeada | "Olha, uma padaria trocou de regime e [prova do preset] no mesmo ano." **(cru)** | CT | "uma padaria trocou", palavras 2 a 4 | **não** |
| `social_proof` | Social Proof | usa o volume de gente que já fez | "[prova do preset] alunas já passaram por essa aula de confeitaria comigo." | CF | "[prova do preset] alunas", palavras 1 em diante | **não** |
| `statistic` | Statistic | abre com o número que resume o resultado | "[prova do preset] das mensagens da clínica chegam fora do horário de atendimento." | CE | "[prova do preset]", palavras 1 em diante | **não** |
| `authority` | Authority | ancora em quem faz a coisa por dentro | "Monto cozinha há [prova do preset], e o erro é sempre o mesmo." | MP | "monto cozinha", palavras 1 e 2 | **não** |

## demonstracao

Corpo da peça, orgânico de meio e remarketing declarado. Não abre frio. É aqui que mora o **hook demonstrativo**: quando existe tela ou cena pra mostrar, ela abre a peça e a prova vem antes da promessa.

| id | tática | o que faz | exemplo | nicho | âncora | na spec |
|---|---|---|---|---|---|---|
| `demonstration` | Demonstration | mostra a coisa funcionando já no primeiro frame | "Ó, esse relatório de uma página é o mês inteiro dessa empresa." **(cru)** | CT | "esse relatório", palavras 2 e 3 | **não** |
| `before_after` | Before and After | põe o estado antigo e o novo com número real | "Bolo afundando no meio era o normal. Hoje sai reto, sempre." | CF | "bolo afundando", palavras 1 e 2 | **não** |
| `comparison` | Comparison | compara o custo ou o esforço de dois caminhos | "Recepcionista, plantão e app de agenda pra fazer o que uma conversa faz." | CE | "recepcionista, plantão", palavras 1 e 2 | **não** |
| `unboxing` | Unboxing | abre do zero na frente de quem assiste | "Vou medir essa cozinha do zero e desenhar na tua frente." | MP | "medir essa cozinha", palavras 2 a 4 | **não** |

## educacional

Corpo da peça e orgânico. Não abre frio.

| id | tática | o que faz | exemplo | nicho | âncora | na spec |
|---|---|---|---|---|---|---|
| `reasons_why` | Reasons Why | promete os motivos por trás de um problema conhecido | "Empresa pequena paga imposto a mais por três motivos. O terceiro dói." | CT | "empresa pequena paga", palavras 1 a 3 | sim |
| `how_to` | How To | promete o passo a passo de uma coisa específica | "Como fazer a borda sair reta usando a espátula que você já tem." | CF | "borda sair reta", palavras 3 a 5 | **não** |
| `listicle` | Listicle | anuncia uma lista contável de entregas ou erros | "Olha, quatro coisas que a sua clínica perde toda vez que demora." **(cru)** | CE | "quatro coisas", palavras 2 e 3 | **não** |
| `problem_solution` | Problem Solution | nomeia a dor e promete a saída na mesma frase | "Canto morto na cozinha come metros que você pagou. Tem solução." | MP | "canto morto", palavras 1 e 2 | **não** |

## narrativa

Corpo da peça e orgânico. Não abre frio.

| id | tática | o que faz | exemplo | nicho | âncora | na spec |
|---|---|---|---|---|---|---|
| `storytelling` | Storytelling | conta o caso de alguém do começo ao resultado | "Um dono de padaria abriu o CNPJ errado e pagou por isso." | CT | "dono de padaria", palavras 2 a 4 | sim |
| `relatability` | Relatability | descreve a cena exata do dia da pessoa | "Cara, domingo à noite e você ainda montando bolo de encomenda." **(cru)** | CF | "domingo à noite", palavras 2 a 4 | **não** |

## direto

Remarketing e carrinho, quando a pessoa já sabe o que é. Não abre frio.

| id | tática | o que faz | exemplo | nicho | âncora | na spec |
|---|---|---|---|---|---|---|
| `call_to_action_first` | Call to Action First | pede a ação na primeira linha, com a promessa colada | "Ó, marca a avaliação e vê a agenda da clínica cheia." **(cru)** | CE | "marca a avaliação", palavras 2 a 4 | sim |

Observação sobre `direto`: é a única tática em que a promessa não cabe nas 4 primeiras palavras, porque o verbo de ação ocupa a abertura. Por isso ela não vale pra frio, onde a R2.6 é gate.

---

## Como montar o trio de um conceito

Regra 3-2-2: cada conceito sai em 3 hooks, 2 legendas e 2 formatos. O hook é o eixo que mais move resultado, então:

- Os 3 hooks têm ids DIFERENTES. Dois hooks do mesmo id colidem no nome da peça e viram a mesma variação com outra fala.
- Em frio, os 3 saem de `interrupcao_padrao` ou `curiosidade`.
- Ao menos 1 dos 3 é cru (R1.5): nota de voz, sem lettering de abertura.
- Ao menos 1 dos 3 é pergunta ou paradoxo.
- Cada fala passa pela conferência antes de virar áudio: contar palavras (máximo 14), achar a âncora nas 4 primeiras palavras, checar que não abre com marca e que não tem antítese paralela.

### Trio de exemplo: conceito "agenda que não vaza" (nicho CE, clínica de estética, tráfego frio)

| # | fala | tática | âncora | por que |
|---|---|---|---|---|
| A | "Sua clínica perde cliente justamente na hora que está mais cheia?" | `question` | "clínica perde cliente", palavras 2 a 4 | paradoxo: cheia deveria ser bom, e a frase diz que é ali que ela perde |
| B | "Cuidado: cada hora sem resposta é uma cliente marcando em outro lugar." | `warning` | "cada hora sem resposta", palavras 2 a 5 | ataca o custo que a dona já sente antes de citar qualquer solução |
| C | "Ó, quantos agendamentos sua clínica perdeu essa semana sem ninguém perceber?" **(cru)** | `question` | "quantos agendamentos", palavras 2 e 3 | mesma pergunta em nota de voz, pra testar o efeito do tratamento |

Conferência das três falas:

- Contagem: A tem 11 palavras, B tem 12, C tem 11. Todas dentro do teto de 14.
- Âncora: A nas palavras 2 a 4, B nas 2 a 5, C nas 2 e 3. A de B passa das 4 primeiras, então B é
  reescrita para "Cuidado: hora sem resposta é cliente marcando em outro lugar." (âncora nas
  palavras 2 a 4).
- Marca: nenhuma abre com o nome da clínica nem da oferta.
- Antítese paralela: nenhuma usa "não é X, é Y", "todo mundo X, ninguém Y" nem "enquanto uns X, outros Y".
- Apresentação: nenhuma tem saudação nem "eu sou o" (R2.6).
- Cru: C é a nota de voz, com "ó" e pausa de fala, e não leva lettering de abertura (R1.5).
- Ids distintos: A e C usam o mesmo id `question`, o que **colide**. A correção é trocar A por
  `contrarian` ("Responder rápido não vai encher a sua agenda. O buraco é outro.") e deixar o
  `question` só no hook cru.

Esse último item é o erro mais comum do trio, e ele só aparece quando você monta a tabela. Monte a
tabela sempre.
