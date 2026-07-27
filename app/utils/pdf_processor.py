import fitz  # PyMuPDF


def extract_text_from_pdf(file_path: str):
    """
    Extract text page by page from a PDF.

    Returns:
        list:
        [
            {
                "page_number": 1,
                "text": "..."
            },
            ...
        ]
    """

    document = fitz.open(file_path)

    pages = []

    for page_number in range(len(document)):
        page = document[page_number]

        text = page.get_text().strip()

        if text:
            pages.append(
                {
                    "page_number": page_number + 1,
                    "text": text
                }
            )

    document.close()

    return pages