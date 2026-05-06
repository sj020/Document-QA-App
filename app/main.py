import streamlit as st
import llm_utils
from ingestion import loader
from chunking import chunker
from vector_store import vector_store
from generation import generation

st.set_page_config(page_title="Document Q&A", layout="wide")

st.title("Document Q&A (HuggingFace + Chroma)")

uploaded_files = st.file_uploader(
    "Upload 1–3 PDF files",
    type="pdf",
    accept_multiple_files=True
)

if uploaded_files:

    if st.button("Process Documents"):

        with st.spinner("Processing documents..."):

            # Loading the uploaded documents by the user
            docs = loader.load_documents(uploaded_files)

            # Chunking the uploaded documents of the user
            chunks = chunker.split_documents(docs)

            # Creating a vector DB for those documents [Using ChromaDB]
            # We could have used FAISS or any other available vector store
            collection, embed_model = vector_store.create_chroma_db(chunks)

            # Loading the LLM from Huggingface
            # Loading the model from hugging face, not using API Keys since not having those.
            tokenizer, model, device = llm_utils.load_llm()

            # Save to session
            st.session_state.collection = collection
            st.session_state.embed_model = embed_model
            st.session_state.tokenizer = tokenizer
            st.session_state.model = model
            st.session_state.device = device
            st.session_state.processed = True

        st.success("Documents processed successfully!")


if st.session_state.get("processed", False):

    st.markdown("---")
    st.subheader(" Ask Questions")

    query = st.text_input("Enter your question")

    if st.button("Get Answer"):

        if not query.strip():
            st.warning("Please enter a question.")
        else:
            with st.spinner("Thinking..."):

                answer, sources = generation.answer_query(
                    query,
                    st.session_state.collection,
                    st.session_state.embed_model,
                    st.session_state.tokenizer,
                    st.session_state.model,
                    st.session_state.device
                )

            st.markdown("### Answer")
            st.write(answer)

            st.markdown("### Citations")

            unique_sources = set()

            for s in sources:
                key = (s["source"], s["page"])

                if key not in unique_sources:
                    st.write(f"- {s['source']} (Page {s['page']})")
                    unique_sources.add(key)