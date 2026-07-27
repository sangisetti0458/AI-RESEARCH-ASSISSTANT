from app.core.gemini_client import client
from app.utils.vector_store import collection


class CompareService:

    @staticmethod
    def compare_documents(document_id_1: int, document_id_2: int):

        results = collection.get(include=["documents", "metadatas"])

        documents = results.get("documents", [])
        metadatas = results.get("metadatas", [])

        doc1_chunks = []
        doc2_chunks = []

        document_1_name = "Unknown"
        document_2_name = "Unknown"

        for doc, metadata in zip(documents, metadatas):

            if metadata is None:
                continue

            stored_document_id = metadata.get("document_id")

            if stored_document_id == document_id_1:
                doc1_chunks.append(doc)
                document_1_name = metadata.get("file_name", "Unknown")

            elif stored_document_id == document_id_2:
                doc2_chunks.append(doc)
                document_2_name = metadata.get("file_name", "Unknown")

        if not doc1_chunks:
            raise ValueError(f"Document {document_id_1} not found.")

        if not doc2_chunks:
            raise ValueError(f"Document {document_id_2} not found.")

        context_1 = "\n\n".join(doc1_chunks)
        context_2 = "\n\n".join(doc2_chunks)

        prompt = f"""
You are an AI Research Assistant.

Compare the following two documents.

Document 1:
{context_1}

Document 2:
{context_2}

Return your answer in exactly this format:

Summary:
...

Similarities:
- ...
- ...
- ...

Differences:
- ...
- ...
- ...
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        text = response.text

        summary = ""
        similarities = []
        differences = []

        if "Similarities:" in text and "Differences:" in text:

            summary_part, remaining = text.split("Similarities:", 1)
            similarities_part, differences_part = remaining.split("Differences:", 1)

            summary = summary_part.replace("Summary:", "").strip()

            similarities = [
                line.strip("-• ")
                for line in similarities_part.splitlines()
                if line.strip()
            ]

            differences = [
                line.strip("-• ")
                for line in differences_part.splitlines()
                if line.strip()
            ]

        else:
            summary = text.strip()

        return {
            "document_1": document_1_name,
            "document_2": document_2_name,
            "summary": summary,
            "similarities": similarities,
            "differences": differences,
        }