import requests
import html2text


def fetch_webpage(url: str) -> str:
    # fetching. web pages
    try:
        response = requests.get(
            url,
            timeout=15,
            headers={"User-Agent": "Mozilla/5.0 (compatible; research-agent/1.0)"},
        )
        response.raise_for_status()

        converter = html2text.HTML2Text()
        converter.ignore_links = False
        converter.ignore_images = True
        converter.body_width = 0
        text = converter.handle(response.text)

        # Truncate to ~15000 chars to avoid context overflow
        if len(text) > 15000:
            text = text[:15000] + "\n\n... [TRUNCATED — page too long, search for more specific terms if needed]"
        return text
    except Exception as e:
        return f"Error fetching page: {e}"
