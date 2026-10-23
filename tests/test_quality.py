"""Quality gates run by CI: syntax, SHACL, enforced competency questions."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import validate  # noqa: E402

# Add a competency question here once the vocabulary answers it (e.g. "CQ3"):
# from then on, CI fails if a change makes it unanswerable again.
ENFORCED: list[str] = []


def test_ontology_parses():
    graph, namespace = validate.load_ontology()
    assert len(graph) > 0
    assert namespace


def test_no_shacl_violations():
    graph, namespace = validate.load_ontology()
    violations, _ = validate.shacl_results(graph, namespace)
    assert not violations, "\n".join(violations)


@pytest.mark.parametrize("cq_id", ENFORCED)
def test_enforced_competency_question(cq_id):
    graph, namespace = validate.load_ontology()
    answers = {cq: n for cq, _, n in validate.competency_questions(graph, namespace)}
    assert answers.get(cq_id), f"{cq_id} has no answers in the vocabulary"
