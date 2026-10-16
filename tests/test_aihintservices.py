import pytest
from flask import Flask

from app.services.aihintservices import AIHintService

@pytest.fixture
def app_context():
    app = Flask(__name__)
    app.config.update(
        AI_HINT_ENABLED=True,
        AI_HINT_PROVIDER="ollama",
        AI_HINT_TIMEOUT_SECONDS=15,
        OLLAMA_BASE_URL="http://localhost:11434",
        OLLAMA_MODEL="llama3.1:8b",
        OPENAI_API_KEY="test-key",
        OPENAI_MODEL="gpt-4o-mini",
    )
    with app.app_context():
        yield app

def test_generate_hint_uses_fallback_when_ai_disabled(app_context):
    question = {
        "question": "Select the domain owned by Alice",
        "question_str": "Select the domain owned by Alice",
        "choices": ["example.com", "beta.net", "zeta.org"],
        "subject": "Alice",
        "view_name": "name",
    }
    app_context.config["AI_HINT_ENABLED"] = False
    hint = AIHintService().generate_hint(question)

    assert isinstance(hint, str)
    assert len(hint) > 0

def test_generate_hint_uses_ollama_provider(monkeypatch, app_context):
    question = {
        "question": "Select the domain owned by Alice",
        "question_str": "Select the domain owned by Alice",
        "choices": ["example.com", "beta.net", "zeta.org"],
        "subject": "Alice",
        "view_name": "name",
    }

    app_context.config["AI_HINT_ENABLED"] = True
    app_context.config["AI_HINT_PROVIDER"] = "ollama"

    class FakeResponse:
        def raise_for_status(self):
            return None
        def json(self):
            return {"response": "Look for the shorter, more common domain pattern."}

    def fake_post(url, json, timeout):
        assert url == "http://localhost:11434/api/generate"
        assert json["model"] == "llama3.1:8b"
        assert "Select the domain owned by Alice" in json["prompt"]
        return FakeResponse()

    monkeypatch.setattr("app.services.aihintservices.httpx.post", fake_post)

    hint = AIHintService().generate_hint(question)

    assert hint == "Look for the shorter, more common domain pattern."

def test_generate_hint_uses_openai_provider(monkeypatch, app_context):
    question = {
        "question": "Select the domain owned by Alice",
        "question_str": "Select the domain owned by Alice",
        "choices": ["example.com", "beta.net", "zeta.org"],
        "subject": "Alice",
        "view_name": "name",
    }

    app_context.config["AI_HINT_ENABLED"] = True
    app_context.config["AI_HINT_PROVIDER"] = "openai"

    class FakeOpenAIResponse:
        output_text = "Try the option that matches a common business-style domain."

    class FakeOpenAIClient:
        def __init__(self, api_key):
            assert api_key == "test-key"

        def responses(self):
            return self

        def create(self, model, input):
            assert model == "gpt-4o-mini"
            assert "Select the domain owned by Alice" in input
            return FakeOpenAIResponse()

    monkeypatch.setattr("app.services.aihintservices.OpenAI", FakeOpenAIClient)

    hint = AIHintService().generate_hint(question)

    assert hint == "Try the option that matches a common business-style domain."

    def test_generate_hint_returns_fallback_when_no_choices(app_context):
        question = {
            "question": "Select the domain owned by Alice",
            "question_str": "Select the domain owned by Alice",
            "choices": ["example.com", "beta.net", "zeta.org"],
            "subject": "Alice",
            "view_name": "name",
        }

        app_context.config["AI_HINT_ENABLED"] = True
        app_context.config["AI_HINT_PROVIDER"] = "unknown"

        hint = AIHintService().generate_hint(question)

        assert isinstance(hint, str)
        assert len(hint)




