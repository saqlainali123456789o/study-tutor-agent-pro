from crewai.tools import BaseTool
from ddgs import DDGS


class WebSearchTool(BaseTool):
    name: str = "web_search"

    description: str = (
        "Search the web for current or external information. "
        "Use this tool when the student needs recent information, "
        "research evidence, academic information, or information "
        "not available in the supplied study material."
    )

    def _run(self, query: str) -> str:
        """Search the web and return concise results."""

        if not query or not query.strip():
            return "No search query was provided."

        try:
            results = []

            with DDGS() as ddgs:
                search_results = ddgs.text(
                    query.strip(),
                    max_results=5,
                )

                for item in search_results:
                    title = item.get("title", "")
                    url = item.get("href", "")
                    body = item.get("body", "")

                    if title or url or body:
                        results.append(
                            f"Title: {title}\n"
                            f"URL: {url}\n"
                            f"Summary: {body}"
                        )

            if not results:
                return "No web sources were found."

            return "\n\n".join(results)

        except Exception as exc:
            return f"Web search error: {exc}"
