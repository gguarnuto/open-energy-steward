# Agent

The agent arrives with the Demo release: it answers the competency questions through the MCP server, always citing sources, and proposes new terms and relations for human approval.

The review queue already exists. `propose_term` on the MCP server appends proposals to `proposals.jsonl` here, with source, rationale and an empty `decision`. A steward approves or rejects each one; only approved proposals enter the ontology, through a normal commit.
