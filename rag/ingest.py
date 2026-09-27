from io import BytesIO
from pathlib import Path
import fitz
from docx import Document
from utils import chunk_text


def extract_pdf(data: bytes) -> list[dict]:
    doc = fitz.open(stream=data, filetype="pdf")
    pages = []
    for i, page in enumerate(doc):
        text = page.get_text("text") or ""
        if text.strip():
            pages.append({"page": i + 1, "text": text})
    return pages


def extract_docx(data: bytes) -> list[dict]:
    doc = Document(BytesIO(data))
    text = "\n".join(p.text for p in doc.paragraphs if p.text.strip())
    return [{"page": None, "text": text}] if text.strip() else []


def extract_plain(data: bytes) -> list[dict]:
    text = data.decode("utf-8", errors="ignore")
    return [{"page": None, "text": text}] if text.strip() else []


def extract_file(name: str, data: bytes) -> list[dict]:
    ext = Path(name).suffix.lower()
    if ext == ".pdf":
        return extract_pdf(data)
    if ext == ".docx":
        return extract_docx(data)
    if ext in {".txt", ".md"}:
        return extract_plain(data)
    raise ValueError(f"Unsupported file type: {ext}")


def build_chunks(name: str, data: bytes, chunk_size: int = 900, overlap: int = 150) -> list[dict]:
    records = []
    for page in extract_file(name, data):
        for idx, chunk in enumerate(chunk_text(page["text"], chunk_size, overlap)):
            records.append({
                "chunk_id": f"{name}:{page.get('page') or 0}:{idx}",
                "source": name,
                "page": page.get("page"),
                "text": chunk,
            })
    return records
