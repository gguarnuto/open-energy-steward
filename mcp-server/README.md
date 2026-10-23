# MCP server

Preview of v0.2: an MCP server that exposes the vocabulary to Claude Desktop, Claude Code or any other MCP client.

| Tool | What it does |
| --- | --- |
| `search_terms` | Searches terms by Italian or English label, including abbreviations such as MGP |
| `get_term` | Returns a term with definition, public source, lifecycle status and steward, and warns when it is still a draft |
| `propose_term` | Queues a new term with its public source in `agent/proposals.jsonl`; it never changes the ontology |

## Run it locally

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python mcp-server/server.py      # starts on stdio, stop with Ctrl+C
```

## Connect it to Claude Desktop

In Claude Desktop open Settings, then Developer, then Edit Config, and add this to `claude_desktop_config.json`, with the absolute paths of your clone:

```json
{
  "mcpServers": {
    "open-energy-steward": {
      "command": "/path/to/open-energy-steward/.venv/bin/python",
      "args": ["/path/to/open-energy-steward/mcp-server/server.py"]
    }
  }
}
```

On Windows the command is `C:\\path\\to\\open-energy-steward\\.venv\\Scripts\\python.exe`. Quit Claude Desktop completely and reopen it, then ask: "What is the MGP in the Open Energy Steward vocabulary?". See the official guide: [Getting started with MCP on Claude for Desktop](https://support.claude.com/en/articles/10949351-getting-started-with-model-context-protocol-mcp-on-claude-for-desktop).
