# Micro Harness

Um Harness simples com fins educativos. Meu objetivo é sair da zona de conforto, enfrentando possíveis dores de cabeça e ir aos poucos deixando o bom "vibecoding". Me aprofundando em como realmente funciona, vendo por dentro de como são os processos.

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