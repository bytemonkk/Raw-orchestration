**The LLM doesn't remember that previous API call by itself. Your application sends the relevant conversation state again.**

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

**json format!!**