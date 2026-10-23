[README.md](https://github.com/user-attachments/files/33866291/README.md)
# Open Energy Steward

**Turning knowledge about the Italian electricity market into a governed knowledge graph that people and AI agents can trust.**

Open Energy Steward is an open project built on public data only. It shows a method to capture, map and govern domain knowledge, and applies it end to end: competency questions, a minimal ontology, a knowledge graph, and an agent that answers with its sources and asks a person before changing anything.

> **Status:** v0.1 in progress, target January 2027. See the [roadmap](ROADMAP.md).

## Why

In energy companies, much of the knowledge needed to operate is tacit, held by a few experts, or scattered across regulations, market rules and documents. Newcomers take long to get up to speed, the impact of a regulatory change is hard to trace, and AI agents fed with unstructured material give answers nobody can verify.

Making knowledge AI-ready is a governance problem before it is a technology problem: every term needs a definition, a source, an owner and a lifecycle.

## What you will find here

- **A method** in five phases, driven by competency questions: [docs/method.md](docs/method.md)
- **A minimal ontology** of the Italian electricity market and dispatching, in SKOS and OWL, built from public sources: [ontology/](ontology/)
- **A knowledge graph** extracted from public documents with LLM assistance and human review (from v0.2)
- **An MCP server** exposing ontology and graph to any agent (from v0.2)
- **An agent** that answers the competency questions citing its sources and proposes new terms and relations for human approval, with an audit log (Demo)
- **A governance pack**: AI Act triage, OWASP checklist for agentic applications, system card, evaluation report: [docs/governance.md](docs/governance.md)

## Principles

1. **Start narrow, design for scale.** One domain, a model built to grow.
2. **Competency questions, not completeness.** The ontology answers the questions that matter, nothing more.
3. **Open standards.** SKOS, OWL and SHACL, so nothing is locked in.
4. **Human in the loop.** AI proposes, people approve.
5. **Governance by design.** Every element has an owner, a source and a lifecycle status.

## Competency questions (draft)

The project is scoped by a handful of questions the graph must answer. These are drafts, to be refined in v0.1:

1. Which ARERA resolutions define or change the imbalance rules, and which concepts do they affect?
2. What is the difference between MGP, MI and MSD, and who runs each market?
3. What is the current definition of a given term, and which public source does it come from?
4. If a market rule changes, which concepts, actors and obligations are affected?
5. What does a newcomer need to know to follow a market day, from bids to dispatching?

They live, with expected sources and status, in [evals/competency-questions.yaml](evals/competency-questions.yaml).

## Roadmap

| Release | Target | What ships |
| --- | --- | --- |
| v0.1 | January 2027 | Minimal ontology in SKOS and OWL, about 30 concepts, driven by the competency questions |
| v0.2 | March 2027 | Knowledge graph from public documents, served by an MCP server |
| Demo | April 2027 | Agent on the competency questions with sources and human approval, 15 test cases, governance pack, 3-minute video |
| v0.7 | July 2027 | GME and ENTSO-E dataset with a data contract; the agent proposes critical data elements and data quality rules |
| v0.9 | September 2027 | Extended evaluation: 50 test cases and prompt-injection tests |
| v1.0 | October 2027 | Governance pack, GraphRAG versus vector RAG comparison, article, demo video |

Details and definitions of done are in [ROADMAP.md](ROADMAP.md).

## Repository structure

```
open-energy-steward/
├── docs/          method, governance, sources
├── ontology/      SKOS and OWL files
├── graph/         knowledge graph build (v0.2)
├── mcp-server/    MCP server (v0.2)
├── agent/         agent and audit log (Demo)
├── evals/         competency questions, as YAML and SPARQL
├── scripts/       validation
├── tests/         quality gates run by CI
└── data/          download scripts only, no raw data
```

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python scripts/validate.py       # quality gates and competency question coverage
pytest -q                        # the same checks CI runs on every push
```

To query the vocabulary from Claude Desktop or Claude Code, see [mcp-server/](mcp-server/).

## Quality gates

Governance by design is executable here. On every push, GitHub Actions runs:

- **SHACL shapes** ([ontology/shapes.ttl](ontology/shapes.ttl)): every term needs one Italian and one English label and a lifecycle status; an approved term also needs a real definition, a public source and a steward. Drafts get the same checks as warnings, so the report doubles as a to-do list.
- **Competency questions as tests** ([evals/cq/](evals/cq/)): each question has a SPARQL query. Once the vocabulary answers it, it is added to the enforced list in [tests/test_quality.py](tests/test_quality.py), and CI keeps it answered.

The architecture is described in [docs/architecture.md](docs/architecture.md).

## Data and sources

Only public sources: ARERA, GME, Terna and the ENTSO-E Transparency Platform. Raw data is not redistributed: scripts download it from the original source, whose terms of use apply. Every concept and relation points to the document it comes from. See [docs/sources.md](docs/sources.md).

## Disclaimer

This is a personal, independent project. It uses only publicly available information and contains no data from any employer or client. It is not affiliated with or endorsed by ARERA, GME, Terna or ENTSO-E, and it is not legal or regulatory advice.

## License

Code under the Apache License 2.0 (see [LICENSE](LICENSE)). Ontology, documentation and test cases under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

## Author

Giuseppe Guarnuto, data and AI governance in energy.

## In breve, in italiano

Open Energy Steward è un progetto aperto, costruito solo su fonti pubbliche, che mostra come rendere la conoscenza di dominio pronta per l'AI: competency questions, un'ontologia minima del mercato elettrico italiano e del dispacciamento, un knowledge graph ricavato da documenti pubblici e un agente che risponde citando le fonti e chiede l'approvazione di una persona prima di modificare qualcosa. La roadmap porta alla v1.0 di ottobre 2027.
