"""Utility helpers for inspecting Groq API credentials."""

import os
from typing import List

from dotenv import load_dotenv
from groq import Groq


def get_available_models() -> List[str]:
    """Return the list of model identifiers available to the configured Groq API key."""
    load_dotenv()

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("Missing GROQ_API_KEY environment variable.")

    client = Groq(api_key=api_key)

    try:
        response = client.models.list()
    except Exception as exc:  # pragma: no cover - network errors
        raise RuntimeError(f"Unable to list Groq models: {exc}") from exc

    return [model.id for model in getattr(response, "data", [])]


if __name__ == "__main__":
    models = get_available_models()
    if not models:
        print("No models returned for the configured API key.")
    else:
        print("Available Groq models:")
        for model in models:
            print(f"- {model}")

