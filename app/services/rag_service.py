from sqlalchemy.orm import Session

from app.core.gemini_client import client
from app.services.conversation_service import ConversationService
from app.utils.vector_store import collection
from app.database.models import QueryLog
from app.core.logger import logger


class RAGService:

    @staticmethod
    def ask_question(
        db: Session,
        session_id: str,
        question: str,
    ):

        from app.utils.embedding_generator import model as embedding_model

        query_embedding = embedding_model.encode(question)
        logger.info(f"Question received: {question}")

        results = collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=4,
            include=["documents", "metadatas", "distances"],
        )

        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]

        context = ""

        citations = []
        retrieved_context = []

        seen = set()

        for doc, metadata in zip(documents, metadatas):

            if metadata is None:
                continue

            file_name = metadata.get("file_name")
            page_number = metadata.get("page_number")

            if file_name is None or page_number is None:
                continue

            context += (
                f"\nSource: {file_name} (Page {page_number})\n"
                f"{doc}\n"
            )

            retrieved_context.append(
                {
                    "file_name": file_name,
                    "page_number": int(page_number),
                    "content": doc,
                }
            )

            key = (file_name, page_number)

            if key not in seen:

                seen.add(key)

                citations.append(
                    {
                        "file_name": file_name,
                        "page_number": int(page_number),
                    }
                )

                query_log = QueryLog(
                    session_id=session_id,
                    question=question,
                    document_name=file_name,
                    page_number=int(page_number),
                )

                db.add(query_log)

        db.commit()

        history = ConversationService.get_history(
            db,
            session_id,
        )

        conversation = ""

        for msg in history:

            if msg.role == "user":
                conversation += f"User: {msg.message}\n"

            else:
                conversation += f"Assistant: {msg.message}\n"

        prompt = f"""
You are an AI Research Assistant.

Use the previous conversation to understand follow-up questions.

Answer ONLY using the provided document context.

Instructions:

- Never use outside knowledge.
- Use ONLY the retrieved document context.
- If the answer cannot be determined from the provided context, reply exactly:

I cannot determine the answer from the provided documents.

Conversation History:

{conversation}

Document Context:

{context}

Question:

{question}

Answer:
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        answer = response.text

        if distances:
            average_distance = sum(distances) / len(distances)
            confidence_score = round(max(0.0, 1 - average_distance), 2)
        else:
            confidence_score = 0.0

        ConversationService.save_message(
            db,
            session_id,
            "user",
            question,
        )

        ConversationService.save_message(
            db,
            session_id,
            "assistant",
            answer,
        )

        return {
            "answer": answer,
            "citations": citations,
            "confidence_score": confidence_score,
            "retrieved_context": retrieved_context,
        }