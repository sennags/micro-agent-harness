# Guarda as funções Python e gera descrições para o Ollama

import inspect 
# Aqui ele é usado para examinar uma função sem executá-la, extrair informações sobre sua estrutura e permitir que o harness gere o contexto que será enviado ao modelo
import json 
# Aqui serve para converter valores python para json
from copy import deepcopy 
# Aqui ele apenas retorna uma cópia dos esquemas para que nada de fora possa modificá-las, mantendo a versão original
from typing import Any, Callable, get_type_hints
# Any quer dizer que tal valor pode ser de outro tipo, mas não converte
#Callable quer dizer que um valor pode ser chamado, ou seja uma função
# get_type_hints significa que ele lê o tipo de outras funções

PYTHON_TO_JSON = {str: "string", int: "integer", float: "number", bool: "boolean"}


def validate_value(name: str, value: Any, annotation: type) -> None:
    """Check supported types; bool must not count as an integer."""
    allowed = (int, float) if annotation is float else (annotation,)
    if type(value) not in allowed:
        raise TypeError(f"{name} must be {annotation.__name__}, got {type(value).__name__}")
    json.dumps(value, allow_nan=False)


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, Callable[..., Any]] = {}
        self._schemas: list[dict[str, Any]] = []

    def register(self, func: Callable[..., Any]) -> Callable[..., Any]:
        if func.__name__ in self._tools:
            raise ValueError(f"Tool already registered: {func.__name__}")
        # Validate first so an invalid function leaves no partial registration.
        schema = self._generate_schema(func)
        self._tools[func.__name__] = func
        self._schemas.append(schema)
        return func

    def _generate_schema(self, func: Callable[..., Any]) -> dict[str, Any]:
        if inspect.iscoroutinefunction(func) or inspect.isgeneratorfunction(func):
            raise TypeError("Tools must be regular synchronous functions")
        hints = get_type_hints(func)
        properties: dict[str, Any] = {}
        required: list[str] = []
        for name, parameter in inspect.signature(func).parameters.items():
            if parameter.kind not in (
                inspect.Parameter.POSITIONAL_OR_KEYWORD,
                inspect.Parameter.KEYWORD_ONLY,
            ):
                raise TypeError(f"Unsupported parameter kind: {name}")
            annotation = hints.get(name)
            if annotation not in PYTHON_TO_JSON:
                raise TypeError(f"{name} needs an annotation: str, int, float or bool")
            properties[name] = {"type": PYTHON_TO_JSON[annotation]}
            if parameter.default is inspect.Parameter.empty:
                required.append(name)
            else:
                validate_value(name, parameter.default, annotation)
                properties[name]["default"] = parameter.default
        return {
            "type": "function",
            "function": {
                "name": func.__name__,
                "description": inspect.getdoc(func) or "",
                "parameters": {
                    "type": "object",
                    "properties": properties,
                    "required": required,
                    "additionalProperties": False,
                },
            },
        }

    def get_tool(self, name: str) -> Callable[..., Any]:
        return self._tools[name]

    def get_schemas(self) -> list[dict[str, Any]]:
        return deepcopy(self._schemas)
