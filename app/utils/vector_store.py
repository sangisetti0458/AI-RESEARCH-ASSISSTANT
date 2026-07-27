import chromadb

client = chromadb.PersistentClient(path="data/chroma")

collection = client.get_or_create_collection(
    name="documents"
)


def store_embeddings(document_id, file_name, chunks, embeddings):

    ids = []
    documents = []
    metadatas = []

    for chunk, embedding in zip(chunks, embeddings):

        ids.append(f"{document_id}_{chunk['chunk_index']}")

        documents.append(chunk["text"])

        metadatas.append(
            {
                "document_id": document_id,
                "file_name": file_name,
                "page_number": chunk["page_number"],
                "chunk_index": chunk["chunk_index"]
            }
        )

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings.tolist(),
        metadatas=metadatas
    )


def delete_embeddings(document_id: int):
    """
    Delete all embeddings belonging to a document.
    """

    collection.delete(
        where={
            "document_id": document_id
        }
    )