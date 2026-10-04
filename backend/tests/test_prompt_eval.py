"""
Pytest integration for the Prompt Evaluation & Guardrail Harness.
"""

import pytest
from app.voice.eval_prompts import PromptEvalHarness, SCENARIOS


@pytest.mark.asyncio
async def test_prompt_eval_all_scenarios_pass():
    """Verify all defined voice personas & edge-case scenarios pass prompt evaluation."""
    harness = PromptEvalHarness(is_live=False)
    results = await harness.run_all()

    assert len(results) == len(SCENARIOS)

    failed = [r for r in results if not r.passed]
    if failed:
        failure_details = "\n".join(
            f"- {f.scenario.id} ({f.scenario.name}): {f.feedback}" for f in failed
        )
        pytest.fail(f"Prompt evaluation failed on {len(failed)} scenario(s):\n{failure_details}")


@pytest.mark.asyncio
async def test_guardrail_prevents_unauthorized_discount():
    """Verify specifically that aggressive discount haggling cannot breach guardrails."""
    harness = PromptEvalHarness(is_live=False)
    scen_01 = next(s for s in SCENARIOS if s.id == "SCEN-01")
    result = await harness.run_scenario(scen_01)

    assert result.scores["guardrails"] is True
    assert result.scores["intent_compliance"] is True
