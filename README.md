# Study Tutor Agent

A GitHub + Streamlit Cloud multi-agent study system built with Streamlit, CrewAI, Gemini, Gemini Embeddings, FAISS, document extraction, deterministic calculation, and web research.

## What this is

This is intentionally **not a single chatbot**. A Manager/Orchestrator Agent routes each request to a specialist workflow:

- Teacher Agent
- Knowledge/RAG workflow
- Research Agent
- Assessment Agent
- Evaluator Agent
- Revision Agent
- Learning Planner Agent
- Case Study Agent
- Socratic Tutor Agent
- Notes Agent
- Flashcard Agent
- Exam Agent
- Quantitative/Calculator Agent

## Cloud-first design

The project is designed for GitHub → Streamlit Community Cloud. There is no requirement to run it locally and no API key is committed to the repository.

Uploaded study documents are processed in the active Streamlit session. They are not stored in the GitHub repository.

## Supported study files

PDF, DOCX, TXT, and Markdown.

## Core RAG workflow

Upload → extract → clean → overlapping chunks → Gemini embeddings → in-memory FAISS index → hybrid semantic/keyword retrieval → grounded context → specialist agent.

## Secrets

Add this in Streamlit Community Cloud → App settings → Secrets:

```toml
GEMINI_API_KEY = "YOUR_KEY"
GEMINI_MODEL = "gemini-3.8-flash"
GEMINI_EMBEDDING_MODEL = "gemini-embedding-001"
```

Do not create or commit `.streamlit/secrets.toml`.

## Deploy

1. Create a GitHub repository.
2. Upload the complete project folder contents.
3. Open Streamlit Community Cloud.
4. Connect GitHub.
5. Create app.
6. Select the repository, `main` branch, and `app.py`.
7. In Advanced settings choose Python 3.12.
8. Paste the Secrets above.
9. Deploy.

## Important

The first deployment can take several minutes because Community Cloud installs the dependencies in a cloud environment.

## Future production upgrades

For persistent learner profiles and mastery across devices, add an external database. For large permanent document collections, move the vector index to a managed vector database or managed retrieval service. The current version deliberately keeps those concerns out of the GitHub repository.
