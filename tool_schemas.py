"""The JSON schemas the model sees.

These descriptions are effectively prompts: the model picks tools based on
them. Be precise about WHEN to use each tool and what each argument means.
The 'name' here must match a key in tools.TOOL_FUNCTIONS.
"""

TOOL_SCHEMAS = [
    {
        "name": "web_search",
        "description": (
            "Search the web for current or factual information you do not "
            "already know. Use this for recent events, statistics, "
            "definitions, or anything you would otherwise be guessing at. "
            "Returns a text summary of the top results with source URLs."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query. Keep it short and specific.",
                }
            },
            "required": ["query"],
        },
    },
    {
        "name": "read_file",
        "description": (
            "Read the contents of a local text file from disk. Use this when "
            "the user refers to a file or when you need to inspect a document "
            "on the local filesystem. Returns the file text (long files are "
            "truncated)."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Absolute or relative path to the file.",
                }
            },
            "required": ["path"],
        },
    },
]
