# Roadmap

Six public releases between January and October 2027. Each one has a definition of done: if time is short, the scope shrinks and the date holds.

## v0.1 · Minimal ontology · January 2027

- [ ] 3–5 public competency questions, validated
- [ ] About 30 concepts in SKOS, with Italian and English labels
- [ ] Definitions taken from public documents, each with its source
- [ ] First OWL classes and properties for markets, actors, rules and processes
- [ ] Steward and lifecycle status on every concept

**Done when** every competency question maps to concepts in the ontology and every concept has a source.

## v0.2 · Knowledge graph and MCP server · March 2027

- [ ] Corpus of public documents (ARERA resolutions, GME and Terna rules) with metadata
- [ ] LLM-assisted extraction of entities and relations, reviewed by a person
- [ ] SHACL shapes to validate the graph
- [ ] MCP server exposing concepts, definitions, relations and sources

**Done when** the competency questions can be answered by querying the graph directly.

## Demo · Agent with human approval · April 2027

- [ ] Agent answering the competency questions through the MCP server, always citing sources
- [ ] Proposals of new terms and relations, approved or rejected by a person
- [ ] Audit log of proposals and decisions
- [ ] 15 test cases: answer accuracy and human correction rate
- [ ] Governance pack: AI Act triage, OWASP checklist for agentic applications, system card
- [ ] 3-minute demo video

**Done when** the agent passes the test cases and every change to the graph has a recorded human decision.

## v0.7 · Market data with a data contract · July 2027

- [ ] Clean dataset from GME and the ENTSO-E Transparency Platform: prices, volumes, load, generation
- [ ] Data contract (ODCS) with quality checks
- [ ] The agent proposes critical data elements and data quality rules, through the same approval flow

**Done when** the quality checks run on every refresh and every proposal of the agent has a human decision.

## v0.9 · Extended evaluation · September 2027

- [ ] 50 test cases, including ambiguous and out-of-scope questions
- [ ] Prompt-injection tests on documents and inputs
- [ ] Evaluation report with error analysis

**Done when** the report is published together with the test set.

## v1.0 · Launch · October 2027

- [ ] Complete governance pack
- [ ] GraphRAG versus vector-only RAG on the same questions, with a notebook
- [ ] Article on the method and 3-minute demo video

**Done when** a newcomer can reproduce the demo from the README.

## Out of scope

- Private or confidential data of any organisation
- Production use or operational decisions
- Legal or regulatory advice
