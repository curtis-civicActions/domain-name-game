import json
from typing import Any

import httpx
from flask import current_app
from openai import OpenAI

class AIHintService:
    def generate_hint(self, question: dict[str, Any]) -> str:
        """
        Generate a hint based on the provided question

        Uses  deterministic hints if
        - AI is disabled
        - provider is unknown
        - provider call fails:
        """
        if not current_app.config.get("AI_HINT_ENABLED", False):
            return self._fallback_hint(question)

        provider = current_app.config.get("AI_HINT_PROVIDER", "none")

        try:
            if provider == "ollama":
                return self._generate_with_ollama(question)
            if provider == "openai":
                return self._generate_with_openai(question)
        except Exception:
            return self._fallback_hint(question)

        return self._fallback_hint(question)


    def _build_prompt(self, question: dict[str, Any]) -> str:
        """
        Build a tightly constrained prompt so the model gives a hint
        without giving away the answer.
        """
        payload = {
            "question": question.get("question_str"),
            "choices": question.get("choices", []),
            "subject": question.get("subject"),
            "mode": question.get("view_name", "unknown"),
        }

        return (
            "You are helping a player in a domain-matching game.\n"
            "Write exactly one short hint sentence that helps the player answer the question.\n"
            "Rules:\n"
            "- Do not reveal the correct answer directly.\n"
            "- Do not quote the correct choice verbatim.\n"
            "- Do not mention the internal indexes or scoring.\n"
            "= Keep it under 20 words.\n"
            "- Keep it useful but subtle.\n"
            f"Game data:\n{json.dumps(payload)}"
        )


    def _generate_with_ollama(self, question: dict[str, Any]) -> str:
        base_url = current_app.config["OLLAMA_BASE_URL"].rstrip("/")
        model = current_app.config["OLLAMA_MODEL"]
        timeout = current_app.config["AI_HINT_TIMEOUT_SECONDS"]
        prompt = self._build_prompt(question)

        response = httpx.post(
            f"{base_url}/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
            },
            timeout=timeout,
        )

        response.raise_for_status()
        data = response.json()
        hint = (data.get("response") or "").strip()

        if not hint:
            return self._fallback_hint(question)

        return hint


    def _generate_with_openai(self, question: dict[str, Any]) -> str:
        api_key = current_app.config["OPENAI_API_KEY"]
        model = current_app.config["OPENAI_MODEL"]
        prompt = self._build_prompt(question)

        client = OpenAI(api_key=api_key)

        response = client.responses.create(
            model=model,
            input=prompt,
        )

        hint = (response.output_text or "").strip()
        return hint or self._fallback_hint(question)


    def _fallback_hint(self, question: dict[str, Any]) -> str:
        """
        Generate a fallback hint based on the question data.
        This is used when AI hint generation is disabled or fails.
        """
        choices = question.get("choices", [])
        if not choices:
            return "Try comparing the answer choices carefully."

        shortest = min(choices, key=len)
        longest = max(choices, key=len)

        if shortest != longest:
            return "Compare the length and style of the choices before guessing."

        return "Focus on the wording of the prompt and eliminate the least likely choices."
