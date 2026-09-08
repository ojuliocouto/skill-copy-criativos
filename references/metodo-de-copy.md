# Método de copy: o que dizer, em que ordem, e por quê

`regras-da-tela.md` diz o que a tela **aguenta**. Este arquivo diz o que a copy **faz**. São coisas
diferentes, e uma peça que respeita a tela e ignora o método passa no gate e não vende nada.

Leia este arquivo antes de escrever a primeira linha, e depois use `regras-da-tela.md` para caber.
Nunca o contrário: quem começa pela medida escreve peça que cabe e não convence.

O método vem de três lugares que se encaixam: a metodologia de criativos em três camadas, a
anatomia de anúncio validada em campanha real, e os frameworks clássicos de copy direta (Schwartz,
Hormozi, Brunson, Kennedy, Halbert, Ogilvy) aplicados a vídeo curto.

---

## 1. As três camadas

**A copy nasce do ângulo e da estrutura, e só depois veste o formato. Nunca comece pelo formato.**

| camada | pergunta que ela responde | onde ela aparece no pacote |
|---|---|---|
| **Ângulo** | o QUE dizer: por onde a peça entra no problema | campo `angulo` do `conceito.md`; a lista completa está em `references/angulos-e-estrutura.md` |
| **Estrutura invisível** | em que ORDEM dizer: quais dos 8 elementos de persuasão entram, e onde | campo `estrutura_invisivel` do `conceito.md`, escrito bloco a bloco; a sequência de papéis (seção 3 aqui) é a forma operacional dela |
| **Formato** | COMO mostrar: talking head com inserts, sem avatar, notícia, alerta, mesa de podcast | campo `formatos` do `matriz.md`, e a direção de cada bloco no `roteiro.txt` |

Três regras que não se negociam:

1. **Um conceito mira UM avatar com UMA dor ou promessa macro.** Se a peça fala para dois públicos,
   ela não fala para nenhum.
2. **Dois anúncios do mesmo conceito nunca repetem ângulo.** Três variações da mesma frase contam
   como um.
3. **O gancho SEMPRE combina 2 elementos**, nunca um só. Curiosidade + promessa. Credibilidade +
   quebra de objeção. Dor + número. Um gancho de um elemento só é uma frase, não é um gancho.

O talking head com inserts é **um formato entre muitos**, não o padrão obrigatório. Varie o formato
dentro da leva.

---

## 2. Diagnóstico do avatar: temperatura e nível de consciência

Antes de escrever, decida duas coisas sobre quem vai ver a peça. Elas governam quase todo o resto.

### Temperatura

| | **FRIO** | **QUENTE** |
|---|---|---|
| quem é | nunca ouviu falar de você nem do produto | já viu um anúncio, consumiu conteúdo, visitou a página |
| objetivo da peça | criar consciência e despertar desejo | remover objeção e gerar decisão |
| tom | educativo, revelador, contra-intuitivo | direto, urgente, pessoal |
| hook ideal | espelho de dor, desbanca mito, curiosidade, paradoxo | prova social, urgência, pergunta direta |
| CTA | suave, sem escassez, sem preço, sem data | forte, com escassez legítima |
| duração | mais longo: precisa construir contexto | mais curto: o contexto já existe |

No pacote, a temperatura é o campo `campanha` do `conceito.md`: `frio`, `captacao` e
`perpetuo_frio` são frio; `carrinho`, `lote` e `remarketing` são quente.

### Nível de consciência (Schwartz)

| nível | o que a pessoa sabe | temperatura | o que a copy faz | hook ideal |
|---|---|---|---|---|
| **1. Inconsciente** | nem sabe que tem o problema | frio extremo | cria o problema antes de oferecer a saída, com cena ou dado de mercado | storytelling, contra-intuitivo, notícia ou tendência |
| **2. Consciente do problema** | sente a dor, não conhece o caminho | frio e morno | nomeia a dor melhor do que a pessoa consegue nomear | espelho de dor (lista de sintomas), dor direta, **paradoxo** |
| **3. Consciente da solução** | já pesquisou, está comparando | morno e quente | posiciona o **mecanismo único**: por que esta solução funciona quando as outras não | contraste de valor, desbanca mito |
| **4. Consciente do produto** | conhece você, não comprou | quente | quebra a última objeção com prova específica | prova social com número, pergunta direta, urgência |
| **5. Mais consciente** | já decidiu, falta o empurrão | quente máximo (remarketing) | oferta direta, sem rodeio | urgência, âncora de preço |

**Usar o hook errado para o nível é o erro mais caro da peça.** Falar de oferta com quem nem sabe
que tem o problema é gastar mídia; falar do problema com quem já decidiu é atrasar a venda.

### O que o diagnóstico decide

| decisão | frio | quente |
|---|---|---|
| **cluster do hook** | `interrupcao_padrao`, `curiosidade` | os dois acima mais `promocional` |
| **proporção gancho / corpo / oferta** (Brunson) | 20 / 60 / 20: a história constrói a crença antes da oferta | 20 / 20 / 60: vai direto para a oferta |
| **promessa** (equação de valor, Hormozi) | maximize o **resultado** e minimize o **prazo**: promessa grande o bastante para parar o dedo | maximize a **probabilidade percebida** e minimize o **esforço**: a pessoa já quer, precisa acreditar que funciona para ela |
| **do que a mensagem fala** (Kennedy) | do PROBLEMA ou da OPORTUNIDADE, nunca do produto | pode falar do produto e da oferta diretamente |
| **CTA** | verbo de ação, sem escassez, sem preço, sem data | verbo de ação com escassez legítima |
| **mecanismo único** | apresentado como revelação ou descoberta | reforçado como diferencial já comprovado |

**Especificidade vence sempre**, nas duas temperaturas. "Ganhar muito dinheiro" perde para um valor
com dono e prazo; "em pouco tempo" perde para um número de dias; "vários clientes tiveram
resultado" perde para um caso nomeado com número e contexto. Tudo isso sai do preset de oferta
(`references/modelo-preset-oferta.md`), e o que não está lá não existe.

---

## 3. A anatomia do anúncio, em papéis de bloco

Cada bloco do roteiro tem **um papel**: uma coisa que ele faz na argumentação. O papel é diferente
da forma do bloco.

> **Dois alfabetos, não confunda.** O **papel** (aqui: `H`, `D`, `P`, `M`, `I`, `O`, `T`, `C`) diz o
> que o bloco FAZ na argumentação. A **forma** que o planejador `scripts/planejar_blocos.py` usa
> (`I` insert, `L` lettering em placa, `LC` coluna ou carimbo, `A` apresentador sozinho, `P` ponte,
> `C` CTA) diz o que aparece na TELA. A tabela de blocos carrega as duas colunas: `papel` e `forma`.

**Tabela de conversão papel -> forma** (a mesma `MAPA_PAPEL_PARA_FORMA` de
`scripts/gate_copy/planejador.py`, usada por `derivar_forma_de_papeis` e pelo `--papeis` de
`scripts/planejar_blocos.py`): passe a sequência de papéis pro planejador e ele deriva a forma
sozinho, sem precisar converter na mão.

| papel | forma |
|---|---|
| `H` (hook) | `L` (lettering em placa) |
| `D` (dor ou diagnóstico) | `L` |
| `P` (prova) | `I` (insert) |
| `I` (identificação) | `A` (apresentador sozinho) |
| `M` (mecanismo ou virada) | `A` |
| `O` (oferta) | `L` |
| `T` (ponte) | `P` (ponte, apresentador sozinho ligando o corpo ao CTA) |
| `C` (CTA) | `C` |

Numa combinação (`X+T`, `O+T`), a forma do bloco é a do papel BASE (a parte antes do `+`): a ponte
entra na última frase do bloco, sem trocar o que aparece na tela.

### `H`: hook

**O que faz**: para o dedo em três segundos e abre uma conta que a pessoa precisa fechar.

Duas famílias funcionam, e a escolha depende de ter ou não uma tela para mostrar:

- **Demonstrativo**: abre JÁ mostrando a coisa funcionando. Quando existe demo, **a prova vem antes
  da promessa**, e a tela abre a peça.
- **Afirmação forte, pergunta ou paradoxo**: quando não há tela, ou quando o argumento é de crença.

**Regra do dono da metodologia: ao menos um dos três hooks do conceito é pergunta ou paradoxo.**
Afirmação correta e previsível não segura ninguém: a pessoa concorda com a cabeça e continua
rolando. O paradoxo junta duas coisas que não deveriam andar juntas e obriga a parar para fazer a
conta. O corpo da peça inteiro é a resposta dessa conta. Detalhe e exemplos em
`references/taticas-de-hook.md`.

**Direção visual típica**: apresentador de frente com lettering e garrafal, ou insert de tela real
já no primeiro frame. Nunca rosto parado sem elemento gráfico.

**Exemplos**: serviço (clínica): *"Sua clínica perde cliente justamente na hora que está mais
cheia? Pensa comigo."* Produto físico (móveis planejados): *"Quanto mais caro o planejado, mais
espaço sobrando na sua cozinha? Repara comigo."*

#### Os seis moldes de abertura

Os moldes abaixo valem para qualquer produto ou serviço. O molde é reaproveitável; a frase não. As
frases literais de um produto real estão no estudo de caso
(`references/calibracao-jheni.md`, seção 2.1), e servem para ver o molde em ação, nunca para
copiar.

| molde | forma | quando usar |
|---|---|---|
| **pergunta de custo** | "Quantas [vendas] a sua empresa perdeu [esse mês] por causa de [causa]?" | o público sente a perda e nunca contou o tamanho dela |
| **pergunta paradoxal** | junta duas coisas que não deveriam andar juntas | nível 2, quando o argumento é de crença e não há tela |
| **demonstrativo** | "Isso que você tá vendo na tela é [o quê]" | existe tela real, e a prova pode abrir a peça |
| **afirmação forte** | número, curiosidade ou contrariedade na primeira frase | há um dado grande com dono, ou uma crença cara para derrubar |
| **custo/confronto** | escada de números ou aviso de risco | o público está perdendo dinheiro agora e não sabe |
| **notícia ou descoberta** | "Agora eu entendi por que [gente como você] parou de [X]" | a conclusão é curiosa e a causa é o corpo inteiro |

Um exemplo de cada molde, alternando serviço e produto físico:

- **pergunta de custo** (serviço, contabilidade): "Quanto imposto sua empresa pagou a mais no ano
  passado sem ninguém conferir?"
- **demonstrativo** (produto físico, móveis planejados): "Tá vendo esse canto morto? Adivinha
  quanto ele vira de armário. Tudo."
- **afirmação forte** (serviço, clínica): "A maior parte das mensagens da sua clínica chega fora do
  horário de atendimento."
- **custo/confronto** (produto físico, móveis planejados): "Vou dizer uma coisa impopular:
  planejado caro nem sempre é planejado bom."
- **notícia ou descoberta** (serviço, contabilidade): "Agora eu entendi por que tanta empresa
  pequena paga imposto a mais e nunca descobre."
- **filtro condicional** (variante de afirmação forte que já carrega a identificação; produto
  físico): "Se você vai reformar a cozinha esse ano, presta atenção aqui."

Um catálogo maior, com os quatro nichos de exemplo lado a lado, está em
`references/modelo-mestre.md`, parte 1.

**A regra do dono da metodologia continua valendo por cima da tabela**: dos três hooks do
conceito, um é pergunta ou paradoxo, mesmo quando os moldes de afirmação parecem mais naturais
para a oferta.

**Erro comum**: hook institucional ou morno ("Você conhece o X?"), saudação, apresentação, marca nas
primeiras palavras, e promessa antes da prova quando existe demo disponível.

### `D`: dor ou diagnóstico

**O que faz**: nomeia o problema com precisão maior do que a pessoa usaria sozinha. É aqui que ela
pensa "esse cara tá falando de mim".

Duas formas: **espelho de dor** (a cena exata do dia dela) e **diagnóstico** (a causa por trás do
sintoma, o mecanismo do problema). O diagnóstico é mais forte quando o público já tentou resolver e
falhou.

**Direção visual típica**: apresentador sozinho com garrafal, ou lettering de placa com a palavra da
dor.

**Exemplos**: serviço (clínica): *"Cliente na cadeira, WhatsApp tocando. Quem espera vai marcar
em outra clínica."* Produto físico (móveis planejados): *"Armário novo, e a panela grande continua
no chão. O projeto não perguntou o que você guarda."*

**Erro comum**: descrever o sintoma que todo concorrente já descreve, sem chegar na causa. E
adjetivo no lugar de cena: "é frustrante" não é dor, "sexta à noite e você ainda fazendo isso" é.

### `P`: prova (insert)

**O que faz**: mostra, não afirma. É o bloco que carrega o insert e o coração da peça.

Duas espécies: **prova de funcionamento** (a tela real da coisa rodando) e **prova social** (caso
nomeado com número e contexto, ou volume de gente).

O padrão que mais funciona é a **enumeração**: 3 a 5 itens, um por bloco, **cada item com o próprio
insert**, com ritmo de lista falada. Nunca reuse o mesmo take em dois blocos do mesmo anúncio.

**Como prova e enumeração se juntam**: o papel `P` **repete**, um bloco por item, e cada bloco
carrega um insert diferente. Quatro marcações fazem a lista soar falada em vez de lida:

1. **Reticências no fim do item**, que escrevem a pausa dentro do texto: "A parede morta… virou
   despensa."
2. **Ordinal como pilar**, quando os itens são riscos ou passos: "Primeiro. / Segundo. /
   Terceiro."
3. **Ancoragem espacial**, quando cada item tem tela ou cena própria: "Aqui eu tenho: / Tem
   também / E por último".
4. **Frase de continuação entre itens**, curtíssima e sem conteúdo novo: "E não para por aí.", "E
   mais:", "E de quebra…", "E o melhor:".

As quatro marcações foram observadas num produto real e estão com as frases literais no estudo de
caso (`references/calibracao-jheni.md`, seção 2.2).

Dois cuidados de medida, porque enumeração longa quebra a peça: cada bloco com insert pede o
mínimo de duração do insert, e a **densidade de insert por janela** tem faixa. Enumeração de 3
itens quase sempre precisa de um bloco de apresentador **entre** os itens para a densidade caber,
e é isso que os anúncios do estudo de caso fazem. Rode
`scripts/planejar_blocos.py` antes de escrever, não depois.

**Fórmula de prova social**: *pessoa em situação difícil + o que ela fez + resultado com número e
prazo*. Nome, número e contexto juntos, ou não é prova. E cada peça de prova sai do preset de
oferta: prova de passagem ("já passaram pelo treinamento") nunca vira prova de resultado ("já
conseguiram X").

**Direção visual típica**: insert com enquadramento declarado, um por bloco, com o KEY no painel.

**Exemplos**: serviço (clínica): *"A Dra. Renata ligou o dela e dobrou os agendamentos em um
mês, sem contratar ninguém."* Produto físico (móveis planejados): *"Esse é o mesmo canto, quatro
semanas depois. Cabe a despensa inteira."*

**Erro comum**: número sem dono, prova inventada, "vários clientes" no lugar de um caso, e um insert
genérico servindo dois blocos.

### `M`: mecanismo ou virada

**O que faz**: explica **por que isso funciona quando o resto não funciona**. Não é o produto, é o
mecanismo por trás do resultado. É o bloco que transforma a lista em argumento.

Aqui mora também o **quebra-complexidade**: depois de mostrar a coisa funcionando, a peça precisa
dizer que é mais simples do que pareceu, senão a prova vira intimidação.

Em frio, apresente o mecanismo como revelação. Em quente, reforce como diferencial já comprovado.

**Direção visual típica**: apresentador sozinho (é onde a garrafal vive), ou insert apontando o
elemento que faz a diferença.

**Exemplos**: serviço (clínica): *"Você na cadeira, ele no WhatsApp. Quanto mais cheia a
clínica, mais agendamento entra."* Produto físico (móveis planejados): *"O projeto sai antes da
compra da chapa. É por isso que sobra ambiente, e não material."*

#### Os três moldes de mecanismo

1. **O responsável nomeado.** Aponta a peça exata que faz funcionar, com nome próprio.
   Serviço (clínica): "O responsável por isso é uma ligação simples entre o WhatsApp e a agenda."
   Produto físico (móveis planejados): "O que resolve é o projeto sair antes da compra da chapa, e
   não depois." Forma curta e reaproveitável: **"isso só é possível quando [condição]"**.
2. **Negar o gênio.** É o quebra-complexidade, e ele tem forma fixa: quem apresenta nega ser
   especial antes de dizer que a pessoa consegue. Serviço (contabilidade): "E não é truque de
   contador. Qualquer empresa consegue, se alguém olhar o regime a tempo." Infoproduto
   (confeitaria): "E não é talento. Eu não nasci confeiteira. Eu só aprendi a temperatura certa."
3. **A escala.** Depois da última prova, encolhe o que mostrou para abrir o tamanho do resto:
   "E essa foi só a cozinha. O mesmo projeto resolveu o quarto e a área de serviço." Vem sempre no
   mesmo lugar: última frase do `M`, logo antes da ponte.

E uma regra de vocabulário que mora aqui: **jargão traduzido na mesma frase**. "Regime tributário,
que é a regra que decide quanto a sua empresa paga de imposto." Sem a tradução colada, corte a
palavra.

**Erro comum**: pular o mecanismo e ir da prova direto para a oferta. Sem mecanismo, a promessa vira
pedido de fé, e a pessoa atribui o resultado à sorte de quem apareceu na prova.

### `I`: identificação

**O que faz**: nomeia **para quem isso é**, ou aperta a dor de novo agora que a solução já apareceu.
Serve de filtro (quem não é sai) e de espelho (quem é se reconhece e fica).

Frequentemente vem como contraste de dois mundos: quem está fazendo e quem não está.

**Direção visual típica**: apresentador sozinho, ou lettering com o nome do público.

**Exemplos**: serviço (clínica): *"Isso é pra quem atende com a agenda na mão e perde horário
sem perceber."* Produto físico (móveis planejados): *"Isso é pra quem vai reformar uma vez e não
quer descobrir o erro depois de instalado."*

#### Dois moldes válidos, e um proibido

- **Cena** (o molde do exemplo acima): descreve o dia da pessoa e ela se reconhece.
- **Condicional mais prescrição**, que é o molde mais reaproveitável: *"Se você [é ou tem X] e
  quer [Y]… você precisa [Z]."* Serviço (contabilidade): "Se você tira dinheiro da empresa sem
  saber se pode, você precisa de um fechamento mensal, não de um contador de dezembro." Produto
  físico (móveis planejados): "Se você já mediu a parede três vezes e continua na dúvida, o
  problema não é a trena." Duas leituras: esse molde costuma **carregar o hook junto** (vira o
  bloco `H+I`), e ele aguenta ser repetido e escalado ao longo da peça inteira, uma condição por
  bloco.

**Erro comum**: listar público como se fosse segmentação de mídia ("empresários, autônomos e
profissionais liberais"). A categoria sozinha não identifica ninguém: ou ela vem presa a uma
condição e a uma prescrição, ou vem como cena.

### `O`: oferta

**O que faz**: entre a prova (ou a ponte) e o CTA, diz **o que é a oferta, o que será feito, o que
a pessoa ganha e como ela acessa**. É regra do dono da metodologia, depois de reprovar um ad que ia
da prova mais ponte direto pro CTA: "aqui você encaixa já trazendo o que é a aula, o que será
feito, o que a pessoa ganha e o que ela precisa fazer pra ter acesso". **Sem esse bloco, o gate
reprova** (`checar_oferta`, `scripts/gate_copy/regras/cta.py`).

Os quatro itens obrigatórios, na mesma frase ou em frases vizinhas do mesmo bloco:

1. **O que é.** Nomeia a oferta pelo nome (o produto ou a aula, campo `oferta` do `conceito.md`,
   ou uma das `marcas`).
2. **O que será feito.** O verbo da entrega: "a gente monta", "eu te mostro", "você constrói".
3. **O que a pessoa ganha.** O resultado concreto que ela leva, ligado ao que a prova já mostrou.
4. **Como acessa.** Gratuita, ingresso, inscrição: a palavra que diz o caminho até a oferta (pode
   morar no próprio CTA seguinte, quando o verbo de ação já cobre isso).

Data, preço, edição e lote numerado **só existem em campanha de carrinho ou lote**. Em frio, a
oferta é o que a pessoa aprende ou recebe, sem número comercial nenhum.

**Direção visual típica**: apresentador com lettering, logo do produto ou evento declarado.

**Exemplo, frio, aula gratuita**: *"Na aula gratuita do Agenda Cheia a gente monta o seu, passo a
passo. Você sai com ele respondendo."* (o quê: aula gratuita do Agenda Cheia; o que será feito: a
gente monta; o que ganha: o atendente respondendo; como acessa: gratuita, mais o "toca em saiba
mais" do CTA seguinte)

**Exemplo, quente, produto físico com orçamento**: *"É a visita técnica do Móveis Sob Medida. O
projetista mede na sua frente e você sai com o orçamento na mão, sem compromisso."* (o quê: a
visita técnica; o que será feito: o projetista mede e desenha; o que ganha: o orçamento na mão;
como acessa: o "toca aqui e escolhe o dia" do CTA seguinte)

Os cinco tipos de acesso (aula gratuita, consulta ou avaliação, orçamento, compra direta com preço,
teste grátis) e o que cada um pode dizer estão em `references/modelo-mestre.md`, seção "Oferta por
tipo de acesso".

**Marcadores que o gate procura** (`MARCADORES_DE_OFERTA`, `scripts/gate_copy/limiares.py`): "você
sai com", "a gente monta", "eu te mostro", "você aprende", "passo a passo", "na prática", "do
zero", "com você", "imersão", "aula gratuita", "mentoria", "treinamento", entre outros. E de acesso
(`MARCADORES_DE_ACESSO_DA_OFERTA`): "gratuita", "gratuito", "de graça", "toca em", "clica", "link",
"inscreve", "entra".

**Erro comum**: oferta em frio com preço e prazo, bullets genéricos que qualquer concorrente também
entrega, e nomear a oferta sem dizer a entrega (ou o contrário: entrega sem nomear a oferta). As
duas coisas juntas é que fazem o bloco valer.

### `T`: ponte (transição para o CTA)

**O que faz**: **diz o que o clique entrega**, ligado à prova ou ao benefício que acabou de aparecer
na tela. É o bloco (ou a frase) que dá objeto ao clique.

**Regra do dono da metodologia, e reprovação no gate: benefício e depois "toca em saiba mais" do
nada não passa.** Sem ponte, a peça mostra a prova e no bloco seguinte manda clicar, e quem assiste
não sabe o que ganha com isso. O veredito literal foi "zero copy".

A ponte pode ser um bloco próprio ou a **última frase** do bloco anterior ao CTA. Marcadores que
funcionam: "é isso que", "é esse ... que eu monto com você", "eu te mostro", "na aula", "no
treinamento", "na mentoria", "no evento", "dentro do".

#### Os moldes de ponte

Sete moldes, e dois deles resolvem a maioria das peças. O nome da oferta aparece como `<oferta>`
porque o molde é reaproveitável e a oferta não. As frases literais de um produto real estão no
estudo de caso (`references/calibracao-jheni.md`, seção 2.5), onde treze anúncios têm ponte e oito
usam só estes dois primeiros moldes.

**Molde 1, dêitico mais ensino ou acesso.** A frase aponta com "isso", "essa" ou "esse" o que
acabou de aparecer na tela, e emenda onde a pessoa recebe aquilo.

- "E é exatamente isso que eu monto com você na `<oferta>`." (serviço, clínica)
- "É esse projeto que a gente desenha com você na `<oferta>`." (produto físico, móveis planejados)
- "É exatamente esse fechamento que a gente faz na `<oferta>`." (serviço, contabilidade)
- "É esse acabamento que eu te ensino na `<oferta>`." (infoproduto, confeitaria)

**Molde 2, pergunta de adesão com "Então".** A ponte vira pergunta, e o "Então" é a dobradiça que
abre o CTA. É a forma mais forte quando a peça já provou tudo o que tinha para provar.

- "Topa resolver isso junto comigo? Então [...]" (qualquer nicho)
- "Quer aprender a fazer essa borda em dois minutos? Então [...]" (infoproduto, confeitaria)
- "Quer parar de pagar imposto a mais? Então [...]" (serviço, contabilidade)

**Os cinco moldes restantes**, todos válidos:

- **condicional de fecho**: "E se você quer as três coisas, você precisa [...]"
- **troca declarada**: "A única coisa que eu peço em troca são [prova do preset] minutos da sua
  atenção."
- **convite**: "A hora de resolver isso é agora. E pra isso eu tenho um convite."
- **promessa de entrega**: "A gente começa do zero e entrega pra você [o resultado concreto]."
- **escala mais anúncio da oferta**: "E isso é só o começo do que dá pra fazer."


Duas regras de forma que valem para qualquer molde:

1. **A ponte aponta.** Ou ela usa dêitico para o que apareceu na tela ("isso", "essa", "esse tipo
   de conteúdo", "as três coisas"), ou ela nomeia a troca. Ponte que não aponta nada não é ponte.
2. **Se a ponte é pergunta, a resposta é o CTA, ligada por "Então".** Nunca deixe a pergunta no ar
   e depois mande clicar: o "Então" é o que costura.

Declare onde ela está no campo `ponte` de `cta.md`, no formato `bloco N, "frase"`. Os marcadores
que o gate reconhece estão em `scripts/gate_copy/limiares.py`, na tupla `MARCADORES_DE_PONTE`, e
incluem as formas curtas dos moldes acima.

**Direção visual típica**: fim de um bloco de prova ou de oferta, sem elemento novo na tela.

**Exemplos**: serviço (clínica): *"É esse atendente que eu monto com você na aula."* Produto
físico (móveis planejados): *"É esse projeto que a gente desenha com você na visita."*

**Erro comum**: ponte genérica que não cita nada do que apareceu ("e tem muito mais te esperando").
Ponte é específica ou não é ponte.

### `C`: CTA

**O que faz**: pede UMA ação, no imperativo informal, com objeto explícito.

"Saiba mais" sozinho não é CTA: escreva a ação e o que ela entrega. Em carrinho e lote, some a
escassez legítima. Em frio, corte escassez, preço e data. Em orgânico, nada de clique nem link:
loop, pergunta ou pedido de envio.

**Direção visual típica**: lettering com verbo de ação e seta, logo e legenda juntos na base.

**Exemplos**: serviço (clínica): *"Toca em saiba mais e entra na aula do Agenda Cheia. Sai de lá
com o seu marcando."* Produto físico (móveis planejados): *"Toca aqui embaixo e agenda sua visita.
O projetista vai até você."*

**Erro comum**: duas ações no mesmo CTA, CTA vago, e fecho de urgência dupla e vazia (duas frases
empilhadas em que a segunda só repete a primeira).

### Regras de dinâmica que valem para qualquer papel

- **Nunca mais de duas frases seguidas de apresentador puro.** Entra insert, lettering ou garrafal.
- **A enumeração é o coração da peça**: 3 a 5 itens, cada um com corte visual próprio.
- **Escada de números** para dor ou ganho, quando o preset autoriza os números.
- **Frases-ponte curtíssimas seguram retenção** entre blocos: "E não para por aí.", "E o melhor:",
  "E mais:", "E de quebra…", "E no final, ele ainda…", "Saca só.", "Mas tem um porém."
- **Uma pergunta curta antes do exemplo** compra o bloco seguinte: "Quer um exemplo?", "Sabe
  porque?", "Legal né?". Custa duas palavras e muda o ritmo.
- **Palavra de ênfase vira lettering ou ênfase de legenda.** Escolha na escrita, não na edição.

---

## 4. As sequências válidas

Escolha a sequência **antes** de escrever a tabela de blocos, e declare no campo opcional
`sequencia` do `conceito.md`.

Uma linha por modo, pra decidir rápido:

- **Frio** (`frio`, `captacao`, `perpetuo_frio`): a peça constrói a crença antes de pedir qualquer
  coisa, o miolo é longo, e o CTA não tem escassez, preço nem data.
- **Quente, carrinho ou lote** (`carrinho`, `lote`, `remarketing`): o contexto já existe, a peça é
  curta, e o tempo vai todo pra oferta e pra decisão, com escassez legítima.
- **Orgânico** (`modo: organico`, qualquer campanha): mesma espinha do frio, mas o `C` não pede
  clique: ele fecha em loop, pergunta pra comentário ou pedido de envio (ver
  `references/modelo-mestre.md`, seção "Fechamento orgânico").

### Frio (`frio`, `captacao`, `perpetuo_frio`)

```
H    D  P  M  T  O  C           problema primeiro: nomeia a dor, prova, explica, ponte, oferta, pede
H    P  I  M  P+T  O  C         demonstração primeiro: quando existe tela, a tela abre e a prova vem antes
H    D  P  I  P  P  M  P+T  O  C   enumeração: um insert por item, com respiro entre os itens
H+I  P  P  P  M  T  O  C        filtro condicional: o hook já diz pra quem é, e a lista prova
```

A primeira serve quando o público está no nível 1 ou 2 (não sabe que tem o problema, ou sente a dor
sem conhecer o caminho). A segunda serve no nível 3, quando a pessoa já procura solução e o que
decide é ver a coisa funcionando.

A terceira e a quarta vieram da calibração contra os anúncios gravados
(`references/calibracao-jheni.md`, seção 3.2) e são as duas mais usadas naquele material. Duas
coisas importam nelas:

- **`P` repete, um bloco por item, com insert próprio em cada.** Não é exceção, é o formato.
- **Entre os itens entra um bloco sem insert.** Ele existe por dois motivos ao mesmo tempo: segurar
  a densidade de insert dentro da faixa, e dar o respiro que faz a lista soar falada. É onde cabe
  a frase de continuação ("E não para por aí.") e a identificação.
- **`H+I` é um bloco só.** O molde condicional ("Se você é X e quer Y…") faz hook e identificação
  na mesma frase, e nesse caso a identificação não volta depois.

Em frio, a proporção é 20 / 60 / 20: o miolo (`D`, `P`, `M`, `I`) carrega a peça.

### Quente (`carrinho`, `lote`, `remarketing`)

```
H  P  O+T  C           prova, oferta com a ponte na última frase, ação
```

Curta de propósito. O contexto já existe, então a peça gasta o tempo na oferta e na decisão:
proporção 20 / 20 / 60.

### Orgânico (`modo: organico`)

```
H  D  P  M  I  C           mesma espinha do frio, e o C fecha sem clique
H  P  P  P  M  C           demonstração seguida, quando existe cena ou tela pra mostrar
```

O `O` (oferta) e o `T` (ponte) continuam válidos no orgânico, mas eles não apontam pra um clique:
apontam pro que a pessoa leva assistindo até o fim. O `C` é loop, pergunta pra comentário ou pedido
de envio, nunca "link na bio" como ação principal.

### Como expandir sem quebrar

Papéis podem **repetir** e podem **compartilhar bloco**:

- Repetir `P` é o normal numa peça de enumeração: `H P P P M P O+T C` é a sequência quente com cinco
  provas em vez de uma.
- Compartilhar bloco significa dois papéis no mesmo bloco, o segundo na última frase. Escreva
  `P+T` ou `O+T` na coluna `papel`. É assim que a ponte costuma entrar sem custar um bloco inteiro.

Três coisas que a sequência sempre tem, em qualquer variação:

1. **`T` antes de `C`** (bloco próprio ou última frase de outro bloco, geralmente combinado com `O`
   ou `P`: `P+T`, `O+T`). O gate **reprova** sem isso.
2. **`O` entre a prova e o CTA** (bloco próprio ou combinado, `O+T`): nomeia a oferta e diz a
   entrega. O gate **reprova** sem isso ("CTA sem bloco de oferta").
3. **Ao menos um `P`.** O gate **avisa** quando não há nenhum: peça sem prova é peça pedindo fé.

---

## 5. Checklist de estrutura (rode ANTES do gate)

O gate mede a tela. Este checklist mede o argumento, e ele roda antes, na tabela de blocos, quando
consertar ainda é barato.

- [ ] **Temperatura e nível de consciência declarados?** Você sabe se está em frio ou quente, e em
      qual dos 5 níveis a pessoa está?
- [ ] **O gancho combina 2 elementos?** Um elemento só é frase, não é gancho.
- [ ] **Ao menos um dos três hooks é pergunta ou paradoxo?** Afirmação previsível não para ninguém.
- [ ] **Tem ao menos uma pergunta no CORPO?** Nos treze anúncios do estudo de caso, doze têm, e
      ela aparece sempre em um de três lugares: na virada, antes do exemplo ("Quer um exemplo?",
      "Sabe porque?") ou na própria ponte. Peça sem pergunta nenhuma é palestra.
- [ ] **A ponte usa um dos moldes?** Dêitico mais ensino, pergunta de adesão com "Então", ou um dos
      cinco restantes. Se ela não aponta nada do que apareceu na tela, reescreve.
- [ ] **Tem prova CONCRETA?** Tela real da coisa funcionando, ou caso com nome, número e contexto.
      "Funciona muito bem" não é prova.
- [ ] **O mecanismo está nomeado?** Dá para apontar a frase que diz por que isso funciona quando o
      resto não funciona? Se não dá, a promessa está pedindo fé.
- [ ] **Tem ponte antes do CTA?** Aponte a frase, o bloco, e o que ela liga. Se você não consegue
      apontar, o clique está sem objeto e a peça reprova.
- [ ] **Tem bloco de oferta antes do CTA?** Um bloco (próprio ou combinado com a ponte, `O+T`) que
      diz o que é a oferta, o que será feito, o que a pessoa ganha e como ela acessa. Sem isso, o
      gate reprova com "CTA sem bloco de oferta".
- [ ] **A promessa está calibrada pela temperatura?** Em frio: resultado grande e prazo curto. Em
      quente: probabilidade alta e esforço baixo.
- [ ] **A proporção bate com a temperatura?** Frio 20/60/20, quente 20/20/60. Conte os blocos.
- [ ] **A mensagem fala do que a temperatura pede?** Frio fala do problema ou da oportunidade;
      quente pode falar do produto.
- [ ] **Todo número tem dono e recorte, e sai do preset?** Número sem dono é história, não dado.
- [ ] **Nenhum bloco tem mais de duas frases de apresentador puro sem gancho visual?**
- [ ] **A sequência de papéis está escrita, e `T` vem imediatamente antes de `C`?**

Só depois disso vale escrever `roteiro.txt` e rodar `scripts/gate_copy.py`.

---

## Anti-padrões (nunca, em nenhuma temperatura)

- Hook institucional, morno, ou com saudação e apresentação.
- Promessa antes da prova quando existe uma tela disponível para mostrar.
- Parágrafo longo de apresentador falando sem gancho visual.
- Jargão técnico sem tradução imediata na mesma frase.
- Prova social sem nome, sem número ou sem contexto.
- Prova de passagem apresentada como prova de resultado.
- Oferta com preço, data ou escassez em campanha de tráfego frio.
- CTA sem ponte antes dele, e ponte genérica que não aponta nada do que apareceu na tela.
- CTA sem bloco de oferta antes dele: prova mais ponte direto pro "toca em saiba mais", sem dizer
  o que é a aula, o que será feito, o que a pessoa ganha e como acessa.
- Pergunta na ponte sem o "Então" que a costura no CTA: a pergunta fica no ar e o clique fica sem
  resposta.
- Inventar número, cliente ou demonstração que não existe.

A camada de voz (falada BR, frase curta, antítese paralela banida, números por extenso na fala) está
em `references/voz-e-anti-ia.md`, e vale por cima de tudo que está aqui.
