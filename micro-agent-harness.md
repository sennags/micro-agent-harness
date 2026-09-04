# Specification & Tutoring Guide: Micro-Agent Harness (Python Runtime)

## 1. Tutoring & Pair Programming Protocol (CRITICAL)
> **MANDATÓRIO PARA O ASSISTENTE/AGENTE EXECUTOR:**
> 1. **NÃO escreva o projeto todo de uma vez.** O objetivo é guiar o usuário na implementação do zero para desenvolvimento de habilidades.
> 2. **Abordagem Passo a Passo:** Conduza a implementação arquivo por arquivo, função por função.
> 3. **Explicação Prévia:** Antes de propor qualquer código, explique:
>    - A lógica conceitual por trás daquele componente.
>    - O motivo técnico da escolha daquela estrutura de dados, padrão ou biblioteca padrão.
>    - Como aquela parte se conecta com o restante do harness.
> 4. **Análise Linha por Linha:** Ao demonstrar snippets de código ou revisar a implementação do usuário, comente linha por linha a responsabilidade técnica de cada instrução.
> 5. **Ciclo Socrático:** Faça perguntas de validação e proponha que o usuário tente implementar pequenos blocos antes de receber a solução completa.

---

## 2. Overview
`micro-agent-harness` is a lightweight, dependency-minimal deterministic runtime built in pure Python. It orchestrates interaction between Large Language Models (LLMs) and local tools without relying on high-level orchestration frameworks (e.g., LangChain, CrewAI).

### Key Architectural Pillars
* **State & Loop Management:** Explicit `while` execution loop with state retention and strict iteration boundaries.
* **Tool Dispatcher:** Introspection-based tool registration, runtime argument validation, and invocation.
* **Error Resilience (Self-Healing):** Automatic exception capture and context reinjection for model-driven error recovery.
* **Governance:** Resource bounding via timeout thresholds, turn limits, and token tracking.

---

## 3. Directory Structure

```text
micro_harness/
├── core/
│   ├── engine.py        # Core execution loop (ReAct cycle & turn control)
│   ├── dispatcher.py    # Tool registry, signature inspection & execution
│   └── state.py         # Context memory, role-based message history & metadata
├── tools/
│   ├── base.py          # @tool decorator & JSON Schema generator
│   ├── registry.py      # Central in-memory tool repository
│   └── implementations/ # Concrete tools (HTTP fetcher, Math, System IO)
├── tests/
│   ├── test_dispatcher.py
│   └── test_engine.py
└── main.py              # CLI entry point
```

---

## 4. Core Architectural Components

### 4.1. Tool Registration & Schema Generation (`tools/base.py`)
* Uses Python's `inspect` module and type hints (`typing`) to extract function metadata and produce JSON Schemas.
* Uses the `@tool` decorator to automatically register target functions into the runtime registry.

```python
# tools/base.py contract
from typing import Callable, Any, Dict

class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, Callable] = {}
        self._schemas: list[Dict[str, Any]] = []

    def register(self, func: Callable) -> Callable:
        name = func.__name__
        self._tools[name] = func
        self._schemas.append(self._generate_schema(func))
        return func

    def _generate_schema(self, func: Callable) -> Dict[str, Any]:
        pass

    def get_tool(self, name: str) -> Callable:
        return self._tools[name]

    def get_schemas(self) -> list[Dict[str, Any]]:
        return self._schemas
```

### 4.2. Tool Dispatcher (`core/dispatcher.py`)
* Intercepts model tool calls, validates parameters, and executes the designated callable inside isolated `try/except` blocks.
* Formats execution tracebacks into structured payloads to enable model self-healing.

```python
# core/dispatcher.py execution logic
import json
import traceback
from typing import Any, Dict

class ToolDispatcher:
    def __init__(self, registry):
        self.registry = registry

    def execute(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        try:
            func = self.registry.get_tool(tool_name)
            result = func(**arguments)
            return json.dumps({"status": "success", "data": result})
        except Exception as e:
            return json.dumps({
                "status": "error",
                "error_type": type(e).__name__,
                "message": str(e),
                "traceback": traceback.format_exc()
            })
```

### 4.3. Execution Engine (`core/engine.py`)
* Coordinates the multi-turn ReAct loop (`LLM -> Tool Execution -> Observation -> Decision`).
* Implements boundary conditions (`max_turns`) and tracks token usage.

```python
# core/engine.py execution flow
class AgentEngine:
    def __init__(self, client, dispatcher, max_turns: int = 6):
        self.client = client
        self.dispatcher = dispatcher
        self.max_turns = max_turns

    def run(self, user_prompt: str) -> str:
        messages = [{"role": "user", "content": user_prompt}]
        turns = 0

        while turns < self.max_turns:
            turns += 1
            response = self.client.chat_completion(
                messages=messages,
                tools=self.dispatcher.registry.get_schemas()
            )

            if response.has_tool_calls():
                for call in response.tool_calls:
                    tool_output = self.dispatcher.execute(call.name, call.arguments)
                    messages.append({"role": "assistant", "tool_calls": [call]})
                    messages.append({"role": "tool", "name": call.name, "content": tool_output})
            else:
                return response.content

        raise TimeoutError("Agent exceeded maximum allowed execution turns.")
```

---

## 5. Implementation Roadmap

| Phase | Milestone | Concepts Learned |
| :--- | :--- | :--- |
| **Phase 1** | Schema Generator & `@tool` | Function reflection (`inspect`), Type annotations, JSON Schema standard |
| **Phase 2** | Dispatcher & Error Trapping | Runtime dispatching, exception formatting, defensive engineering |
| **Phase 3** | ReAct Engine Loop | State machines, multi-turn message lifecycles, HTTP client consumption |
| **Phase 4** | Resilience & Tests | Unit tests with `pytest`, Mock objects, edge case testing |

---

## 6. Development Rules
1. **Zero High-Level Frameworks:** Pure Python standard library + standard HTTP client (`httpx`) or official bare client.
2. **Explicit Type Annotations:** PEP 484 compliance on all internal signatures.
3. **No Hidden Logic:** Every state mutation must be inspectable and serializable.