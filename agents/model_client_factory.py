import os
from agentopera.agents.models.openai import OpenAIChatCompletionClient

def get_shared_model_client():
    model_name = os.getenv("MODEL_NAME", "deepseek/deepseek-chat-v3-0324")
    api_key = os.getenv("MODEL_API_KEY")
    base_url = os.getenv("MODEL_BASE_URL", "https://api.tensoropera.ai/v1")

    if not all([model_name, api_key, base_url]):
        raise EnvironmentError("❌ Missing MODEL_NAME, MODEL_API_KEY, or MODEL_BASE_URL in .env")

    model_info = {
        "vision": False,
        "function_calling": True,
        "json_output": False,
        "family": "OpenAI"
    }

    return OpenAIChatCompletionClient(
        model=model_name,
        api_key=api_key,
        base_url=base_url,
        model_info=model_info
    )
