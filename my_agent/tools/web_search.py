from io import BytesIO
import re
from urllib.parse import urlparse

import fitz
import requests
from bs4 import BeautifulSoup
from ddgs import DDGS

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
)


def _query_keywords(query: str) -> list[str]:
    words = re.findall(r"[A-Za-z0-9']+", query.lower())
    stop = {
        "the",
        "and",
        "for",
        "with",
        "from",
        "that",
        "this",
        "what",
        "which",
        "when",
        "where",
        "have",
        "has",
        "had",
        "are",
        "was",
        "were",
        "only",
        "give",
        "just",
        "name",
    }
    keywords = [w for w in words if len(w) >= 3 and w not in stop]
    return keywords[:12]


def _extract_relevant_excerpt(content: str, query: str, max_chars: int = 900) -> str:
    keywords = _query_keywords(query)
    lines = [line.strip() for line in content.splitlines() if line.strip()]
    if not lines:
        return content[:max_chars]

    scored: list[tuple[int, int]] = []
    for idx, line in enumerate(lines):
        lower = line.lower()
        score = sum(1 for keyword in keywords if keyword in lower)
        if score > 0:
            scored.append((score, idx))

    if not scored:
        return "\n".join(lines)[:max_chars]

    scored.sort(reverse=True)
    best_idx = scored[0][1]
    start = max(0, best_idx - 2)
    end = min(len(lines), best_idx + 3)
    excerpt = "\n".join(lines[start:end])
    return excerpt[:max_chars]


def web_search(query: str, max_results: int = 8) -> str:
    """Search the web and return ranked result metadata.

    Use this when you first need candidate URLs.
    """
    if max_results < 1:
        raise ValueError("max_results must be at least 1.")
    max_results = min(max_results, 5)

    with DDGS() as ddgs:
        results = ddgs.text(query, max_results=max_results)

    if not results:
        return "No search results found."

    formatted_results: list[str] = []
    for index, result in enumerate(results, start=1):
        title = result.get("title", "").strip()
        url = result.get("href", "").strip()
        snippet = result.get("body", "").strip()[:220]
        formatted_results.append(
            f"{index}. Title: {title}\nURL: {url}\nSnippet: {snippet}"
        )
    return "\n\n".join(formatted_results)


def fetch_webpage(url: str, max_chars: int = 12000) -> str:
    """Fetch and read a webpage or PDF URL.

    Use this when a question includes a URL or after selecting a search result.
    """
    if max_chars < 500:
        raise ValueError("max_chars must be at least 500.")

    parsed_url = urlparse(url)
    request_url = parsed_url._replace(fragment="").geturl()

    response = requests.get(
        request_url,
        timeout=20,
        headers={"User-Agent": USER_AGENT},
    )
    response.raise_for_status()

    content_type = response.headers.get("content-type", "").lower()
    is_pdf = "pdf" in content_type or parsed_url.path.lower().endswith(".pdf")

    if is_pdf:
        pages: list[str] = []
        with fitz.open(stream=BytesIO(response.content), filetype="pdf") as document:
            for page_number, page in enumerate(document, start=1):
                text = page.get_text("text").strip()
                if text:
                    pages.append(f"--- Page {page_number} ---\n{text}")
        if not pages:
            return "The PDF was fetched successfully, but no readable text was found."
        return "\n\n".join(pages)[:max_chars]

    soup = BeautifulSoup(response.text, "html.parser")
    for element in soup(["script", "style", "noscript"]):
        element.decompose()

    title = soup.title.string.strip() if soup.title and soup.title.string else ""
    section_text = ""
    if parsed_url.fragment:
        target = soup.find(id=parsed_url.fragment)
        if target is not None:
            section_text = target.get_text(separator="\n", strip=True)

    main = soup.find("main")
    root = main if main is not None else soup.body if soup.body is not None else soup
    text = section_text if section_text else root.get_text(separator="\n")
    cleaned_lines = [line.strip() for line in text.splitlines() if line.strip()]
    cleaned_text = "\n".join(cleaned_lines)

    if title:
        cleaned_text = f"Title: {title}\n\n{cleaned_text}"
    return cleaned_text[:max_chars]


def web_research(
    query: str,
    max_results: int = 5,
    max_chars_per_page: int = 3500,
) -> str:
    """Search and read top pages, returning focused evidence snippets.

    Use this when flash-lite needs compact evidence instead of full page dumps.
    """
    if max_results < 1:
        raise ValueError("max_results must be at least 1.")
    max_results = min(max_results, 4)

    with DDGS() as ddgs:
        results = ddgs.text(query, max_results=max_results)
    if not results:
        return "No research results found."

    sections: list[str] = []
    for index, result in enumerate(results, start=1):
        title = result.get("title", "").strip()
        url = result.get("href", "").strip()
        snippet = result.get("body", "").strip()

        section_lines = [
            f"Result {index}",
            f"Title: {title}",
            f"URL: {url}",
            f"Search Snippet: {snippet}",
        ]
        if url:
            try:
                page_content = fetch_webpage(url, max_chars=max_chars_per_page)
                evidence = _extract_relevant_excerpt(page_content, query)
                section_lines.append(f"Evidence Excerpt:\n{evidence}")
            except Exception as error:
                section_lines.append(f"Fetch Error: {error}")
        sections.append("\n".join(section_lines))

    return "\n\n".join(sections)


def count_pdf_pages_with_phrase(url: str, phrase: str) -> str:
    """Count how many pages in a PDF URL contain a phrase.

    Use this for questions like "how many pages mention X".
    """
    if not phrase.strip():
        raise ValueError("phrase must not be empty.")

    response = requests.get(
        url,
        timeout=30,
        headers={"User-Agent": USER_AGENT},
    )
    response.raise_for_status()

    content_type = response.headers.get("content-type", "").lower()
    parsed_url = urlparse(url)
    is_pdf = "pdf" in content_type or parsed_url.path.lower().endswith(".pdf")
    if not is_pdf:
        raise ValueError("The provided URL does not appear to be a PDF.")

    target = phrase.lower()
    matching_pages: list[int] = []
    with fitz.open(stream=BytesIO(response.content), filetype="pdf") as document:
        for page_number, page in enumerate(document, start=1):
            text = page.get_text("text").lower()
            if target in text:
                matching_pages.append(page_number)

    if not matching_pages:
        return "0"
    return str(len(matching_pages))
