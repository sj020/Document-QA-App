def retrieve(query, collection, embed_model, k):
    """Retriever utility which would fetch k similar chunks from the vector-store."""
    query_embedding = embed_model.encode(query).tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )

    return results