# AI Hint Service

> Note: this document was AI-generated with human review.

## Overview

The `AIHintService` provides short, safe hints for the domain-matching game without revealing the correct answer outright. The service is designed to be flexible: it can use a local Ollama model, an external OpenAI-compatible API, or a deterministic fallback hint when AI is disabled or unavailable.

This keeps the game playable even if the AI provider is down or not configured.

## Purpose in the app

The hint flow is tied to the current game round. Each rendered question is stored with a `question_id`, and the hint endpoint looks up the active question to generate a hint that matches that exact round.

This prevents stale hints from previous questions and keeps the user experience consistent.

## Current design

The service is implemented in `app/services/aihintservices.py` and can be used like this in a Python example:

```python
from app.services.aihintservices import AIHintService

question = {
    "question": "Select the domain owned by Alice",
    "question_str": "Select the domain owned by Alice",
    "choices": ["example.com", "beta.net", "zeta.org"],
    "subject": "Alice",
    "view_name": "name",
}

hint = AIHintService().generate_hint(question)
print(hint)
```

The `generate_hint()` method does the following:

1. Checks whether AI hints are enabled in the app config.
2. Chooses the configured provider:
   - `ollama`
   - `openai`
   - `none`
3. Calls the selected provider.
4. Falls back to a deterministic hint if the provider fails or is disabled.

## Provider options

### Option A: Ollama

Ollama is the preferred local option for privacy-conscious setups.

Required config values:

```python
AI_HINT_ENABLED = True
AI_HINT_PROVIDER = "ollama"
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_MODEL = "llama3.1:8b"
AI_HINT_TIMEOUT_SECONDS = 15
```

Typical setup:

```bash
ollama pull llama3.1:8b
ollama serve
```

The Ollama path uses the `/api/generate` endpoint and passes a tightly constrained prompt that asks for a short hint without revealing the answer.

### Option B: OpenAI

OpenAI is useful when you want higher-quality hint wording without running a local model.

Required config values:

```python
AI_HINT_ENABLED = True
AI_HINT_PROVIDER = "openai"
OPENAI_API_KEY = "your-api-key"
OPENAI_MODEL = "gpt-4o-mini"
AI_HINT_TIMEOUT_SECONDS = 15
```

The OpenAI path calls the model and returns the generated response text as the hint.

## Fallback behavior

The fallback is intentionally simple and safe. It uses the current question data to produce a generic hint that helps without revealing the correct answer.

Example fallback output:

- "Compare the length and style of the choices before guessing."
- "Focus on the wording of the prompt and eliminate the least likely choices."

This ensures the game remains usable even when AI is temporarily unavailable.

## Security and safety expectations

The hint prompt is constrained to:

- avoid revealing the correct answer directly
- avoid quoting the exact answer text
- avoid exposing hidden indexes or scoring logic
- stay brief and helpful

This keeps the hint feature supportive without trivializing the game.

## Recommended configuration pattern

The app should keep provider selection in `app/config.py` instead of hardcoding a model in the service itself. That allows the same code path to support:

- local AI via Ollama
- cloud AI via OpenAI
- no AI at all with deterministic fallbacks

## Typical usage flow

1. The user clicks **Get Question**.
2. The current question is generated and stored with a `question_id`.
3. The user clicks **Get Hint**.
4. The browser sends the `question_id` to the route.
5. The route looks up the current question in cache.
6. `AIHintService.generate_hint()` builds a hint.
7. The frontend renders the hint below the question.

## Summary

The AI hint feature is a safety-oriented enhancement to the game: it improves the experience without making the game trivial. The service is designed to be configurable, resilient, and safe by default, with a local deterministic fallback whenever AI is unavailable.
