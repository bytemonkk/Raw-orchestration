**The LLM doesn't remember that previous API call by itself. Your application sends the relevant conversation state again.**

```text
                ┌───────────────┐
                │     Qwen      │
                │    LLM #1     │
                └───────┬───────┘
                        │
                   tool_call
                        │
                        ▼
                ┌───────────────┐
                │ Orchestrator  │
                │    (Python)   │
                └───────┬───────┘
                        │
                        ▼
                ┌───────────────┐
                │  calculator() │
                └───────┬───────┘
                        │
                       425
                        │
                        ▼
                ┌───────────────┐
                │ Orchestrator  │
                └───────┬───────┘
                        │
                   messages + 425
                        │
                        ▼
                ┌───────────────┐
                │     Qwen      │
                │    LLM #2     │
                └───────┬───────┘
                        │
                        ▼
                 "The answer is 425"
```

**json format!!**

## LLM decides

* Should I use a tool?
* Which tool?
* What arguments?

## Orchestrator controls

* Execute the tool
* Store the result
* Give the result back to LLM
* Call LLM again
* Detect final response
* Terminate the loop

**The LLM produces a response. The orchestrator interprets that response and decides whether another iteration is necessary.**

**We've completed this orchestration step. Go back and ask the LLM again.**

```text
MESSAGE: assistant + tool_calls
        ↓
TOOL NAME: calculator
        ↓
ARGUMENTS: {"expression": "25 * 17"}
        ↓
TOOL RESULT: 425
        ↓
messages updated
        ↓
LOOP → LLM again
        ↓
MESSAGE: assistant + content
        ↓
NO tool_calls
        ↓
FINAL ANSWER
        ↓
break
```

## Note it dobby!

```text
Does the LLM want another action?
        │
     ┌──┴──┐
    YES   NO
     │     │
     ▼     ▼
 execute  finish
  tool     loop
```

**That's the core agent loop.**

**So your mental model is now:**

**LLM = decision maker**

**Tools = capabilities**

**Orchestrator = execution + state + control flow**