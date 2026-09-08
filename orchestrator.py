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

while True:

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
    message = data["message"]

    print("MESSAGE:", message)

    #Did the LLM request a tool?
    if "tool_calls" in message and message["tool_calls"]:

        tool_call = message["tool_calls"][0]

        tool_name = tool_call["function"]["name"]
        arguments = tool_call["function"]["arguments"]

        print("TOOL NAME:", tool_name)
        print("ARGUMENTS:", arguments)

        if tool_name == "calculator":
            result = calculator(**arguments)

            print("TOOL RESULT:", result)

        messages.append(message)

        messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call["id"],
                "content": str(result),
            }
        )

        continue

    else:
        print("LLM RETURNED FINAL ANSWER")
        print(message["content"])
        break