from models.gpt import GPT
from models.anthropic import AnthropicAI

models = {"GPT": GPT, "Anthropic": AnthropicAI}


def get_valid_models():
    return list(models.keys())


def get_ai_model(index):
    return models.get(index)
