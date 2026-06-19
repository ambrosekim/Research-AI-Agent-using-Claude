"""The agent orchestrator: the core reason -> act -> observe loop.

The model is stateless. The full `messages` list IS the agent's memory; we
pass it in its entirety on every call and append to it as we go.
"""

import anthropic

import config
from tools import TOOL_FUNCTIONS
from tool_schemas import TOOL_SCHEMAS


class ResearchAgent:
    def __init__(self):
        self.client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from env
        self.messages = []  # the conversation history == the agent's state

    def _run_tool(self, name: str, tool_input: dict) -> str:
        """Dispatch a single tool call to its implementation."""
        func = TOOL_FUNCTIONS.get(name)
        if func is None:
            return f"Error: unknown tool {name!r}."
        return func(**tool_input)

    def run(self, user_message: str) -> str:
        """Run one user turn to completion and return the final text answer."""
        self.messages.append({"role": "user", "content": user_message})

        for iteration in range(config.MAX_ITERATIONS):
            response = self.client.messages.create(
                model=config.MODEL,
                max_tokens=config.MAX_TOKENS,
                system=config.SYSTEM_PROMPT,
                tools=TOOL_SCHEMAS,
                messages=self.messages,
            )

            # Record the assistant's turn (text + any tool_use blocks) verbatim.
            self.messages.append({"role": "assistant", "content": response.content})

            # If the model didn't ask for a tool, it's done: return its text.
            if response.stop_reason != "tool_use":
                return self._extract_text(response.content)

            # Otherwise, run every tool the model requested this turn and
            # collect the results into a single user message.
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    print(f"  [tool] {block.name}({block.input})")
                    result = self._run_tool(block.name, block.input)
                    tool_results.append(
                        {
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": result,
                        }
                    )

            self.messages.append({"role": "user", "content": tool_results})

        return "Stopped: reached the maximum number of tool iterations."

    @staticmethod
    def _extract_text(content) -> str:
        """Pull the plain-text blocks out of an assistant response."""
        return "\n".join(b.text for b in content if b.type == "text").strip()
