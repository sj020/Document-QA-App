import chromadb
from sentence_transformers import SentenceTransformer

def create_chroma_db(chunks):
    """
    Creates a collection for the chunks by creating embeddings as well.
    Using Open source model.
    """
    client = chromadb.Client()

    # Reset collection every run
    try:
        client.delete_collection("documents")
    except:
        pass

    collection = client.get_or_create_collection("documents")

    embed_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    texts = [chunk["text"] for chunk in chunks]
    embeddings = embed_model.encode(texts)

    collection.add(
        ids=[str(i) for i in range(len(texts))],
        embeddings=embeddings.tolist(),
        documents=texts,
        metadatas=[
            {"source": chunk["source"], "page": chunk["page"]}
            for chunk in chunks
        ]
    )

    return collection, embed_model

