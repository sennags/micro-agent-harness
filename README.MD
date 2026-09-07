# Micro Harness

Um Harness simples com fins educativos. Percebi que estou estudando muito a parte teórica e quase nada da prática. Nesse projeto pretendo fazer um Harness do zero usando apenas a IA como guia, sem deixar ela codar por mim ou algo do tipo.

Meu objetivo é sair da zona de conforto, enfrentando possíveis dores de cabeça e ir aos poucos deixando o bom "vibecoding". Me aprofundando em como realmente funciona, quais chamadas, tools, vendo por dentro de como são os processos.

## Métodologia

Estou usando 2 agentes: o <b>Professor</b><i>(micro-agent-harness.md)</i> e o <b>Instrutor</b><i>(instructor.md)</i>. O professor recebe o objetivo enquanto o instrutor recebe as instruções de agir apenas como assistente, para qual usarei apenas quando tiver dúvidas "simples".

## Estrutura

Nesse sistema terá essa estrutura:
- Registry; Relaciona nomes de ferramentas às funções python
- Schema; Descrever ao modelo como solicitar cada ferramenta
- Dispatcher; Localizar e executar a função, tratando erros
- Cliente Ollama; Enviar mensagens e receber respostas
- Estado; Guardar o histórico da interação
- Engine; Coordenar o ciclo e limitar suas repetições

## Estado de estudo

<u>*Início*</u>
Como tenho conhecimento básico sobre Python, pensei que seria simples de entender o funcionamento das classes, schemas e o fluxo que o código em si vai tratar. **Mero engano**, acabei mais me atrapalhando e me atrasando tanto que só em 3/4 horas consegui compreender o que a base.py tinha que fazer. Decidi aprender primeiro como funciona o fluxo, do zero até o final. Ficando mais fácil de entender o código no meio. O que me leva a teoria novamente.