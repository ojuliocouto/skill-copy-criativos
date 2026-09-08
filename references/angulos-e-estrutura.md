# Ângulos e estrutura invisível (a biblioteca dos 78)

O `conceito.md` de todo pacote declara dois campos que vêm daqui: `angulo` e
`estrutura_invisivel`. Este arquivo é a lista completa dos dois, para você escolher sem depender
de nenhuma outra ferramenta.

**Ângulo** é o RECORTE do argumento: por onde a peça entra no problema. **Estrutura invisível** é
a ORDEM em que os elementos de persuasão aparecem dentro do gancho, do corpo e do CTA. Duas peças
podem ter o mesmo ângulo e estruturas diferentes, e é isso que faz uma leva de doze anúncios não
parecer o mesmo anúncio doze vezes.

Uma peça declara **um ângulo** e **uma estrutura**. Peças diferentes do mesmo lote não repetem o
par.

---

## 1. Os 78 ângulos, em 5 categorias

### Problema (20)

Dor e agitação (PAS) · Medo ou consequência futura · Inimigo comum · Nós contra eles · Erro
invisível · Sintoma que vira causa raiz · Mito ou crença falsa · Dilema · Paradoxo ·
Contra-intuitivo · Contraste · Custo oculto · Diagnóstico e autoidentificação · Frustração
acumulada · FOMO do problema · Urgência de contexto (assunto do momento) · Confissão e
vulnerabilidade · Comparação social negativa · Zeitgeist · Injustiça.

### Solução (18)

Novidade · Mecanismo único · Antes e depois · Comparação de métodos · Atalho · Simplicidade ·
Contra-mainstream ou segredo · Prova científica ou dado · Descoberta acidental · Jornada de
transformação · Empréstimo de autoridade · Origem improvável · Sem o sacrifício esperado ·
Demonstração · Futuro projetado (visualização) · Pequeno ajuste (1%) · Permissão · Velocidade do
resultado.

### Produto (15)

Prova social · Autoridade do criador · Feature que vira benefício · Bastidores · Especificidade ·
Estudo de caso · Superioridade declarada · Nova categoria · Tour, ou o que tem dentro · Endosso de
terceiros · Objeção respondida · Anti-venda e desqualificação · Identidade e status · Manada
qualificada · Origem e história do produto.

### Oferta (16)

Exclusividade · Escassez · Urgência com prazo · Ancoragem · Empilhamento de valor · Bônus
protagonista · Garantia e risco invertido · Gratuidade ou amostra · Custo por dia · Comparação de
custo · Facilidade de pagamento · Última chance · Reason why da oferta · Qualificação · Aumento
iminente · ROI declarado.

### Genéricos (9, servem em qualquer nível de consciência)

Curiosidade e loop aberto · Pattern interrupt · Pergunta direta · Dog whistle · UGC e nativo ·
Polêmica · Desafio · Analogia · Psicologia reversa.

### Como escolher

- **Público que ainda não sabe que tem o problema**: ângulo de Problema ou Genérico. Oferta e
  Produto aqui queimam a peça, porque falam de solução para quem não pediu solução.
- **Público que já sabe do problema e procura saída**: Solução.
- **Público que já conhece você**: Produto.
- **Público que já quer comprar e está decidindo**: Oferta. Só isso justifica escassez e preço, e
  só em campanha de carrinho ou lote (R6.4).
- Os ângulos de Oferta pedem campanha de carrinho ou lote. Em tráfego frio eles reprovam no gate,
  porque a peça abre vendendo antes de nomear o problema.

O nome do ângulo escolhido vai no `conceito.md` com a categoria entre parênteses, por exemplo:
`angulo: Custo oculto (categoria Problema, biblioteca dos 78)`.

---

## 2. A estrutura invisível: os 8 elementos

Todo roteiro é **gancho + corpo + CTA**. A estrutura invisível é a combinação destes oito
elementos dentro dessas três partes:

1. **Benefício funcional.** O que a coisa faz. "Responde no WhatsApp e marca na agenda."
2. **Benefício dimensional.** O tamanho do que ela faz: quanto, em quanto tempo, quantas vezes.
   "Responde em segundos, vinte e quatro horas por dia."
3. **Benefício emocional.** O que a pessoa deixa de sentir ou passa a sentir. "Você para de olhar
   o celular no meio do atendimento."
4. **Quebra de objeção.** Tempo, dinheiro, esforço, conhecimento ou risco. Uma por peça já basta;
   duas na mesma peça viram defesa.
5. **Credibilidade.** Demonstração, reason why, autoridade, estudo, depoimento, prova social,
   humildade, reconhecer o ceticismo, ou reduzir a promessa de propósito. Sempre ancorada no
   preset de oferta.
6. **Mecanismo do problema.** A causa por trás da dor. É o que separa a peça do concorrente que
   só descreve o sintoma.
7. **Mecanismo da solução.** Como a solução ataca aquela causa específica. Sem isso, a promessa
   fica sendo pedido de fé.
8. **Gatilhos mentais.** Novidade, urgência, escassez, exclusividade, curiosidade. Os três do
   meio só entram em carrinho ou lote.

### Combinações que funcionam (use como variador entre peças do mesmo lote)

| # | gancho | corpo | CTA |
|---|---|---|---|
| 1 | curiosidade + promessa | benefício funcional em lista | ação simples |
| 2 | dor com custo oculto | mecanismo do problema, depois mecanismo da solução | ação simples |
| 3 | credibilidade (caso nomeado) | benefício dimensional + quebra de objeção | ação simples |
| 4 | pattern interrupt | benefício emocional + prova social | ação simples |
| 5 | mito derrubado | mecanismo da solução + quebra de objeção de conhecimento | ação simples |
| 6 | pergunta direta | diagnóstico, depois benefício funcional | ação simples |
| 7 | promessa grande e específica | prova social + quebra de objeção de risco | escassez real (só carrinho) |
| 8 | confissão | jornada + mecanismo da solução | ação simples |
| 9 | comparação de custo | benefício dimensional + ROI | escassez real (só carrinho) |
| 10 | demonstração já no primeiro frame | benefício funcional + credibilidade | ação simples |

O campo `estrutura_invisivel` do `conceito.md` é essa combinação escrita em texto corrido, na
ordem dos blocos. Exemplo do pacote `agenda_cheia`:

```
estrutura_invisivel: gancho de dor com custo oculto no bloco 1; mecanismo do problema no
bloco 2; mecanismo da solução nos blocos 3 e 4; credibilidade por caso no bloco 5; custo
oculto nomeado no bloco 6; CTA sem escassez no bloco 7
```

Escrever a estrutura assim, bloco a bloco, é o que torna possível auditar a peça depois: dá para
apontar qual bloco carrega qual elemento, e qual elemento está faltando quando a peça não fecha.

---

## 3. Ângulo e tática de hook não são a mesma coisa

O **ângulo** é do conceito inteiro e vale para os três hooks e para o corpo. A **tática de hook**
(`references/taticas-de-hook.md`) é do molde da primeira frase, e os três hooks da matriz têm
táticas diferentes com o MESMO ângulo. Um conceito de ângulo "Custo oculto" pode abrir com
`shocking_statement`, com `contrarian` e com `question`: o recorte é o mesmo, o mecanismo de
parada é outro.
