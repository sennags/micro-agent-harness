#Descrição de uma função para a LLM puxar

{
    "type": "function",
    "function": {
        "name": "somar",
        "description": "Somar dois inteiros.",
        "parameters": {
            "type": "objetc",
            "properties": {
                "a": { "type": "integer" },
                "b": { "type": "integer" }
            },
            "required": ["a", "b"]
        }
    }
}