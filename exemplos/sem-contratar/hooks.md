# Hooks: sem_contratar

## Hook A
- id: question
- tatica: Question
- cluster: curiosidade
- cru: não
- fala: Quantos agendamentos sua clínica perdeu esse mês por mensagem que ninguém respondeu?
- ancora: quantos agendamentos
- palavras: 12
- lettering: LEAD: esse mês | KEY: QUANTOS AGENDAMENTOS
- garrafal: PERDEU
- insert: nenhum
- por que: molde "pergunta com custo" do modelo mestre. A pessoa faz a conta na cabeça e a resposta vem no bloco seguinte, que nomeia a hora em que a mensagem chega sem ninguém no celular.

## Hook B
- id: contrarian
- tatica: Contrarian
- cluster: interrupcao_padrao
- cru: não
- fala: Contratar secretária não resolve o WhatsApp da sua clínica. Sabe por quê?
- ancora: contratar secretária
- palavras: 12
- lettering: LEAD: contratar secretária | KEY: NÃO RESOLVE
- insert: nenhum
- por que: contraria a solução que a dona já pagou pra testar, e a pergunta no fim abre o corpo.

## Hook C
- id: warning
- tatica: Warning
- cluster: interrupcao_padrao
- cru: sim
- fala: Ó, o agendamento que some é o que chega quando a clínica tá fechada.
- ancora: o agendamento
- palavras: 14
- lettering: nenhum
- insert: nenhum
- por que: o hook cru, nota de voz com "Ó", sem lettering e sem apresentadora em tela. Aviso seco do mesmo mecanismo do problema.
