import requests


calculator_tool = {
    "type": "function",
    "function": {
        "name": "calculator",
        "description": "Calculate a mathematical expression",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "Mathematical expression to calculate",
                }
            },
            "required": ["expression"],
        },
    },
}

messages = [
    {
        "role": "user",
        "content": "What is 25 * 17?",
    }
]

def calculator(expression: str):
    return eval(expression)

response = requests.post(
    "http://localhost:11434/api/chat",
    json={
        "model": "qwen3:4b",
        "messages": messages,
        "tools": [calculator_tool],
        "stream": False,
    },
)


data = response.json()

tool_call = data["message"]["tool_calls"][0]

tool_name = tool_call["function"]["name"]
arguments = tool_call["function"]["arguments"]

if tool_name == "calculator":
    result = calculator(**arguments)
    print("TOOL RESULT:", result)

message = data["message"]

print("ROLE:", message["role"])
print("CONTENT:", message["content"])
print("TOOL CALLS:", message["tool_calls"])