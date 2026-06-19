"""The actual tool implementations.

Each function takes simple arguments and returns a STRING. The return value
is fed straight back to the model, so it should be readable text. Errors are
returned as strings too (never raised) so the model can read them and recover.
"""

import os
import urllib.parse
import urllib.request


def web_search(query: str) -> str:
    """Search the web and return a text summary of the top results.

    This uses DuckDuckGo's free Instant Answer API so the example runs with no
    extra API key. For real use, swap in Brave, Tavily, SerpAPI, Exa, etc.
    """
    try:
        url = "https://api.duckduckgo.com/?" + urllib.parse.urlencode(
            {"q": query, "format": "json", "no_html": 1}
        )
        req = urllib.request.Request(url, headers={"User-Agent": "research-agent"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            import json

            data = json.loads(resp.read().decode())

        parts = []
        if data.get("AbstractText"):
            parts.append(f"Summary: {data['AbstractText']} (source: {data.get('AbstractURL', 'n/a')})")
        for topic in data.get("RelatedTopics", [])[:5]:
            text = topic.get("Text")
            href = topic.get("FirstURL")
            if text:
                parts.append(f"- {text} ({href})")

        if not parts:
            return f"No results found for query: {query!r}."
        return "\n".join(parts)
    except Exception as e:  # noqa: BLE001 - return errors to the model, don't crash
        return f"Error during web_search: {e}"


def read_file(path: str, max_chars: int = 8000) -> str:
    """Read a local text file and return its content (truncated)."""
    try:
        if not os.path.exists(path):
            return f"Error: file not found at path {path!r}."
        if os.path.isdir(path):
            return f"Error: {path!r} is a directory, not a file."
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read(max_chars + 1)
        if len(content) > max_chars:
            content = content[:max_chars] + "\n...[truncated]"
        return content or "(file is empty)"
    except Exception as e:  # noqa: BLE001
        return f"Error during read_file: {e}"


# Maps tool name -> callable. The orchestrator uses this to dispatch.
TOOL_FUNCTIONS = {
    "web_search": web_search,
    "read_file": read_file,
}
