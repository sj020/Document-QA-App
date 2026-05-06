import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# Loading the Tokenizer, Model and return the device it can be run
# Currently, for windows machine it would run in CPU only
def load_llm():
    """Utility method for loading the tokenizer, model and the device on which the model would run"""
    model_name = "Qwen/Qwen3-0.6B"
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype="auto", trust_remote_code=True)

    device = "mps" if torch.backends.mps.is_available() else "cpu"
    model = model.to(device)

    return tokenizer, model, device