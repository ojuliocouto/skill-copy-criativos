# Exemplo limpo: `agenda_cheia`

Este é o **exemplo limpo** da skill: um pacote fictício de nove blocos que passa no gate com
**zero reprovações e zero avisos**. É o que imitar quando você está aprendendo o formato.

O outro exemplo, `exemplos/cinco-entregas/`, reproduz uma peça **real** aprovada e por isso carrega
treze avisos assumidos. Os dois são úteis por motivos diferentes: aquele mostra o que acontece
quando a peça de campo não cabe na régua; este mostra a régua fechando.

Nada aqui é real. A oferta, a apresentadora, o caso citado e os números saem do preset fictício
`references/preset-oferta-exemplo.md`. Não reaproveite em peça de verdade.

**O conceito**: uma mentoria de quatro semanas para donos de clínica de estética que perdem
agendamento por demorar a responder no WhatsApp. Tráfego frio, captando lead para uma aula
gratuita. Ângulo **Custo oculto** (categoria Problema).

---

## 1. Este pacote está na terceira versão

Duas rodadas de correção o trouxeram até aqui, e as duas viraram regra da skill. Vale ler esta
seção antes da tabela de blocos, porque é aqui que mora a diferença entre copy que passa em
medição e copy que funciona.

### v1 para v2: o hook e a ponte, corrigidos pelo dono da metodologia

A versão 1 passava no gate com zero avisos e mesmo assim **foi reprovada**. O hook era uma
afirmação genérica e o CTA vinha colado no benefício, sem nada entre uma coisa e outra.

| | fala do bloco 1 |
|---|---|
| **v1** | "Cada cliente que espera resposta no WhatsApp já foi marcar em outra clínica." |
| **v2 e v3** | "Sua clínica perde cliente justamente na hora que está mais cheia? Pensa comigo." |

A v1 é uma afirmação correta e completamente previsível: quem tem clínica já sabe disso, concorda
com a cabeça e continua rolando o feed. A v2 é um **paradoxo**: clínica cheia deveria ser sinal de
saúde, e a frase diz que é exatamente ali que ela perde cliente. A pessoa precisa parar para fazer
a conta, e o corpo inteiro é a resposta.

O CTA da v1 vinha logo depois da prova, sem ponte. O veredito foi literal: **"zero copy"**. A v2
acrescentou a frase que liga a prova ao que o clique entrega, e **isso virou regra e gate**.

O hook aprovado na v2 **não mudou** na v3. O que mudou foi tudo o que vem depois dele.

### v2 para v3: o corpo, calibrado pelos anúncios já gravados

A v2 tinha um corpo de duas provas: um insert do atendente e o print da Dra. Renata. Passava, e era
magro. A calibração contra treze anúncios reais da casa (`references/calibracao-jheni.md`) mostrou
que o corpo que funciona na prática tem outra forma: **enumeração com um insert por item, respiro
de apresentadora entre os itens, mecanismo nomeado e ponte com molde**.

| | v2 | v3 |
|---|---|---|
| blocos | 6 | 9 |
| prova | 1 insert do atendente, 1 print | 3 inserts enumerados do atendente, 1 print |
| corpo | "Ele responde em segundos e já marca na agenda", tudo num bloco só | "Tá vendo esse atendente aqui?… E aqui ele confirma o horário… E no dia ele ainda manda lembrete." |
| identificação | não existia | bloco 4: "Isso é pra quem atende sem recepção. Não para por aí." |
| mecanismo | "Você na cadeira, ele no WhatsApp. Quanto mais cheia a clínica, mais agendamento entra." | "Isso só é possível quando o atendimento não para. Clínica cheia vira mais agendamento." |
| ponte | "É esse atendente que eu monto com você na aula." | "É exatamente isso que eu te ensino na aula." |
| fecho do CTA | "Sai de lá com o seu marcando." | "Bora montar o seu." |
| gate | zero reprovações, 1 aviso | **zero reprovações, zero avisos** |

Quatro moldes da casa entraram, e cada um tem endereço em `references/metodo-de-copy.md`:

1. **Pergunta demonstrativa abrindo a prova** ("Tá vendo esse atendente aqui?"). Nos anúncios reais
   a pergunta aparece muito mais no corpo do que na abertura, e aponta a tela antes da lista.
2. **Enumeração com um insert por item**, com as marcações faladas da casa ("E aqui ele…", "E no
   dia ele ainda…"), mais a frase de continuação "Não para por aí." no bloco de respiro.
3. **Mecanismo no molde "isso só é possível quando…"**, que nomeia a condição em vez de repetir o
   benefício.
4. **Ponte no molde dêitico mais ensino** ("é exatamente isso que eu te ensino na aula"), que é o
   molde mais usado nos anúncios gravados, junto com a pergunta de adesão.

O que **não** foi importado: escassez, lote, preço e data. Os treze anúncios da calibração são de
campanha de lote, esta peça é fria, e a régua de frio continua valendo por cima da calibração.

---

## 2. Onboarding

| # | item | situação |
|---|---|---|
| 1 | brief com avatar, promessa, modo, canal e campanha | completo: dono de clínica de estética, promessa de não perder agendamento, pago, reels, frio |
| 2 | conceito e ângulo | Custo oculto (categoria Problema), com a estrutura invisível declarada bloco a bloco no `conceito.md` |
| 3 | oferta e provas autorizadas | preset em `references/preset-oferta-exemplo.md`. Duas provas e nada além: mais de duzentas clínicas atendidas, e o caso da Dra. Renata |
| 4 | assets passados | dois arquivos no Drive. A gravação rende três recortes de momentos diferentes, um por item da enumeração. Nenhum asset novo precisou ser proposto, então nenhuma linha `criar:*` entrou em `assets.md` |
| 5 | onde a peça vai ser montada | nenhuma esteira instalada. O gate rodou com os limiares e o catálogo de táticas **embutidos**, sem `--gates` e sem `--taticas`, e isso fica declarado aqui |

---

## 3. A tabela de blocos

**A sequência de papéis vem primeiro**, e está declarada no `conceito.md`:

```
sequencia: H,D,P,I,P,P,M,P+T,C
```

É a sequência de enumeração do `references/metodo-de-copy.md` (`H D P I P P M P+T C`). Lida em
português: o paradoxo abre (`H`), a dor é nomeada (`D`), o primeiro item da prova aparece na tela
(`P`), a identificação serve de respiro e diz para quem isso é (`I`), o segundo e o terceiro itens
fecham a lista (`P`, `P`), a virada nomeia o mecanismo (`M`), o caso da Dra. Renata fecha a prova e
emenda a ponte (`P+T`), e o CTA pede a ação (`C`).

Só depois disso vem a tabela, que é o que o cliente aprova **antes** de o texto virar `roteiro.txt`.
Conversão usada: duração final = palavras / 2,9 / 1,45, ou seja **4,205 palavras por segundo
final**.

A coluna `papel` diz o que o bloco FAZ na argumentação; a coluna `forma` diz o que aparece na TELA.
São alfabetos diferentes e não se misturam.

| bloco | papel | fala | palavras | final | mínimo exigido | passa | insert | LEAD | KEY | forma |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | H | Sua clínica perde cliente justamente na hora que está mais cheia? Pensa comigo. | 13 | 3,09s | 2,80s (KEY em placa) | sim | nenhum | sua clínica | PERDE CLIENTE | placa_h2 |
| 2 | D | Cliente na cadeira, WhatsApp tocando. Quem espera vai marcar em outra clínica. | 12 | 2,85s | 2,80s (KEY em placa) | sim, no limite | nenhum | quem espera | OUTRA CLÍNICA | placa_h1 |
| 3 | P | Tá vendo esse atendente aqui? Ele responde em segundos e você nem larga a cadeira. | 15 | 3,57s | 3,50s (insert; a placa pedia 3,05s) | sim | atendente respondendo no whatsapp da clínica | tá vendo | RESPONDE EM SEGUNDOS | placa_h2 |
| 4 | I | Isso é pra quem atende sem recepção. Não para por aí. | 11 | 2,62s | teto de 6,00s (apresentadora sozinha) | sim | nenhum | nenhum | nenhum | nenhuma |
| 5 | P | E aqui ele confirma o horário direto na agenda. E o cliente já sai marcado. | 15 | 3,57s | 3,50s (insert; a placa pedia 3,05s) | sim | atendente confirmando o horário na agenda | e aqui ele | CONFIRMA O HORÁRIO | placa_h4 |
| 6 | P | E no dia ele ainda manda lembrete. Ninguém esquece e a cadeira não fica vazia. | 15 | 3,57s | 3,50s (insert; a placa pedia 2,80s) | sim | atendente mandando o lembrete no whatsapp | e no dia | MANDA LEMBRETE | placa_h1 |
| 7 | M | Isso só é possível quando o atendimento não para. Clínica cheia vira mais agendamento. | 14 | 3,33s | teto de 6,00s (apresentadora sozinha) | sim | nenhum | nenhum | nenhum | nenhuma |
| 8 | P+T | Dra. Renata dobrou a agenda num mês. É exatamente isso que eu te ensino na aula. | 16 | 3,80s | 3,75s (KEY em coluna, 3 palavras de tempo) | sim | print da agenda cheia da dra renata | Dra. Renata | DOBROU A AGENDA | coluna |
| 9 | C | Toca em saiba mais e entra na aula do Agenda Cheia. Bora montar o seu. | 15 | 3,57s | 3,05s (KEY em seta_cta) e 3,00s (CTA) | sim | nenhum | toca em saiba mais | ENTRA NA AULA | seta_cta |

**Total: 126 palavras, 29,96s finais.** A faixa de pago frio é 15 a 30s, então a peça cabe, e cabe
apertado no teto: qualquer palavra a mais no roteiro vira aviso de duração.

Repare na contagem do KEY, que são duas contas diferentes. `RESPONDE EM SEGUNDOS` vale **2** para
o limite de palavras de conteúdo ("em" é funcional e não conta) e **3** para o tempo de leitura,
onde toda palavra conta. `DOBROU A AGENDA` segue a mesma lógica, e por isso o mínimo do bloco 8 é
3,75s (3,5s da coluna mais 0,25s da terceira palavra) e não 3,5s. O bloco tem 3,80s: **cinquenta e
cinco milésimos de folga**, e é por isso que ele tem 16 palavras e não 15.

**A ponte fica no fim do bloco 8**, dentro do mesmo bloco da prova. Ela não vira bloco próprio: se
virasse, seria mais um bloco de apresentadora sozinha entre a prova e o CTA, e a peça perderia o
encadeamento que faz a ponte funcionar.

---

## 4. As contas que fecharam a peça

Estas são as contas que mudam a **forma** da peça, não só a redação. É por isso que a skill manda
rodar `scripts/planejar_blocos.py` no passo 0, antes de escrever qualquer fala: elas dependem da
linha do tempo acumulada e não dá para acertar no papel.

Comando rodado antes da copy:

```bash
python3 scripts/planejar_blocos.py --modo pago --campanha frio \
  --blocos "L,L,I,A,I,I,A,I,C" --palavras "13,12,15,11,15,15,14,16,15"
```

### Por que a enumeração precisa do bloco 4

Três inserts seguidos estouram a densidade. Com os blocos 3, 5 e 6 colados, a janela do corpo (3 a
15s) fica em 77% de cobertura de insert, contra a faixa de 45 a 55%. **O bloco 4 existe por duas
razões ao mesmo tempo**: ele derruba a densidade para 54% e é onde cabe a identificação e a frase
de continuação que faz a lista soar falada. Nos anúncios reais da casa esse respiro está lá,
marcado como um "de frente" entre um item e o outro.

### Densidade de insert por janela

O gate mede quanto tempo de cada janela está coberto por insert e cobra **45 a 55%** em cada uma.
São duas janelas: **corpo**, de 3 a 15s, e **fecho**, de 15s até o fim.

- **Corpo (3 a 15s)**: 54%, dentro da faixa.
- **Fecho (15s ao fim)**: 54%, dentro da faixa.

A v2 fechava em 58% no fecho e assumia o aviso. A v3 fecha nas duas janelas porque a prova, em vez
de morar num bloco longo só, virou três blocos curtos com respiro entre eles.

### Teto de dois blocos vizinhos sem insert

Blocos vizinhos sem insert, somados, não passam de **6,0s** finais. Os blocos 1 e 2 somam
**5,94s**. É por isso que o bloco 2 tem **12 palavras e não 13**: a décima terceira palavra levaria
a soma para 6,18s e viraria aviso. Os outros dois blocos sem insert (4 e 7) não são vizinhos entre
si, porque a enumeração os separa.

### Retenção dos dois primeiros inserts

O primeiro insert precisa começar entre 5 e 10s: o bloco 3 começa em **5,94s**. O segundo precisa
começar entre 12 e 20s: o bloco 5 começa em **12,13s**. As duas janelas são apertadas de propósito,
e é a soma dos blocos 1, 2 e 4 que decide se elas fecham.

---

## 5. Prova: o que entrou e o que ficou de fora

Autorizado no preset: **mais de duzentas clínicas atendidas** e o **caso da Dra. Renata**, que
dobrou os agendamentos em um mês.

- **Entrou**: o caso da Dra. Renata, no bloco 8, com as palavras do preset e nada além. A
  enumeração dos blocos 3, 5 e 6 é **prova de funcionamento**, não prova de resultado: ela mostra
  o que a tela faz, sem prometer número nenhum.
- **Ficou de fora**: as mais de duzentas clínicas. Não coube na faixa de duração. Fica registrada
  como variação futura do bloco 8, não como prova que não existe.
- Nenhum outro número, nome, preço, data ou promessa entrou na peça.

Registrar o que ficou de fora é parte da entrega. A próxima variação do conceito costuma nascer
exatamente daí.

---

## 6. O gate

Comando, sem `--gates` e sem `--taticas`, porque não há esteira instalada:

```bash
cd ~/.claude/skills/copy-criativos
python3 scripts/gate_copy.py exemplos/agenda-cheia
```

Saída:

```
RESUMO POR BLOCO:
  bloco 1: 13 palavras, 4.48s natural, 3.09s final, insert=False, key=PERDE CLIENTE
  bloco 2: 12 palavras, 4.14s natural, 2.85s final, insert=False, key=OUTRA CLÍNICA
  bloco 3: 15 palavras, 5.17s natural, 3.57s final, insert=True, key=RESPONDE EM SEGUNDOS
  bloco 4: 11 palavras, 3.79s natural, 2.62s final, insert=False, key=
  bloco 5: 15 palavras, 5.17s natural, 3.57s final, insert=True, key=CONFIRMA O HORÁRIO
  bloco 6: 15 palavras, 5.17s natural, 3.57s final, insert=True, key=MANDA LEMBRETE
  bloco 7: 14 palavras, 4.83s natural, 3.33s final, insert=False, key=
  bloco 8: 16 palavras, 5.52s natural, 3.80s final, insert=True, key=DOBROU A AGENDA
  bloco 9: 15 palavras, 5.17s natural, 3.57s final, insert=False, key=ENTRA NA AULA
Pacote aprovado, sem reprovações nem avisos.
```

**Zero reprovações e zero avisos.** Dois avisos apareceram na primeira rodada, nos blocos 5 e 6,
porque as duas falas tinham 15 palavras numa frase só. As duas viraram duas frases curtas, sem
mudar a contagem total nem a duração do bloco. Fica o registro: aviso de frase longa quase sempre
se resolve com um ponto final no lugar de uma vírgula.

---

## 7. Auditoria antes de entregar

- [x] cada bloco diz o que a tela mostra: os quatro blocos com insert citam a resposta, a
  confirmação do horário, o lembrete e a agenda cheia, que é exatamente o que os arquivos do Drive
  mostram
- [x] nenhum take se repete entre blocos: os assets 1, 2 e 3 são trechos com timecode diferente da
  mesma gravação, e isso está declarado em `assets.md`
- [x] toda palavra de KEY, LEAD e garrafal está na fala do bloco certo
- [x] um dos três hooks é pergunta ou paradoxo (o Hook A é pergunta, o Hook C é o mesmo paradoxo em
  afirmação), e existe pergunta no corpo (bloco 3)
- [x] o hook nomeia o problema nas 4 primeiras palavras e não abre com marca
- [x] existe ponte antes do CTA, ligada à prova do bloco anterior, e o molde dela está declarado em
  `cta.md`
- [x] CTA bate com modo pago e campanha frio: verbo de ação, sem escassez, sem preço, sem data
- [x] nenhuma prova fora do preset, e a enumeração é prova de funcionamento, não de resultado
- [x] zero travessão, acentuação completa, voz falada BR, sem antítese paralela
- [x] o gate rodou e o output está aqui e na entrega

---

## 8. Detalhes que valem copiar

- **A prova é uma lista de três, não um parágrafo.** "Responde em segundos", "confirma o horário",
  "manda lembrete". Três verbos, três blocos, três inserts. É o padrão que mais aparece nos
  anúncios reais da casa e o que a `references/calibracao-jheni.md` mediu.
- **O bloco de respiro carrega trabalho.** O bloco 4 não é pausa: ele diz para quem a peça é
  ("isso é pra quem atende sem recepção") e anuncia que a lista continua ("não para por aí"),
  enquanto segura a densidade de insert dentro da faixa.
- **O mecanismo nomeia a condição, não o benefício.** "Isso só é possível quando o atendimento não
  para" diz por que funciona. Repetir "você ganha mais agendamento" seria repetir a promessa.
- **A ponte aponta.** "É exatamente isso que" se refere ao que acabou de aparecer na tela. Ponte
  que não aponta nada ("e tem muito mais te esperando") não é ponte.
- **Os três hooks têm o mesmo ângulo e táticas diferentes.** `question`, `contrarian` e
  `shocking_statement`: o recorte "custo oculto" é o mesmo nos três, o mecanismo de parada é outro.
  É assim que a matriz 3x2x2 testa hook sem trocar de conceito.
- **O Hook A e o Hook C carregam o mesmo paradoxo em formas opostas.** O A pergunta, o C afirma.
  Testar pergunta contra afirmação com o mesmo conteúdo isola a variável.
- **O hook C é o cru.** Nota de voz, com "Ó" e pausa, `lettering: nenhum`, sem apresentadora em
  tela.
- **A garrafal G1 é CHEIA**, a palavra do paradoxo, e não repete o KEY do bloco (`PERDE CLIENTE`).
  A G2 é AGENDAMENTO, no bloco 7, que é o bloco de apresentadora sozinha depois da enumeração. Fora
  do bloco 1, a garrafal só entra em bloco de apresentador sozinho.
- **As duas garrafais fecham a virada.** "Cheia" abre a peça sendo o problema; "agendamento" fecha
  o corpo sendo o resultado da mesma palavra. A mesma condição, invertida de sinal.
- **O asset 4 é imagem parada** e a ressalva de `assets.md` diz isso, junto com o que quem monta
  precisa fazer (deslize lento no próprio print, sem desfoque, véu ou recorte novo).
- **O CTA diz o KEY inteiro.** A fala é "toca em saiba mais e entra na aula", e o KEY é
  `ENTRA NA AULA`. Lettering que a voz não diz vira segunda mensagem.
