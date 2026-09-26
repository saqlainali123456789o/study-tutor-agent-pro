# GitHub → Streamlit Cloud Deployment

## Before upload

Make sure the repository contains `app.py` and `requirements.txt` in the root. Community Cloud executes the app from the repository root and installs Python dependencies from the dependency file.

## GitHub

1. Sign in to GitHub.
2. Create a new repository named `study-tutor-agent`.
3. Keep it empty when creating it if you are uploading these files through the browser.
4. Upload all files and folders from this project.
5. Commit to `main`.

Do not upload:

- `.env`
- `.streamlit/secrets.toml`
- API keys
- virtual environments
- generated caches

## Streamlit Community Cloud

1. Open `share.streamlit.io`.
2. Connect your GitHub account.
3. Click Create app.
4. Select repository `study-tutor-agent`.
5. Branch: `main`.
6. Main file: `app.py`.
7. Advanced settings → Python version: `3.12`.
8. Secrets:

```toml
GEMINI_API_KEY = "YOUR_KEY"
GEMINI_MODEL = "gemini-3.8-flash"
GEMINI_EMBEDDING_MODEL = "gemini-embedding-001"
```

9. Click Deploy.

## No-local workflow

You do not need Python, VS Code, Git, FAISS, or CrewAI installed on your computer. Streamlit Community Cloud creates the runtime environment from `requirements.txt`.

## Troubleshooting

### Missing GEMINI_API_KEY
Check App settings → Secrets. Do not put the key in GitHub.

### Dependency build error
Open the deployment logs. Confirm Python is 3.12 and `requirements.txt` is at the repository root.

### Gemini model error
Change `GEMINI_MODEL` in Secrets to a Gemini model available to your API account. The code does not hard-code a secret.

### Empty web search
Research requests depend on public search availability. The app will report when search is unavailable rather than inventing sources.
