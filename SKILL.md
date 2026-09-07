---
name: copy-criativos
description: "Escreve a COPY de criativos em vídeo (anúncio pago e peça orgânica: Reels, Shorts, TikTok, Stories, feed) já no formato que a esteira creative-studio consome: roteiro anotado bloco a bloco com direção de insert, LEAD e KEY, mais hooks com tática nomeada, garrafais, letterings, CTA por modo, origem dos assets e a matriz 3x2x2. A copy sai da mão do copywriter pronta pra virar peça sem retrabalho de edição. Triggers: copy de criativo, roteiro de anúncio em vídeo, roteiro anotado, hooks, matriz de criativos, pacote de copy, copy pra creative-studio, /copy-criativos."
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
pairs-with:
  - skill: creative-method-creator
    reason: escolhe conceito, ângulo (78) e estrutura invisível antes; esta skill escreve a partir do conceito aprovado
  - skill: creative-studio
    reason: a esteira em ~/creative-studio (repositório, CLI python -m creative_studio) consome o roteiro.txt deste pacote; ela nunca reescreve copy, esta skill nunca edita vídeo
---

# Copy de criativos (para a esteira creative-studio)

Esta skill escreve a copy de UM CONCEITO por vez e entrega um PACOTE (diretório com 8 arquivos),
não um texto. O arquivo central é o `roteiro.txt`, no formato anotado que a esteira lê
(`[inserção de vídeo: <asset> | LEAD: <lead> | KEY: <key>] fala`). A fronteira é essa: a copy
termina no `roteiro.txt`; a `creative-studio` começa nele e nunca reescreve uma palavra.

A regra de ouro, que vem das 31 decisões registradas do Júlio na peça piloto (a 1 e as 7 a 36;
as de número 2 a 6 não existem no arquivo): **a copy escolhe as palavras que vão virar tela
(garrafal, KEY, ênfase da legenda) e as coloca na fala; nunca o contrário.**
Lettering que a voz não diz é decoração, e garrafal escolhida por caber está proibida (decisão
8).

## O que precisa existir antes (onboarding)

Confira, nesta ordem, e recuse o pedido nomeando o que falta (R8.4 da spec):

1. **Brief com os 4 campos obrigatórios**: avatar (pra quem), promessa (uma frase), modo
   (`pago` ou `organico`) e canal (`reels`, `stories`, `feed_4x5`, `feed_1x1`, `tiktok`,
   `shorts`). Em modo pago, também a campanha (`frio`, `captacao`, `perpetuo_frio`, `carrinho`,
   `lote`, `remarketing`): é ela que decide se o CTA pode ter escassez e preço (R6.4).
2. **Conceito e ângulo**: um dos 78 ângulos da biblioteca do Léo e a estrutura invisível, vindos
   da skill `creative-method-creator`. Sem ângulo declarado, rodar a `creative-method-creator`
   primeiro (ela monta a matriz avatar x ângulo e o Júlio aprova antes de qualquer copy).
3. **Oferta e provas autorizadas**: preset da oferta (ex.:
   `~/.claude/skills/copywriter-video-ads/references/oferta-occ.md`). Número, nome de aluno,
   prova ou preço fora do preset não existe. Nunca inventar.
4. **Assets passados**: o que o Júlio ou o time já entregou pro conceito (asset marcado no doc,
   GalerIA, Drive, gravação). Se o brief veio em Google Doc com comentários, ler os comentários
   pela API antes (`python3 ~/.claude/scripts/ler-comentarios-doc.py <DOC_ID>`): comentário com
   N links = N assets naquele bloco.
5. **Acesso à esteira**: `~/creative-studio` existe. O gate tenta sozinho os dois caminhos
   padrão de lá, `config/taticas_hook.yaml` e `config/gates.yaml`, e aceita `--taticas` e
   `--gates` pra apontar outro lugar. Sem o repositório ele cai nas listas e limiares embutidos,
   e a entrega tem que dizer que rodou assim.

Quando faltar 1 ou 2, parar e pedir. Quando faltar 3 ou 4, escrever com placeholders
`[PROVA A CONFIRMAR]` e `origem: criar:...` e dizer isso na entrega. Nunca escrever "algo de
tecnologia" no lugar de um asset: direção vaga reprova no gate.

## Ler antes de escrever uma linha

- `references/regras-da-tela.md`: uma linha por decisão do Júlio que muda a copy (com o número
  da decisão e onde ela mora na esteira). É a fonte das regras abaixo.
- `references/formato-do-pacote.md`: o contrato dos 8 arquivos, campo a campo, e a tabela de
  números do gate (seção 9).
- `references/taticas-de-hook.md`: as 29 táticas da Motion por cluster, com exemplo na voz da
  casa e a regra de cluster por objetivo.
- Voz da casa: as memórias `feedback-voz-julio-anti-ia`, `feedback-antitese-paralela-cara-de-ia` e
  `feedback-headlines-julio` (no diretório de memória do Claude Code, quando existirem).
- Exemplo do que "pronto" significa: `exemplos/cinco-entregas/` (o conceito do ad21v2
  reconstruído; o `README.md` de lá explica cada diferença em relação ao gravado).

## O pacote (a saída)

```
<saida>/<conceito>/
  conceito.md      ângulo, avatar, promessa, modo, canal, campanha, marcas, brief resumido
  roteiro.txt      o roteiro anotado da esteira, um bloco por linha
  hooks.md         3 hooks com tática nomeada (um cru), regra 3-2-2 do Léo
  garrafais.md     as 2 ou 3 palavras de maior carga de copy, com a frase âncora
  letterings.md    LEAD e KEY por bloco, com a palavra âncora e a forma
  cta.md           fechamento por modo
  assets.md        origem e enquadramento de cada insert
  matriz.md        as 12 peças nomeadas: {conceito}_{canal}_{formato}_{hook}_{legenda}_v{n}
```

Diretório de saída padrão: `~/creative-studio/copy/<conceito>/`. Se o Júlio pedir outro, usar o
que ele pedir. Cada arquivo tem formato fixo (ver `references/formato-do-pacote.md`); o gate lê
exatamente aquilo.

## As regras de escrita que vêm da tela (resumo; o detalhe está em `regras-da-tela.md`)

Números de partida: a voz do Thales mede 2,9 palavras por segundo em fala natural (ad21v2), e a
peça é entregue a 1,45x. Tudo abaixo é em tempo FINAL, que é onde a esteira mede.

| regra | número | por quê |
|---|---|---|
| bloco com insert | 15 palavras ou mais (3,5s finais) | o b-roll roda em 1,0x e precisa de tempo; bloco curto não comporta insert (decisões 29 e 30) |
| bloco com KEY em placa (`h1`, `h2` ou `h4`) | 12 palavras ou mais (2,8s + 0,25s por palavra além da segunda) | tempo de leitura do lettering (decisão 29) |
| bloco com KEY em coluna ou carimbo | 15 palavras ou mais (3,5s) | a coluna obriga o olho a girar, o carimbo é pequeno |
| bloco com KEY em `seta_cta` | 12 palavras ou mais (2,8s) | `permanencia_min_ms.seta_cta` |
| forma do lettering | `placa_h1`, `placa_h2`, `placa_h4`, `coluna`, `carimbo`, `seta_cta`; a mesma forma nunca em dois blocos vizinhos com lettering | o rodízio de `gates.yaml -> dinamica.lettering.rodizio` são os três estilos de placa (`h1`, `h2`, `h4`) e `.formas` guarda só `coluna` e `carimbo`, com `repetir_vizinho: false`. "Placa" não é forma única: h1 depois de h2 é rodízio funcionando. Sequência aprovada no `MAPA-LETTERINGS.md`: h2 no gancho, depois h1, h2, coluna, h4, h1, carimbo, seta_cta |
| carimbo | só em bloco que tem insert | é lettering de APOIO: marca onde a peça está quando o insert já é o assunto |
| bloco de CTA | 13 palavras ou mais (3,0s) e no máximo 21 (5,0s) | janela final do CTA (R6.3, `pago.yaml -> fechamento.janela_final_min_s` e `.janela_final_max_s`); acima de 21 palavras é aviso |
| bloco sem insert e sem KEY | 25 palavras no máximo (6,0s) | bloco único acima disso REPROVA (R3.3) |
| blocos vizinhos sem insert | somados, 25 palavras no máximo (6,0s), mesmo com KEY | AVISA, porque o lettering cobre só parte do bloco (R3.3) |
| peça pago frio e orgânico | 15 a 30s finais = 64 a 126 palavras | R6.1; remarketing 6 a 15s = 26 a 63 palavras |
| peça de carrinho ou lote | sem faixa própria: usa a de frio como referência, e o número vira aviso | `pago.yaml -> duracao` só declara `frio` e `remarketing`; a peça v5.7 aprovada tem 41,48s (decisão 36) |
| hook | até 14 palavras (5s naturais); problema ou promessa nas 4 primeiras palavras | R1.3 e R2.6 |
| marca, produto, evento | marca dentro das 12 primeiras palavras do bloco 1 ou de qualquer hook REPROVA, salvo hook com `- logo_ancorado: sim` em `hooks.md`, que vira aviso; nas 3 primeiras palavras reprova sempre | R2.5 e decisão 11; o teto das 3 palavras é regra do brief ("nunca abre com marca"), valor de partida |
| frase | até 14 palavras de conforto, 20 é o teto | valor de partida do brief: a R5.2 publica o bloco de legenda de 2 a 3 palavras em 2 linhas, não o número de palavras por frase |
| KEY | até 2 palavras de conteúdo (algarismo e "de", "no", "que" não contam), substantivo forte, todas ditas na fala | legível em corpo pequeno (68px no gancho, 84px no painel do insert, decisão 10 e `posicao_por_contexto`); a esteira ancora no alinhamento da voz |
| LEAD | contexto curto, até 4 palavras, itálico | é o "entrega cinco" acima do "UM SQUAD" |
| garrafal | 2 ou 3 por peça, no máximo 2 no gancho; dita na fala; nunca repete o KEY do bloco; fora do bloco 1, só em bloco sem insert E sem KEY | decisão 8 e `MAPA-GARRAFAIS.md` (ela vive entre o fundo e a pessoa, e ainda pede 80ms de folga do lettering) |
| números | por extenso na fala ("oito mil"), algarismo no lettering ("8 MIL", "2 DIAS", "5 ENTREGAS") | voz da casa; a ênfase forte da legenda tem gatilho de número |
| conteúdo que envelhece | data, preço, edição e lote numerado só em `carrinho` e `lote` | decisão 19 e R6.4 |
| um insert por bloco | e o bloco DIZ o que a tela mostra ("Cinco: um squad" pede tela de squad) | a esteira casa asset por âncora exata |
| espalhar os inserts | 45 a 55% do tempo de cada janela com insert, a partir de 3,0s; blocos de insert colados estouram a janela do corpo | R3.4, `gates.yaml -> retencao.densidade_insert` e `.janelas` (corpo de 3 a 15s, fecho de 15s ao fim) |
| direção do bloco | vem da copy e não se troca: se o asset não tem o movimento que a fala descreve, a esteira produz o movimento, nunca vira o bloco em avatar | `feedback-copy-manda-a-direcao-do-bloco` |
| voz | curta, direta, "pra", "tá", sem antítese paralela ("não é X. É Y."), sem saudação, sem "eu sou o Thales" | `feedback-voz-julio-anti-ia` |

Fechamento por modo (R6.3 a R6.5):

- **Pago, carrinho ou lote**: verbo de ação + escassez legítima. "Toca em saiba mais e garante
  seu ingresso, ainda tem vaga."
- **Pago, frio, captação ou perpétuo**: verbo de ação, sem escassez, sem preço, sem data.
- **Orgânico**: nunca link nem clique. Loop (a última frase casa com a primeira), pergunta pra
  comentário ou pedido de envio ("manda pra quem...").

Assets (decisões 12, 15, 21, 30, 31, 34, 35): o insert é feito com o que foi PASSADO. Só quando
não há nada pronto pro bloco a esteira cria (captura real em telefone, depois UI fiel em HTML,
depois gerado com DNA), direcionada pela fala e proposta antes ao Júlio. Asset horizontal ou
borrado é o que mais derruba a peça, mas asset do briefing é intocável: a copy marca `serve:
não` com a ressalva em `assets.md`, nunca troca por conta. Enquadramento padrão `inteiro`;
`foco` só leve.

## Processo (o que funcionou no piloto)

1. **Ler o brief e o conceito.** Conferir os 5 itens do onboarding. Recusar sem avatar,
   promessa, modo e canal.
2. **Rascunhar o roteiro por blocos e mostrar EM TABELA** antes de polir qualquer coisa:
   colunas `bloco | fala | palavras | insert | LEAD | KEY`. Marcar em cada linha o mínimo de
   palavras exigido e se passa. O Júlio aprova bloco a bloco; só depois de aprovado é que o
   texto vira `roteiro.txt`.
3. **Gerar os 3 hooks** com tática nomeada (`references/taticas-de-hook.md`): cluster de
   interrupção ou curiosidade em frio; promocional liberado só em carrinho, lote ou prazo. Um dos
   três é cru (nota de voz, sem lettering, sem avatar). Ids distintos. Mostrar os três em tabela
   (`hook | tática | cluster | fala | palavras | âncora | cru`) e pedir a escolha ou o mix.
   O Hook A é a fala do bloco 1; B e C entram antes do bloco 1 na montagem.
4. **Fechar garrafais, letterings e CTA** nos arquivos próprios, com a âncora da fala em cada
   um. Preencher `assets.md` (origem de cada insert) e `matriz.md` (12 nomes).
5. **Rodar o gate**:
   ```bash
   /usr/bin/python3 ~/.claude/skills/copy-criativos/scripts/gate_copy.py <saida>/<conceito> \
     --gates ~/creative-studio/config/gates.yaml \
     --taticas ~/creative-studio/config/taticas_hook.yaml
   ```
   As duas flags são opcionais: o gate tenta esses mesmos dois caminhos sozinho. Passe as duas
   explicitamente quando quiser deixar registrado na entrega contra qual config ele rodou.
   Ele reprova nomeando o bloco (palavras contra o tempo de leitura do insert e do lettering,
   âncora do hook até 1,2s, marca nas 12 primeiras palavras sem `logo_ancorado: sim` e nas 3
   primeiras sempre, forma de lettering repetida em bloco vizinho, CTA coerente com o modo, bloco
   sem direção, palavra de lettering fora da fala, asset sem origem, matriz incompleta) e avisa o
   que não reprova (antítese paralela, algarismo na fala, marca entre as 12 primeiras palavras
   COM `logo_ancorado: sim`, blocos vizinhos sem insert somando mais de 6,0s, densidade de insert
   fora de 45 a 55% por janela, CTA acima de 5,0s, janelas de insert de R3.2, duração fora da
   faixa). Corrigir e rodar de novo até zero reprovações. Aviso
   fica registrado na entrega, não se esconde.
6. **Entregar o pacote**: caminho do diretório, a tabela final de blocos, os 3 hooks, os avisos
   que ficaram e a frase "a creative-studio consome o `roteiro.txt` direto". Nada de "pronto"
   sem o output do gate colado na entrega.

## Auditoria antes de entregar (além do gate)

- [ ] Cada bloco diz o que a tela mostra? Direção de insert específica, escrita pra quem vai
  buscar ou criar o asset?
- [ ] Toda palavra de KEY, LEAD e garrafal está na fala, no bloco certo?
- [ ] O hook nomeia problema ou promessa nas 4 primeiras palavras e não abre com marca?
- [ ] CTA bate com o modo e a campanha?
- [ ] Nenhum número ou prova fora do preset da oferta?
- [ ] Zero travessão, acentuação completa, voz falada BR, nenhuma frase com cara de IA?
- [ ] O gate rodou e o output está na entrega?

## O que esta skill NÃO faz

- Não edita vídeo, não escolhe arquivo de asset, não renderiza nada: isso é da
  `creative-studio`.
- Não escolhe conceito nem ângulo do zero: isso é da `creative-method-creator`.
- Não escreve copy longa (página, VSL, e-mail): `narrativa-lancamento`, `funil-vsl`,
  `copy-pagina-vendas`.
- Não inventa prova, número, aluno ou demo.

## Handoff

Entregar no chat: caminho do pacote, tabela de blocos, os 3 hooks, output do gate, avisos que
ficaram. A esteira segue com `creative-studio` lendo `<saida>/<conceito>/roteiro.txt` e os
demais arquivos do pacote.
