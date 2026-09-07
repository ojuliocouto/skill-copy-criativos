# Regras da tela: o que a copy de um criativo em vídeo precisa saber da edição

Este arquivo é a lista completa do que a edição vai fazer com o seu texto, escrita para quem
escreve o roteiro anotado antes de a esteira `creative-studio` montar a peça. Você não precisa
abrir o repositório: tudo que a tela exige está aqui, com o número e o lugar onde ele mora.
A regra de ouro é uma só: **a copy escolhe as palavras que viram tela e as põe na fala, nunca o
contrário.** Palavra grande escolhida porque cabe na faixa é decoração; palavra dita na fala e
marcada como KEY ou garrafal é a peça funcionando. Se a palavra certa não couber, o corpo desce
até ela caber, ou ela não entra: o que nunca acontece é a medida escolher a palavra.

---

## 1. Hook (os 3 primeiros segundos)

| nº | o que a tela exige | consequência para a copy | onde mora |
|---|---|---|---|
| R2.1 | Texto na tela até 1,0s e no máximo 1,0s acumulado sem texto dentro dos 3s | O bloco 1 nasce com `KEY` marcado, salvo quando o hook é cru | `config/gates.yaml -> hook.texto_ate_s`, `.acumulado_sem_texto_max_s` |
| R2.2 | Primeira palavra falada até 0,5s da peça final | Comece o bloco 1 com palavra de conteúdo, nunca com respiro ou muleta | `config/gates.yaml -> hook.primeira_palavra_ate_s` (valor de partida) |
| R2.3 | Uma mudança visual entre 0 e 3,0s | O bloco 1 declara insert, lettering ou garrafal; hook só de rosto parado não passa | `config/gates.yaml -> hook.mudanca_visual_ate_s` |
| R2.4 | Frame 1 não pode ser avatar parado sem elemento gráfico | Se o hook abre no apresentador, marque `LEAD`/`KEY` ou garrafal nesse mesmo bloco | `config/gates.yaml -> hook.frame1_avatar_exige_elemento` |
| R2.5 | Logo, marca e nome do produto proibidos nos 3s | Marca dentro das 12 primeiras palavras do bloco 1 ou de qualquer hook REPROVA, salvo hook com `- logo_ancorado: sim` em `hooks.md`, que vira aviso; marca nas 3 primeiras palavras reprova sempre | `config/gates.yaml -> hook.logo_proibido_ate_s`, decisão 11, seção 9 do `formato-do-pacote.md`; o teto das 3 palavras é regra do brief ("nunca abre com marca"), valor de partida sem medição própria |
| R2.6 | Problema ou promessa nomeado até 1,2s e nada de apresentação | Ponha a âncora de problema ou promessa nas 4 primeiras palavras; proibido "eu sou o", "meu nome é" | `config/gates.yaml -> hook.problema_nomeado_ate_s`, `.apresentacao_nas_duas_primeiras_frases` |
| R2.7 | O gate mede texto, fala e visual separados e reprova em qualquer um | Hook incompleto em um canal derruba a peça inteira: entregue os três no mesmo bloco | `config/gates.yaml -> hook.canais_medidos` |
| R2.8 | Hook trocado por medição de impressões, nunca por leitura pontual | Escreva os 3 hooks já na entrega: o segundo entra sem pedir copy nova | `docs/creative-studio-spec.md -> R2.8`, `config/gates.yaml -> regua.amostra_minima` |
| decisão 10 | O KEY do gancho pousa no TOPO, acima da cabeça, e o corpo cai para 68px | KEY do hook curto e legível em corpo pequeno: 2 palavras, sem palavra comprida | `config/gates.yaml -> dinamica.lettering.gancho_no_topo`, decisão 10 |
| decisão 11 | Logo do evento é liberado nos 3s quando o nome do evento é DITO naquele instante | Se quiser o logo cedo, escreva o nome do evento na fala do bloco e declare a âncora | `config/gates.yaml -> hook.logo_ancorado_na_fala_permitido`, decisão 11 |
| R1.3 e R1.5 | Hook alternativo é fala curta do mesmo lote de voz; um dos três é cru | Cada hook tem até 5,0s de fala natural (14 palavras); o cru vai sem lettering | `config/gates.yaml -> diversidade.hook_fala_max_s`, `.matriz.hooks_crus_min` |

## 2. Blocos e duração

| nº | o que a tela exige | consequência para a copy | onde mora |
|---|---|---|---|
| R3.1 | Um evento visual a cada 5,0s no máximo, entre 3s e 15s | Nenhum bloco de fala corrida longa: quebre em blocos que peçam insert ou KEY | `config/gates.yaml -> retencao.intervalo_max_evento_s` |
| R3.2 | Primeiro insert entre 5 e 10s; segundo entre 12 e 20s quando a peça passa de 15s | Distribua as marcações de insert nessas janelas, não todas no começo | `config/gates.yaml -> retencao.insert_1`, `.insert_2` |
| R3.3 | Avatar sozinho no máximo 6,0s seguidos | Bloco único sem insert e sem KEY acima de 6,0s (25 palavras) REPROVA; blocos vizinhos sem insert, mesmo com KEY, somando acima de 6,0s AVISA (o lettering cobre só parte do bloco) | `config/gates.yaml -> retencao.avatar_sozinho_max_s`, seção 9 do `formato-do-pacote.md` |
| R3.4 | Densidade de insert medida por janela (hook, corpo, fecho) | Espalhe os inserts pelas três janelas; não deixe o fecho sem nenhum | `config/gates.yaml -> retencao.densidade_insert`, `.janelas` |
| R3.4 | A densidade fica entre 45% e 55% do tempo de cada janela com insert, a partir de 3,0s | Blocos de insert colados estouram a janela do corpo (3 a 15s); intercale um bloco de apresentador entre eles. As janelas são corpo, de 3 a 15s, e fecho, de 15s ao fim | `config/gates.yaml -> retencao.densidade_insert.min`, `.max`, `.aplica_a_partir_de_s`, `.janelas` |
| R3.5 | No split o insert ocupa mais área que o avatar | Bloco com insert é bloco em que o insert é o assunto: escreva a fala citando o que aparece | `config/gates.yaml -> inserts.split.fracao_painel_insert` |
| decisão 23 | Entrega acelerada a 1,45x, aplicada antes de transcrever | Toda conta de tempo é palavras / 2,9 / 1,45: escreva mais palavras do que a duração final sugere | `config/modos/pago.yaml -> aceleracao.fator`, decisão 23 |
| decisão 29 | Lettering tem permanência mínima: 2,8s placa (`h1`, `h2` e `h4`), 2,8s `seta_cta`, 3,5s coluna e carimbo, mais 0,25s por palavra além da segunda | Bloco com KEY em placa ou `seta_cta` pede 12 palavras de fala; em coluna ou carimbo, 15 | `config/gates.yaml -> dinamica.lettering.permanencia_min_ms`, `.leitura_por_palavra_extra_ms`, `.palavras_de_graca` |
| decisão 30 | B-roll corre em 1,0x, nunca acelerado junto com a fala | Bloco com insert precisa de 15 palavras de fala para o asset respirar | decisão 30, seção 9 do `formato-do-pacote.md` |
| decisão 24 | Vídeo, voz e wav de transcrição saem do mesmo fator | Só edição; a copy não faz nada | decisão 24, gate `R8.1-sincronia-fator` |

## 3. Insert e asset

| nº | o que a tela exige | consequência para a copy | onde mora |
|---|---|---|---|
| decisão 12 | Todo insert DECLARA o que mostra: `inteiro` ou `foco`, sem meio termo | Uma linha por insert em `assets.md`, com o enquadramento declarado; sem isso o motor recusa | `config/gates.yaml -> inserts.enquadramento.declaracao_obrigatoria`, decisão 12 |
| decisão 15 | O padrão é `inteiro`; `foco` só até 1,25x; asset que não lê é trocado, nunca ampliado | Marque `foco` só quando a fala cita um pedaço específico, e escreva na ressalva qual é | `config/gates.yaml -> inserts.enquadramento.padrao`, `.foco_escala_maxima`, decisão 15 |
| decisão 21 | Proibido desfoque, véu, escurecimento ou opacidade sobre insert | Nunca peça "asset desfocado ao fundo": o fundo do painel é cor sólida da casa | `config/gates.yaml -> inserts.fundo.modo`, decisão 21 |
| decisão 31 | Zero filtro de desfoque em qualquer estágio do pipeline do insert | Reforça a linha acima: direção com "borrado" na âncora reprova | decisão 31 |
| decisão 30 | O conteúdo do insert nunca corre acima de 1,0x da origem | Direção do tipo "pipoca" ou "sequência" precisa de bloco longo, nunca de 2 segundos | decisão 30 |
| decisão 34 | O insert é feito com o que foi PASSADO; criar por conta só quando não há nada pronto | `origem` em `doc`, `galeria`, `drive` ou `gravacao`; `criar:*` só com proposta antes | seção 7 do `formato-do-pacote.md`, decisão 34 |
| decisão 35 | Asset do briefing é intocável, mesmo quando parece fraco | Não troque asset por conta: marque `serve: não` e escreva a ressalva | decisão 35 |
| memória | Asset horizontal ou borrado é o que mais derruba a peça | Asset assim entra com `serve: não` e ressalva, e a fala não pode depender de detalhe dele | seção 7 do `formato-do-pacote.md` (decisões 12, 15, 21, 30, 31) |
| decisão 18 | As duas variantes do squad aprovadas para a biblioteca | Só edição; a copy não faz nada | decisão 18 |
| memória | A direção do bloco vem da COPY e não se troca | Se o asset não tem o movimento que a fala descreve, a esteira PRODUZ o movimento; o bloco nunca vira avatar por causa do asset. Bloco escrito pra abrir em insert abre em insert | `feedback-copy-manda-a-direcao-do-bloco.md` (leva 2 da OCC: 5 de 9 anúncios tiveram a abertura invertida assim) |

## 4. Lettering: LEAD e KEY

| nº | o que a tela exige | consequência para a copy | onde mora |
|---|---|---|---|
| decisão 1 | A zona útil é medida por faixa de altura (x até 930 acima dos botões) | KEY com no máximo 2 palavras, 3 só no CTA: é o que cabe sem o corpo desabar | `config/gates.yaml -> safezone.faixas_da_zona_util`, decisão 1 |
| decisão 13 | O lettering do corpo é diagramado por CONTEXTO, com três pousos | Marque `KEY` no bloco certo: avatar sozinho pousa no topo, bloco com insert pousa no painel | `config/gates.yaml -> dinamica.lettering.posicao_por_contexto`, decisão 13 |
| decisão 13 | O rodízio é `h1`, `h2` e `h4` (os três estilos de placa), mais as duas formas alternativas, `coluna` e `carimbo`, e a `seta_cta` do fechamento | Escreva a forma por bloco em `letterings.md` pelo nome do estilo (`placa_h1`, `placa_h2`, `placa_h4`, `coluna`, `carimbo`, `seta_cta`), nunca "placa" como forma única: h1 seguida de h2 é rodízio, não repetição. A mesma forma nunca em dois blocos vizinhos com lettering. Sequência aprovada: h2 no gancho, depois h1, h2, coluna, h4, h1, carimbo, seta_cta | `config/gates.yaml -> dinamica.lettering.rodizio` (`[h1, h2, h4]`), `.formas` (coluna e carimbo), `.repetir_vizinho: false`, `piloto/etapas/etapa5/MAPA-LETTERINGS.md` |
| decisão 13 | O carimbo é lettering de APOIO, não pede o quadro | Marque `carimbo` só em bloco que tem insert: ele existe pra marcar onde a peça está quando o insert já é o assunto | `config/gates.yaml -> dinamica.lettering.formas.carimbo`, `MAPA-LETTERINGS.md` (L6) |
| decisão 14 | Lettering pode dividir a tela com o insert quando pousa no painel | Pode e deve parear insert e KEY no MESMO bloco: é o pareamento que o doc faz de propósito | `config/gates.yaml -> colisao.regras[R8.1-folga-lettering].excecao`, decisão 14 |
| decisão 20 | Os templates de insert nascem com rodapé reservado para o lettering | Reforça o pareamento acima: bloco com insert aceita KEY sem brigar com o asset | decisão 20 |
| decisão 29 | Lettering precisa de tempo de leitura, e quem cede é o insert, nunca o lettering | KEY de 3 palavras em coluna pede 16 palavras de fala (3,5s + 0,25s da terceira = 3,75s) | `config/gates.yaml -> dinamica.lettering.permanencia_min_ms`, `.quem_cede` |
| decisão 33 | A coluna vertical não divide faixa com a legenda (folga de 24px) | Não escreva KEY comprido para coluna: ela encolhe até 60px antes de a legenda ceder | `config/gates.yaml -> colisao.faixa_da_legenda`, decisão 33 |
| R5.6 | Lettering e legenda alternam, com ao menos um lettering de impacto além do hook | Garanta pelo menos um KEY forte no corpo, fora do hook e fora do CTA | `config/gates.yaml -> legenda.alternar_com_lettering`, `.letterings_de_impacto_min` |
| decisão 13 | O LEAD é o contexto em itálico acima do KEY | LEAD com até 4 palavras; LEAD fora da fala é aviso, não reprovação | seção 5 do `formato-do-pacote.md`, `templates/lettering/*.html` |
| decisão 13 | Toda palavra do KEY tem que estar na fala do bloco | Escreva a fala primeiro e recorte o KEY dela; algarismo casa com número por extenso | seção 5 do `formato-do-pacote.md` |
| decisão 9 | Colisão medida no quadro final, em vários instantes, valendo o pior caso | Só edição; a copy não faz nada | decisão 9 |

## 5. Garrafal (a palavra grande atrás do apresentador)

| nº | o que a tela exige | consequência para a copy | onde mora |
|---|---|---|---|
| decisão 8 | A garrafal é ancorada na COPY: a maior carga do bloco (promessa, número da promessa ou dor) | Escolha a palavra pelo peso dela na fala, nunca porque cabe na faixa | `config/gates.yaml -> dinamica.garrafal.ancorada_na_copy`, decisão 8 |
| decisão 8 | A garrafal é sincronizada com o instante em que a palavra é dita | Declare a âncora: a palavra tem que estar na fala daquele bloco | `garrafais.md` (campo `ancora`), decisão 8 |
| decisão 8 | Nunca repete a palavra que o KEY do mesmo bloco já diz | Se o bloco já tem KEY, a garrafal carrega OUTRA palavra da mesma fala | `config/gates.yaml -> dinamica.garrafal.nao_repetir_o_lettering` |
| MAPA-GARRAFAIS | Ela vive entre o fundo e a pessoa: só onde o apresentador está SOZINHO em tela | Fora do bloco 1, marque garrafal só em bloco SEM `inserção de vídeo` e SEM `KEY`: insert por cima apaga o efeito e lettering junto empilha dois textos grandes (a garrafal ainda pede 80ms de folga do lettering) | `piloto/etapas/MAPA-GARRAFAIS.md`, regra 1, `config/gates.yaml -> dinamica.garrafal.folga_para_o_lettering_ms` |
| decisão 8 | Máximo 2 por gancho | No bloco 1 cabem 2 garrafais; a terceira vira três camadas de texto | `config/gates.yaml -> dinamica.garrafal.maximo_por_gancho` |
| decisão 10 | Estilo G2: laranja da casa a 0,8, atravessando o quadro devagar | Palavra curta e forte: a travessia entrega a palavra ao longo do tempo | `config/gates.yaml -> dinamica.garrafal.cor`, `.travessia_px`, decisão 10 |
| decisão 10 | Paleta por PAPEL, não por gosto: `casa` é a marca e a oferta, `quente` é o resultado, `teal_do_fundo` e `rosado_do_fundo` recuam | Declare a cor pelo papel da palavra na argumentação | `config/gates.yaml -> dinamica.garrafal.paleta`, `MAPA-GARRAFAIS.md` |
| MAPA-GARRAFAIS | O número vai em algarismo na tela e por extenso na fala | Escreva "dois dias" na fala e "2 DIAS" na garrafal: o gate casa os dois | `piloto/etapas/MAPA-GARRAFAIS.md`, seção 4 do `formato-do-pacote.md` |

## 6. Legenda queimada

| nº | o que a tela exige | consequência para a copy | onde mora |
|---|---|---|---|
| R5.1 | Legenda queimada obrigatória em todos os modos e canais | Toda palavra escrita na fala vai aparecer na tela: sem muleta, sem palavra de enrolar | `config/gates.yaml -> legenda.queimada_obrigatoria` |
| R5.2 | Blocos de 2 a 3 palavras, no máximo 2 linhas, zero bloco de 1 palavra | Frase acima de 20 palavras reprova e acima de 14 avisa. Os dois números são VALOR DE PARTIDA do brief: a R5.2 não publica número de palavras por frase, só o tamanho do bloco de legenda | `config/gates.yaml -> legenda.palavras_por_bloco`, `.linhas_max`; 14 e 20 são valor de partida |
| R5.2 | Corpo de 72px (64px no split), dwell mínimo de 0,34s por bloco | Frase curta e falada em ritmo normal: frase longa vira parede de legenda | `config/gates.yaml -> legenda.corpo_px`, `.dwell_min_s` |
| R5.3 | Palavra de ênfase em laranja da casa (#FA4E04) | A ênfase é escolhida por CONTEÚDO, então plante as palavras que merecem destaque | `config/gates.yaml -> legenda.enfase_cor` |
| R5.3 | Ênfase FORTE só com gatilho: número na palavra ou palavra de promessa | Use número na fala e palavras da lista (prontas, sozinha, grátis, hoje, agora, garantido) | `config/gates.yaml -> legenda.enfase.forte.gatilho_numeros`, `.gatilho_palavras` |
| R5.4 | Texto queimado cobre no mínimo 95% das palavras faladas; vão sem texto no máximo 12% e nunca acima de 2,5s | A fala escrita tem que ser a fala gravada, palavra por palavra | `config/gates.yaml -> legenda.cobertura_min`, `.vaos` |
| decisões 16 e 17 | Cama de música 18 dB abaixo da voz falada, clima T3 na peça | Só edição; a copy não faz nada | `config/gates.yaml -> montagem.audio.camas`, decisões 16 e 17 |

## 7. Fechamento e CTA

| nº | o que a tela exige | consequência para a copy | onde mora |
|---|---|---|---|
| R6.1 | Duração final: pago frio e orgânico 15 a 30s; remarketing 6 a 15s | Peça de 15 a 30s finais = 64 a 126 palavras no roteiro inteiro. `pago.yaml -> duracao` só tem faixa pra `frio` e `remarketing`: `carrinho` e `lote` NÃO têm faixa declarada e usam a de frio como referência, com o número registrado como aviso (a peça v5.7 aprovada tem 41,48s) | `config/modos/pago.yaml -> duracao`, `config/modos/organico.yaml -> duracao`, decisão 36 |
| R6.2 | Aceleração 1,45x aplicada antes de transcrever | Toda conta de duração parte de palavras, nunca de segundos escritos à mão | `config/modos/pago.yaml -> aceleracao.fator` |
| R6.3 | No modo pago, os últimos 3 a 5s têm CTA falado E lettering com verbo de ação, mais seta quando o canal tem botão | Bloco de CTA com no mínimo 13 palavras e verbo da lista da esteira na fala | `config/modos/pago.yaml -> fechamento`, seção 6 do `formato-do-pacote.md` |
| R6.3 | CTA vago reprova | "Saiba mais" sozinho não é CTA: escreva a ação e o objeto ("garante seu ingresso") | `config/modos/pago.yaml -> fechamento.cta_vago_reprova` |
| R6.4 | Oferta, prazo e preço no CTA só em carrinho ou lote | Em captação e perpétuo frio, corte escassez, preço e data da fala do CTA | `config/modos/pago.yaml -> fechamento.oferta_no_cta` |
| R6.5 | No orgânico a peça não pede clique nem mostra link | Fechamento em loop, pedido de envio ou pergunta; proibido "toca em", "clica", "link", "bio" | `config/modos/organico.yaml -> fechamento.saidas` |
| R6.6 | Fechamento em loop exige último quadro parecido com o primeiro | Se declarar loop, escreva a frase partida que termina onde a peça começa | `config/gates.yaml -> loop.diferenca_max` |
| decisão 7 | O KEY do CTA é "GARANTE SEU INGRESSO", com a seta do estilo `seta_cta` | KEY do CTA aceita 3 palavras (verbo + objeto); o resto do roteiro fica em 2 | decisão 7, seção 5 do `formato-do-pacote.md` |
| decisões 22, 25, 26 | Onde o CTA pousa foi decidido três vezes (base, topo, e por fim rodapé abaixo do logo e da legenda) | Histórico é de edição: a copy só garante que o CTA é lettering com verbo e seta | decisões 22, 25 e 26 |
| decisões 28 e 32 | O pacote de fechamento é logo + CTA + seta juntos na base, com folga do queixo | Só edição; a copy só entrega o bloco do CTA com o logo declarado na direção | decisões 28 e 32 |
| decisão 11 | O logo do fechamento é legítimo porque o nome do evento é dito | Diga o nome do evento na fala do bloco do CTA ou no anterior | decisão 11, `cta.md` (campo `logo`) |

## 8. Matriz e diversidade

| nº | o que a tela exige | consequência para a copy | onde mora |
|---|---|---|---|
| R1.2 | Matriz mínima de 3 hooks x 2 legendas x 2 formatos, com ao menos um formato sem avatar | Entregue 12 peças nomeadas em `matriz.md`, nunca uma peça solta | `config/gates.yaml -> diversidade.matriz` |
| R1.3 | Hooks alternativos são falas curtas do mesmo lote de voz | Cada hook cabe em 5,0s naturais, ou seja, 14 palavras | `config/gates.yaml -> diversidade.hook_fala_max_s` |
| R1.4 | Cada hook tem tática nomeada, e o cluster depende do objetivo | Em frio, só `interrupcao_padrao` e `curiosidade`; em carrinho entra `promocional` | `config/modos/pago.yaml -> clusters_hook`, `references/taticas-de-hook.md` |
| R1.5 | Ao menos 1 dos 3 hooks é cru, sem lettering de abertura | Escreva um hook que funcione sem texto na tela, só pela fala | `config/gates.yaml -> diversidade.matriz.hooks_crus_min` |
| R1.6 | A peça declara MODO e CANAL primário | `modo` e `canal` no front matter do `conceito.md`, sem exceção | `docs/creative-studio-spec.md -> R1.6`, seção 1 do `formato-do-pacote.md` |
| R7.1 | Nome da peça no padrão `{conceito}_{canal}_{formato}_{hook}_{legenda}_v{n}` | O `conceito` em `snake_case` sem acento vira o prefixo de todas as 12 peças | `matriz.md`, `docs/creative-studio-spec.md -> R7.1` |
| R7.2 | Duas peças do lote não repetem hook, fundo do avatar e formato de abertura ao mesmo tempo | Hooks realmente diferentes: três variações da mesma frase contam como um | `config/gates.yaml -> diversidade.combinacao_proibida` |
| R7.3 | A abertura de duas peças do mesmo conceito tem que diferir visualmente | Cada hook pede a própria direção de abertura no bloco 1 | `config/gates.yaml -> abertura.diferenca_min` |
| R7.4 | Só conceito e formato contam como diversidade; lote vizinho não repete conceito | Nomeie o ângulo da biblioteca dos 78 no `conceito.md` e não repita entre lotes | `config/gates.yaml -> diversidade.eixos_que_contam`, `.repetir_conceito_em_lote_vizinho` |
| R7.5 | Formatos sem avatar existem como opção nomeada (`sem_avatar`, `noticia`, `alerta`, `podcast_mesa`) | Escreva pelo menos um formato que funcione só com narração e inserts | `matriz.md`, `docs/creative-studio-spec.md -> R7.5` |
| decisão 27 | Cada versão nova mostra diferença VISÍVEL nos itens tocados | Variação real entre peças: tipo de inserção, formatação por insert, fundo do avatar | decisão 27 |
| decisão 36 | A peça v5.7 é a referência aprovada da skill | Use o roteiro do piloto como modelo de formato, nunca como copy a copiar | decisão 36, `piloto/insumos/roteiro.txt` |

## 9. Conteúdo que envelhece e política

| nº | o que a tela exige | consequência para a copy | onde mora |
|---|---|---|---|
| decisão 19 | Conteúdo que envelhece na tela é atenção registrada, não bloqueio | Data, preço, edição e lote numerado reprovam fora de carrinho e lote; dentro, avisam | decisão 19, seção 9 do `formato-do-pacote.md` |
| R6.4 | Oferta, prazo e preço só quando a campanha é de carrinho ou lote | Declare `campanha` no `conceito.md`: é ela que libera ou proíbe a escassez na fala | `config/modos/pago.yaml -> fechamento.oferta_no_cta` |
| R10.1 | O avatar nunca segura produto ou objeto; prova entra por insert real | Nunca escreva direção do tipo "Thales mostrando o celular": a prova é insert | `config/gates.yaml -> politica.avatar_segura_objeto`, `.prova_por_insert_real` |
| R10.2 | O roteiro do avatar carrega desfluência natural, com higienização conservadora | Escreva como se fala, com pausa e retomada; texto picotado reprova na higienização | `config/gates.yaml -> politica.desfluencia_marcada`, `.higienizacao` |
| R10.3 | Em pago com avatar, nada de claim de saúde ou renda com número insustentável, nem testemunho gerado como cliente real | Todo número da fala vem de dado autorizado no brief, com a fonte | `config/modos/pago.yaml -> politica_do_modo` |

---

## Números que a copy usa de cabeça

Conversão única: **palavras = segundos finais x 1,45 x 2,9**, ou seja, 4,205 palavras por segundo
final, sempre arredondando para cima (o teto de avatar sozinho arredonda para baixo, porque é
teto). Os 2,9 palavras por segundo foram medidos no ad21v2 (174 palavras em 60,155s de voz
natural) e o 1,45 é a decisão 23.

| o que | número | de onde sai |
|---|---|---|
| palavras por segundo de fala natural | 2,9 | medido no ad21v2, `conceito.md -> palavras_por_segundo` |
| aceleração de entrega | 1,45 | decisão 23, `config/modos/pago.yaml -> aceleracao.fator` |
| bloco com insert | mínimo 15 palavras | 3,5s finais (decisões 29 e 30) |
| bloco com KEY em placa (`h1`, `h2` ou `h4`) | mínimo 12 palavras | 2,8s finais (`permanencia_min_ms.placa`) |
| bloco com KEY em coluna ou carimbo | mínimo 15 palavras | 3,5s finais (`permanencia_min_ms.coluna`, `.carimbo`) |
| palavra do KEY além da segunda | mais 0,25s cada, ou seja, mais 2 palavras | `leitura_por_palavra_extra_ms`, `palavras_de_graca` |
| bloco com KEY em `seta_cta` | mínimo 12 palavras | 2,8s finais (`permanencia_min_ms.seta_cta`) |
| bloco de CTA | mínimo 13 palavras | 3,0s finais (`fechamento.janela_final_min_s`) |
| bloco de CTA | máximo 21 palavras (aviso) | 5,0s finais (`pago.yaml -> fechamento.janela_final_max_s`) |
| bloco de avatar sozinho | máximo 25 palavras | 6,0s finais (`retencao.avatar_sozinho_max_s`); dois vizinhos sem insert somando mais que isso avisam |
| densidade de insert por janela | 45% a 55% do tempo com insert | `retencao.densidade_insert`, a partir de 3,0s, nas janelas de corpo (3 a 15s) e fecho (15s ao fim) |
| peça inteira, pago frio e orgânico | 64 a 126 palavras | 15 a 30s finais (R6.1) |
| peça inteira, carrinho e lote | sem faixa própria | `pago.yaml -> duracao` não declara faixa; usa a de frio como referência e o número vira aviso |
| peça inteira, remarketing | 26 a 63 palavras | 6 a 15s finais (R6.1) |
| hook | até 14 palavras | 5,0s de fala natural a 2,9 p/s (`diversidade.hook_fala_max_s`) |
| âncora do hook | nas 4 primeiras palavras | 1,2s a 2,9 p/s (R2.6, `hook.problema_nomeado_ate_s`) |
| marca, reprovação | nas 3 primeiras palavras, sempre; nas 12 primeiras sem `logo_ancorado: sim` | R2.5 (as 3 palavras são regra do brief, valor de partida) |
| marca, aviso | nas 12 primeiras palavras COM `logo_ancorado: sim` | 3s finais a 1,45x (R2.5 e decisão 11) |
| frase | reprova acima de 20 palavras, avisa acima de 14 | valor de partida do brief; a R5.2 publica o bloco de legenda de 2 linhas, não o número de palavras por frase |

Estes números são os mesmos da seção 9 do `formato-do-pacote.md`: se um dia divergirem, quem
manda é o `config/gates.yaml`, e os dois arquivos se corrigem juntos.

**Nota de rodapé sobre as 2,9 palavras por segundo.** As 174 palavras do ad21v2 são contagem da
TRANSCRIÇÃO da peça entregue, não do roteiro escrito: o roteiro tem 171 palavras. A régua de 2,9
p/s carrega esse viés de cerca de 1,7% (a transcrição pega desfluência e retomada que o roteiro
não escreve), então ela mede a fala gravada com folga e o roteiro escrito com um pouco de sobra.
Quem escreve não precisa corrigir nada: os mínimos de bloco já são pisos, e o viés joga a favor
deles.

---

**Nota de rodapé sobre a numeração das decisões.** O `piloto/DECISOES.md` começa na decisão 1 e
pula direto para a 7: **as decisões de número 2 a 6 não existem no arquivo**. Elas são citadas de
passagem em outros documentos (a decisão 5, revogada pela 21, e a decisão 6, citada na seção 9 do
`formato-do-pacote.md` junto com a 19), mas o texto delas não está registrado, então nada aqui foi
deduzido a partir delas.
