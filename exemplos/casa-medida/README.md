# Exemplo: `casa_medida` (produto físico, formato completo)

Pacote escrito seguindo o `SKILL.md` da skill `copy-criativos`, na ordem: modelo mestre preenchido
parte a parte, sequência de papéis, planejador, tabela de blocos, redação, gate.

## 1. Modelo mestre preenchido (as 9 partes, com o produto da Casa Medida)

| parte | o que ficou | onde mora no roteiro |
|---|---|---|
| 1. abertura | molde contrária mais curiosidade: o orçamento por metro linear é o que encarece a cozinha | bloco 1 |
| 2. demonstração | antes e depois do mesmo canto da cozinha dos Souza, um insert por estado (a peça é de produto físico, então usa a seção "Demonstração quando não tem tela", forma antes e depois) | blocos 3 e 5 |
| 3. escala | "E isso ainda é só um pedaço da cozinha" | última frase do bloco 5 |
| 4. virada (mecanismo) | molde do responsável nomeado: o projeto começa pelo uso da família, com a pergunta no corpo "Quer ver o que muda?" | bloco 6 |
| 5. identificação | condicional mais prescrição, servindo de respiro entre os dois inserts | bloco 4 |
| 6. prova social | as duas únicas linhas do preset: trezentas cozinhas em Curitiba e o caso Souza (vinte por cento com o mesmo espaço útil) | bloco 7 |
| 7. ponte | molde dêitico mais acesso: "É esse desenho que eu levo pra sua casa na visita" | última frase do bloco 9 |
| 8. oferta (4 partes) | tipo de acesso "orçamento": o que é, o que será feito, o que ganha com quebra de objeção, como acessa | bloco 8 mais o CTA |
| 9. CTA | verbo de ação, objeto e lugar físico, sem escassez, sem preço, sem data (campanha frio) | bloco 10 |

## 2. Sequência de papéis e planejador

Sequência declarada: `H,D,P,I,P,M,P,O,P+T,C`.

```
python3 scripts/planejar_blocos.py --modo pago --campanha frio --formato completo \
  --papeis "H,D,P,I,P,M,P,O,P+T,C" --palavras "13,12,25,20,35,24,24,29,24,15"
```

Saída relevante: forma derivada `L,L,I,A,I,A,I,L,I,C`; capacidade de garrafais 3 blocos;
densidade de insert 50% no corpo (3 a 15s) e 53% no fecho (15s ao fim); duração 52,56s.

Um aviso do planejador ficou de pé, por decisão: "plano sem bloco O de oferta antes do CTA". O
planejador só olha o papel imediatamente anterior ao `C`, e aqui o `O` está no bloco 8, com o
`P+T` (a ponte com o insert do projeto em três dimensões) entre ele e o CTA. O gate mede a mesma
regra com janela de três blocos antes do CTA e aprova. Foi essa a escolha: manter a ponte colada
no CTA, como o método pede, e assumir o aviso do planejador.

## 3. Tabela de blocos (aprovada antes de virar roteiro)

| bloco | papel | fala | palavras | final | mínimo exigido | passa | insert | LEAD | KEY | forma |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | H | Orçamento por metro linear deixa a sua cozinha mais cara. Repara comigo aqui. | 13 | 3,09s | 2,80s (KEY em placa, 2 palavras de tempo) | sim | não | por metro linear | COZINHA CARA | placa_h2 |
| 2 | D | Você paga por metro de armário. Sobra armário fundo que ninguém alcança. | 12 | 2,85s | 2,80s | sim | não | você paga por metro | ARMÁRIO FUNDO | placa_h1 |
| 3 | P | Essa é a cozinha da família Souza antes da reforma. Armário até o teto, e a panela grande morando ali no chão da cozinha. | 24 | 5,71s | 3,75s (coluna, 3 palavras de tempo) | sim | sim | antes da reforma | PANELA NO CHÃO | coluna |
| 4 | I | Se você já pediu orçamento e saiu mais confusa, isso aqui é pra você. Olha o próximo canto comigo agora. | 20 | 4,76s | teto de 6,0s (sem insert e sem KEY) | sim | não | | | apresentadora sozinha |
| 5 | P | Aqui é o mesmo canto depois da reforma. A panela desceu pra gaveta funda, do lado do fogão. E o canto morto atrás da porta hoje é despensa. E isso ainda é só um pedaço da cozinha. | 37 | 8,80s | 3,50s (insert) e 2,80s (KEY em placa) | sim | sim | o mesmo canto | GAVETA FUNDA | placa_h2 |
| 6 | M | O projeto começa pelo que a sua família faz na cozinha. A gente mede o uso antes da parede. Quer ver o que muda? | 24 | 5,71s | teto de 6,0s (sem insert e sem KEY) | sim | não | | | apresentadora sozinha |
| 7 | P | Já são mais de trezentas cozinhas entregues aqui em Curitiba. Na dos Souza, o orçamento caiu vinte por cento, com o mesmo espaço útil. | 24 | 5,71s | 3,50s (insert) e 2,80s (KEY em placa) | sim | sim | caiu vinte por cento | ESPAÇO ÚTIL | placa_h1 |
| 8 | O | A visita técnica da Casa Medida é gratuita. Eu meço a sua cozinha e monto o projeto em três dimensões com você. O orçamento sai junto, e você decide depois. | 30 | 7,13s | 3,05s (KEY em placa, 3 palavras de tempo) | sim | não | visita técnica gratuita | PROJETO E ORÇAMENTO | placa_h4 |
| 9 | P+T | Esse é o projeto que os Souza viram na mesa da cozinha deles. É esse desenho que eu levo pra sua casa na visita. | 24 | 5,71s | 3,75s (coluna, 3 palavras de tempo) | sim | sim | esse é o projeto | DESENHO NA VISITA | coluna |
| 10 | C | Toca aqui embaixo e marca a sua visita. Eu vou até a sua cozinha com o desenho. | 17 | 4,04s | 3,00s (janela do CTA, teto 5,0s) | sim | não | toca aqui embaixo | MARCA SUA VISITA | seta_cta |

Total: 225 palavras, 53,51s finais. Formato completo (220 a 300 palavras, 52 a 71s).

Checklist de estrutura (seção 5 do `metodo-de-copy.md`), item a item: prova concreta nos blocos 3,
5 e 7; mecanismo nomeado no bloco 6; ponte apontada no bloco 9; bloco de oferta no bloco 8; gancho
combinando contrariedade mais curiosidade no bloco 1; pergunta no corpo no bloco 6.

## 4. Rodadas do gate

Comando (sem `--gates` e sem `--taticas`, ou seja, contra os limiares e o catálogo de táticas
embutidos na skill, porque não existe esteira `creative-studio` instalada neste teste):

```
python3 ~/.claude/skills/copy-criativos/scripts/gate_copy.py <pacote>
```

| rodada | reprovações | avisos | o que mudou |
|---|---|---|---|
| 1 | 2 | 2 | "no dia da medição" (fala e LEAD do bloco 3) caiu no detector de envelhecimento, que lê "dia" como data. Reescrevi o bloco 3 e o LEAD pra "antes da reforma", e a âncora do asset 1 junto |
| 2 | 0 | 2 | passou. Antes de fechar, rodei a auditoria de eco contra os arquivos da skill e achei três trechos parecidos demais com os exemplos MP dos references |
| 3 | 0 | 2 | reescrevi o hook B, a terceira frase do bloco 5, o bloco 8 inteiro e o CTA, pra sair do molde emprestado. Rodei um comparador de cinco palavras entre o meu roteiro e todos os `.md` e `.txt` da skill: zero coincidências |

Avisos que ficaram, os dois assumidos e declarados:

1. `assets.md #4: asset é imagem parada` (`drive:imagem`). A foto do projeto em três dimensões é o
   único asset parado do brief. Quem monta dá o movimento com deslize lento no próprio arquivo.
2. `roteiro: duração total fora da faixa esperada (52 a 71s contra 15 a 30s)`. Aviso previsto pelo
   próprio `SKILL.md`: a faixa de 15 a 30s é a da esteira, e o formato completo roda de 52 a 71s.
