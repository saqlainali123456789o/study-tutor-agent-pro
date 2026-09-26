import os
import streamlit as st

APP_NAME = "Study Tutor Agent"
APP_VERSION = "1.0.0"
DEFAULT_GEMINI_MODEL = "gemini-3.8-flash"
DEFAULT_EMBEDDING_MODEL = "gemini-embedding-001"


def get_secret(name: str, default: str | None = None) -> str | None:
    try:
        value = st.secrets.get(name)
        if value:
            return str(value)
    except Exception:
        pass
    return os.getenv(name, default)


def get_gemini_api_key() -> str | None:
    return get_secret("GEMINI_API_KEY") or get_secret("GOOGLE_API_KEY")


def get_gemini_model() -> str:
    return get_secret("GEMINI_MODEL", DEFAULT_GEMINI_MODEL) or DEFAULT_GEMINI_MODEL


def get_embedding_model() -> str:
    return get_secret("GEMINI_EMBEDDING_MODEL", DEFAULT_EMBEDDING_MODEL) or DEFAULT_EMBEDDING_MODEL


def validate_configuration() -> tuple[bool, str]:
    if not get_gemini_api_key():
        return False, "GEMINI_API_KEY is missing. Add it in Streamlit Community Cloud → App settings → Secrets."
    return True, "Configuration ready."
