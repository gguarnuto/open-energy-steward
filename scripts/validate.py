"""Validate the vocabulary: Turtle syntax, SHACL quality gates, competency question coverage.

Run: python scripts/validate.py
Exit code 1 if there are SHACL violations. Warnings are printed as a to-do list.
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml
from pyshacl import validate
from rdflib import Graph
from rdflib.namespace import OWL, RDF, SH, SKOS

ROOT = Path(__file__).resolve().parents[1]
ONTOLOGY = ROOT / "ontology" / "core.ttl"
SHAPES = ROOT / "ontology" / "shapes.ttl"
CQ_FILE = ROOT / "evals" / "competency-questions.yaml"
CQ_DIR = ROOT / "evals" / "cq"
PLACEHOLDER_NS = "https://TUO-UTENTE.github.io/open-energy-steward/ontology/core#"


def load_ontology() -> tuple[Graph, str]:
    """Parse core.ttl and return the graph with its namespace (the ontology IRI)."""
    graph = Graph().parse(ONTOLOGY)
    namespace = str(next(graph.subjects(RDF.type, OWL.Ontology)))
    return graph, namespace


def load_shapes(namespace: str) -> Graph:
    """Load the SHACL shapes, mapped to the namespace actually used in core.ttl."""
    text = SHAPES.read_text(encoding="utf-8").replace(PLACEHOLDER_NS, namespace)
    return Graph().parse(data=text, format="turtle")


def _name(graph: Graph, node) -> str:
    for label in graph.objects(node, SKOS.prefLabel):
        if label.language == "en":
            return str(label)
    return str(node).split("#")[-1]


def shacl_results(graph: Graph, namespace: str) -> tuple[list[str], list[str]]:
    """Return (violations, warnings) as readable lines."""
    _, report, _ = validate(graph, shacl_graph=load_shapes(namespace), allow_warnings=True)
    violations, warnings = [], []
    for result in report.subjects(RDF.type, SH.ValidationResult):
        focus = report.value(result, SH.focusNode)
        message = report.value(result, SH.resultMessage)
        line = f"{_name(graph, focus)}: {message}"
        if report.value(result, SH.resultSeverity) == SH.Violation:
            violations.append(line)
        else:
            warnings.append(line)
    return sorted(set(violations)), sorted(set(warnings))


def competency_questions(graph: Graph, namespace: str) -> list[tuple[str, str, int | None]]:
    """Run each competency question that has a SPARQL query: (id, question, number of answers)."""
    prefix = f"PREFIX oes: <{namespace}>\n"
    rows = []
    for cq in yaml.safe_load(CQ_FILE.read_text(encoding="utf-8")):
        query = CQ_DIR / f"{cq['id']}.rq"
        if not query.exists():
            rows.append((cq["id"], cq["question_en"], None))
            continue
        answers = len(list(graph.query(prefix + query.read_text(encoding="utf-8"))))
        rows.append((cq["id"], cq["question_en"], answers))
    return rows


def main() -> int:
    graph, namespace = load_ontology()
    violations, warnings = shacl_results(graph, namespace)

    print(f"Ontology: {ONTOLOGY.relative_to(ROOT)} ({len(graph)} triples)\n")
    print(f"Violations: {len(violations)}")
    for line in violations:
        print(f"  ✗ {line}")
    print(f"\nTo do (warnings): {len(warnings)}")
    for line in warnings:
        print(f"  • {line}")

    print("\nCompetency questions:")
    for cq_id, question, answers in competency_questions(graph, namespace):
        state = "no query yet" if answers is None else f"{answers} answer(s)"
        print(f"  {cq_id}  {state:<14} {question}")

    return 1 if violations else 0


if __name__ == "__main__":
    sys.exit(main())
