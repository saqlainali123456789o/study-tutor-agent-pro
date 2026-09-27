import streamlit as st


APP_NAME = "Study Tutor Agent Pro"
APP_VERSION = "1.0.0"


# Current Gemini models
# Primary = strongest Flash model
# Fallback = lower-cost/high-throughput Flash-Lite model
GEMINI_MODELS = [
    "gemini-3.8-flash",
    "gemini-3.5-flash-lite",
]


EMBEDDING_MODEL = "gemini-embedding-001"


def get_gemini_api_key():
    api_key = st.secrets.get("GEMINI_API_KEY", "")

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY was not found in Streamlit Secrets."
        )

    return api_key


def get_gemini_model():
    return GEMINI_MODELS[0]


def get_embedding_model():
    return EMBEDDING_MODEL


def validate_configuration():

    try:

        api_key = get_gemini_api_key()

        if not api_key:
            return False, "GEMINI_API_KEY is missing."

        return True, "Gemini configuration is valid."

    except Exception as exc:

        return False, str(exc)
