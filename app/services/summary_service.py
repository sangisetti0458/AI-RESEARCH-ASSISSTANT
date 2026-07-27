from chromadb import PersistentClient
from app.core.gemini_client import client

# ChromaDB
chroma_client = PersistentClient(path="data/chroma")
collection = chroma_client.get_or_create_collection("documents")


class SummaryService:

    @staticmethod
    def summarize_document(document_id: int):

        results = collection.get(include=["documents", "metadatas"])

        documents = results.get("documents", [])
        metadatas = results.get("metadatas", [])

        selected_chunks = []

        for doc, metadata in zip(documents, metadatas):

            if metadata is None:
                continue

            if metadata.get("document_id") == document_id:
                selected_chunks.append(doc)

        if not selected_chunks:
            return {
                "document_id": document_id,
                "executive_summary": "Document not found.",
                "technical_summary": "",
                "bullet_point_summary": [],
                "key_takeaways": []
            }

        context = "\n\n".join(selected_chunks)

        prompt = f"""
You are an AI Research Assistant.

Summarize the following document.

Generate the response using EXACTLY the following sections.

Executive Summary:
(A short high-level overview.)

Technical Summary:
(A detailed technical explanation.)

Bullet Point Summary:
- Point 1
- Point 2
- Point 3
- Point 4
- Point 5

Key Takeaways:
- Takeaway 1
- Takeaway 2
- Takeaway 3
- Takeaway 4
- Takeaway 5

Document:

{context}

Return ONLY these sections.
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        text = response.text

        executive_summary = ""
        technical_summary = ""
        bullet_point_summary = []
        key_takeaways = []

        try:
            sections = {}

            current_section = None

            for line in text.splitlines():

                stripped = line.strip()

                if stripped.startswith("Executive Summary"):
                    current_section = "executive"
                    sections[current_section] = []

                elif stripped.startswith("Technical Summary"):
                    current_section = "technical"
                    sections[current_section] = []

                elif stripped.startswith("Bullet Point Summary"):
                    current_section = "bullet"
                    sections[current_section] = []

                elif stripped.startswith("Key Takeaways"):
                    current_section = "takeaways"
                    sections[current_section] = []

                elif current_section:
                    sections[current_section].append(stripped)

            executive_summary = "\n".join(
                sections.get("executive", [])
            ).strip()

            technical_summary = "\n".join(
                sections.get("technical", [])
            ).strip()

            bullet_point_summary = [
                item.strip("-•1234567890. ")
                for item in sections.get("bullet", [])
                if item.strip()
            ]

            key_takeaways = [
                item.strip("-•1234567890. ")
                for item in sections.get("takeaways", [])
                if item.strip()
            ]

        except Exception:

            executive_summary = text

        return {
            "document_id": document_id,
            "executive_summary": executive_summary,
            "technical_summary": technical_summary,
            "bullet_point_summary": bullet_point_summary,
            "key_takeaways": key_takeaways
        }