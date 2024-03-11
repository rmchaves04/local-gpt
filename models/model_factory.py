from models.gpt import GPT

models = {
    "GPT": GPT,
}


def get_valid_models():
    return list(models.keys())


def get_ai_model(index):
    return models.get(index)
