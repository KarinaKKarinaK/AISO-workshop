from ddgs import DDGS


def web_search(query: str) -> str:
    # web search tool
    try:
        results = DDGS().text(query, max_results=8)
        if not results:
            return "No results found."
        output = []
        for i, r in enumerate(results, 1):
            output.append(
                f"Result {i}:\n"
                f"  Title: {r['title']}\n"
                f"  URL: {r['href']}\n"
                f"  Snippet: {r['body']}"
            )
        return "\n\n".join(output)
    except Exception as e:
        return f"Search error: {e}"
