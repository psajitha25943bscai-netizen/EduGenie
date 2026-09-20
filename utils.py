# Shared helpers (Member 1 - Team Lead)
from google import genai
from google.genai import types

MODEL = "gemini-3.1-flash-lite"


def get_client(api_key: str):
    return genai.Client(api_key=api_key)


def build_config(level: str, language: str, json_output: bool = False):
    system = (
        "You are EduGenie, a friendly and patient tutor. "
        "Explain step by step with simple examples and analogies. "
        f"Student level: {level}. Reply in {language}."
    )
    if json_output:
        return types.GenerateContentConfig(
            system_instruction=system, response_mime_type="application/json"
        )
    return types.GenerateContentConfig(system_instruction=system)
