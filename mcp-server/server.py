"""Open Energy Steward MCP server (preview of v0.2).

Exposes the vocabulary to any MCP client, such as Claude Desktop or Claude Code:
search terms, read a term with its definition, source and lifecycle status,
and propose a new term. Proposals never touch the ontology: they go to a
review queue that a person approves or rejects.

Run: python mcp-server/server.py   (stdio transport)
"""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path

from mcp.server.mcpserver import MCPServer
from mcp.types import ToolAnnotations
from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import DCTERMS, OWL, RDF, SKOS

ROOT = Path(__file__).resolve().parents[1]
ONTOLOGY = ROOT / "ontology" / "core.ttl"
PROPOSALS = Path(os.environ.get("OES_PROPOSALS", ROOT / "agent" / "proposals.jsonl"))

graph = Graph().parse(ONTOLOGY)
OES = Namespace(str(next(graph.subjects(RDF.type, OWL.Ontology))))

server = MCPServer(
    "open-energy-steward",
    instructions=(
        "Vocabulary of the Italian electricity market and dispatching, built from public sources. "
        "Always cite the source of a definition and say when a term is still a draft. "
        "Never invent definitions: if a term is missing, propose it with propose_term and a public source."
    ),
)


def _local(node) -> str:
    return str(node).split("#")[-1] if node is not None else ""


def _terms() -> set[URIRef]:
    """Governed terms are the ones with a lifecycle status."""
    return set(graph.subjects(OES.status, None))


def _describe(term: URIRef) -> dict:
    labels = {lit.language: str(lit) for lit in graph.objects(term, SKOS.prefLabel)}
    definition = graph.value(term, SKOS.definition)
    has_definition = definition is not None and not str(definition).startswith("TODO")
    source = graph.value(term, DCTERMS.source)
    steward = graph.value(term, OES.steward)
    status = _local(graph.value(term, OES.status))
    info = {
        "id": _local(term),
        "label_it": labels.get("it", ""),
        "label_en": labels.get("en", ""),
        "alt_labels": sorted(str(alt) for alt in graph.objects(term, SKOS.altLabel)),
        "definition": str(definition) if has_definition else None,
        "source": str(source) if source is not None else None,
        "status": status,
        "steward": str(steward) if steward is not None else None,
        "broader": sorted(_local(b) for b in graph.objects(term, SKOS.broader)),
        "narrower": sorted(_local(n) for n in graph.subjects(SKOS.broader, term)),
    }
    if status != "approved" or not has_definition:
        info["caution"] = "Draft term, not yet approved by a steward: do not present it as an established definition."
    return info


@server.tool(annotations=ToolAnnotations(read_only_hint=True))
def search_terms(text: str) -> list[dict]:
    """Search the vocabulary by Italian or English label, including abbreviations such as MGP."""
    needle = text.casefold().strip()
    hits = []
    for term in _terms():
        names = list(graph.objects(term, SKOS.prefLabel)) + list(graph.objects(term, SKOS.altLabel))
        if any(needle in str(name).casefold() for name in names):
            hits.append(_describe(term))
    return sorted(hits, key=lambda t: t["label_en"])


@server.tool(annotations=ToolAnnotations(read_only_hint=True))
def get_term(term: str) -> dict:
    """Get a term by id or exact label, with definition, public source, lifecycle status and steward."""
    wanted = term.casefold().strip()
    for node in _terms():
        names = [_local(node)] + [str(n) for n in graph.objects(node, SKOS.prefLabel)]
        names += [str(n) for n in graph.objects(node, SKOS.altLabel)]
        if wanted in (name.casefold() for name in names):
            return _describe(node)
    return {"error": f"No term '{term}'. Try search_terms, or propose it with propose_term."}


@server.tool(annotations=ToolAnnotations(read_only_hint=False, destructive_hint=False))
def propose_term(
    label_it: str,
    label_en: str,
    definition: str,
    source_url: str,
    broader: str | None = None,
    rationale: str = "",
) -> dict:
    """Propose a new term for human review. It is queued, never added to the ontology directly.

    A public source URL is required: the document that defines the term.
    """
    if not source_url.startswith(("https://", "http://")):
        return {"accepted": False, "reason": "A public source URL is required."}
    record = {
        "proposed_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "proposed_by": "agent",
        "label_it": label_it,
        "label_en": label_en,
        "definition": definition,
        "source": source_url,
        "broader": broader,
        "rationale": rationale,
        "decision": None,
    }
    PROPOSALS.parent.mkdir(parents=True, exist_ok=True)
    with PROPOSALS.open("a", encoding="utf-8") as queue:
        queue.write(json.dumps(record, ensure_ascii=False) + "\n")
    return {
        "accepted": True,
        "status": "proposed",
        "next_step": "A steward reviews the proposal before it enters the ontology.",
    }


if __name__ == "__main__":
    server.run()
