import fitz


def read_pdf(file_path: str) -> str:
    # PDF reader
    doc = fitz.open(file_path)
    pages = []
    for i, page in enumerate(doc):
        text = page.get_text()
        if text.strip():
            pages.append(f"--- Page {i + 1} ---\n{text}")
    doc.close()
    return "\n".join(pages)
