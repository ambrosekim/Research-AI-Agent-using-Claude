# Research Agent — single-agent starter

A minimal, working AI agent: one reasoning loop, two tools (web search + file
read). No framework — just the Anthropic SDK so you can see the whole machine.

## Setup

```bash
pip install anthropic
export ANTHROPIC_API_KEY=sk-ant-...   # your key
python main.py
```

Then type a question, e.g. `What is the capital of Kenya?` or
`read ./config.py and tell me the max iteration count`.

## Files

| File              | Role                                                      |
|-------------------|-----------------------------------------------------------|
| `main.py`         | CLI entry point / chat loop                               |
| `agent.py`        | The orchestrator — the reason→act→observe loop + memory   |
| `tools.py`        | The actual tool functions (return strings, never raise)   |
| `tool_schemas.py` | The JSON schemas the model sees (these double as prompts) |
| `config.py`       | Model name, iteration cap, system prompt                  |

## How it works

The model is stateless. `agent.messages` is the entire memory; it's passed in
full on every API call. Each turn the model either returns text (done) or
requests a `tool_use`. On a tool request the orchestrator runs the function,
appends a `tool_result`, and calls the model again — until it answers or hits
`MAX_ITERATIONS`.

## Extend it next

1. Add a third tool (a real search API like Tavily/Brave; a calculator).
2. Add streaming so answers print token-by-token.
3. Add evals: a set of questions + expected qualities, scored automatically.
4. Add persistent memory so it remembers across sessions.
