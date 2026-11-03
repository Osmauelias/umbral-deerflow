"""Prevent recurrence: managed OpenAI GPT-6 tools must use Responses API."""
import pytest
from deerflow.config.managed_model_providers import resolve_preset_model

@pytest.mark.parametrize("name", ["gpt-6-luna", "gpt-6-sol", "gpt-6.1-sol"])
def test_managed_openai_gpt6_uses_responses(name):
    model = resolve_preset_model("openai", name, "DUMMY_NOT_A_REAL_KEY")
    assert model["use"] == "langchain_openai:ChatOpenAI"
    assert model["use_responses_api"] is True
    assert model["output_version"] == "responses/v1"

def test_legacy_model_not_changed():
    model = resolve_preset_model("openai", "gpt-4o-mini", "DUMMY_NOT_A_REAL_KEY")
    assert "use_responses_api" not in model
