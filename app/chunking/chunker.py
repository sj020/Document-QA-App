def split_documents(documents, chunk_size=500, overlap=100):
    chunks = []

    for doc in documents:
        text = doc["text"]

        # Clean text
        text = text.replace("—", " ")
        text = " ".join(text.split())

        start = 0
        while start < len(text):
            end = start + chunk_size

            chunks.append({
                "text": text[start:end],
                "source": doc["source"],
                "page": doc["page"]
            })

            start += chunk_size - overlap

    return chunks