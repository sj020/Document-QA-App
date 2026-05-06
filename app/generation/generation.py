from retriever import retriever

def generate_answer(prompt, tokenizer, model, device):
    """Generatar utility it would generate an answer by 
    1. Tokenizing the prompt 
    2. Sending the tokenized prompt to LLM
    3. Model generate the token IDs
    4. Decode the model generated IDs
    5. Return the Answer
    """
    messages = [{"role": "user", "content": prompt}]
    text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True,
                                         enable_thinking=False)
    model_inputs = tokenizer([text], return_tensors="pt").to(device)

    generated_ids = model.generate(
        **model_inputs,
        max_new_tokens=32768)

    output_ids = generated_ids[0][len(model_inputs.input_ids[0]):].tolist()
    try:
        index = len(output_ids) - output_ids[::-1].index(151668)
    except ValueError:
        index = 0
    result = tokenizer.decode(output_ids[index:], skip_special_tokens=True).strip("\n")

    # Remove prompt from output since we have not that great of a model so sometimes LLM generate the prompt in response.
    # Just removing the prompt from the generated answer (This happens intermittantly.)
    answer = result.replace(prompt, "").strip()

    return answer

def answer_query(query, collection, embed_model, tokenizer, model, device, k=3):
    """Entry point of the pipeline where we would connect all the pieces together."""

    # Based on the user query we would fetch the results from the vector DB.
    # Result would contain the chunks and metadata for the citation
    results = retriever.retrieve(query, collection, embed_model, k)
    docs = results["documents"][0]
    metas = results["metadatas"][0]
    context = "\n\n".join(docs)
    context = context.replace("—", " ")
    context = " ".join(context.split())

    # Creating the Prompt which would have the historical context and the user query.
    prompt = f"""
    Answer the question using ONLY the context below.
    Context:
    {context}

    Question: {query}
    """

    # Passing the retrieved context and query to the LLM
    answer = generate_answer(prompt, tokenizer, model, device)
    return answer, metas