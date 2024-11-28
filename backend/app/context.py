import os
from llama_index import ServiceContext
from llama_index.llms import OpenAI

def create_base_context():
    # Get model name from the environment variable (default to 'gpt-4' if not set)
    model = os.getenv("MODEL", "gpt-4")

    # Ensure the model is either 'gpt-4' or 'gpt-3.5-turbo'
    if model not in ["gpt-4", "gpt-3.5-turbo"]:
        raise ValueError("Invalid model specified. Please choose either 'gpt-4' or 'gpt-3.5-turbo'.")

    return ServiceContext.from_defaults(
        llm=OpenAI(model=model),
    )
