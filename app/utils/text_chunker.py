from langchain_text_splitters import RecursiveCharacterTextSplitter


splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=150
)


def split_pages_into_chunks(pages):
    """
    pages = [
        {
            "page_number": 1,
            "text": "..."
        }
    ]
    """

    chunks = []

    chunk_index = 0

    for page in pages:

        page_chunks = splitter.split_text(page["text"])

        for chunk in page_chunks:

            chunks.append(
                {
                    "chunk_index": chunk_index,
                    "page_number": page["page_number"],
                    "text": chunk
                }
            )

            chunk_index += 1

    return chunks