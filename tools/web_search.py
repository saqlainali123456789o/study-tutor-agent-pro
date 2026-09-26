from ddgs import DDGS
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

class SearchInput(BaseModel):
    query: str = Field(description="A concise web research query")

class WebSearchTool(BaseTool):
    name: str = "web_search"
    description: str = "Search the public web for current or external information and return result titles, URLs, and snippets."
    args_schema = SearchInput

    def _run(self, query: str) -> str:
        try:
            results = DDGS(timeout=10).text(query, max_results=6)
            rows = []
            for r in results or []:
                rows.append(f"TITLE: {r.get('title')}\nURL: {r.get('href')}\nSNIPPET: {r.get('body')}")
            return "\n\n---\n\n".join(rows) if rows else "No web results found."
        except Exception as exc:
            return f"Web search unavailable: {exc}"
