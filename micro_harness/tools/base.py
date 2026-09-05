from typing import Any, Callable 
#typing ajuda na detecção de erros antes de rodar.
#Any representa um valor específico, mas que pode variar.
#Callable representa uma função que pode ser chamada.


class ToolRegistry: 
    #Deve resgistrar funçoes, manter cada funçao associada a um nome, produzir schemas compatíveis com o campo tools da API do modelo, permitir que o ToolDispatcher, próximo componente, localize uma ferramenta pelo nome solicitado pelo LLM.
    def __init__(self) -> None:
        self._tools: dict[str, Callable] = {}
        self._schema: list[dict[str, Any]] = []

        