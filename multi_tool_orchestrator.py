import requests


# =========================
# TOOL DEFINITIONS
# =========================

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


weather_tool = {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get the current weather for a city",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "Name of the city",
                }
            },
            "required": ["city"],
        },
    },
}


# =========================
# ACTUAL TOOL FUNCTIONS
# =========================

def calculator(expression: str):
    return eval(expression)


def get_weather(city: str):
    return f"The weather in {city} is 28°C and sunny."


# =========================
# USER MESSAGE
# =========================

messages = [
    {
        "role": "user",
        "content": "What is 25 * 17, and what is the weather in Hyderabad?",
    }
]


# =========================
# ORCHESTRATION LOOP
# =========================

while True:

    # =========================
    # LLM CALL
    # =========================

    response = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": "qwen3:4b",
            "messages": messages,
            "tools": [
                calculator_tool,
                weather_tool,
            ],
            "stream": False,
        },
    )

    data = response.json()
    message = data["message"]

    print("MESSAGE:", message)


    # =========================
    # CHECK FOR TOOL CALLS
    # =========================

    if "tool_calls" in message and message["tool_calls"]:

        # Store LLM's tool-call message
        messages.append(message)

        # =========================
        # EXECUTE ALL TOOL CALLS
        # =========================

        for tool_call in message["tool_calls"]:

            tool_name = tool_call["function"]["name"]
            arguments = tool_call["function"]["arguments"]

            print("TOOL NAME:", tool_name)
            print("ARGUMENTS:", arguments)

            if tool_name == "calculator":

                result = calculator(**arguments)

            elif tool_name == "get_weather":

                result = get_weather(**arguments)

            print("TOOL RESULT:", result)


            # =========================
            # STORE TOOL RESULT
            # =========================

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call["id"],
                    "content": str(result),
                }
            )


        # =========================
        # GO BACK TO LLM
        # =========================

        continue


    # =========================
    # FINAL ANSWER
    # =========================

    else:

        print("FINAL ANSWER:", message["content"])

        break