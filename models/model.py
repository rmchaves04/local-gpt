from typing import List, Dict


class Model:
    def __init__(self, model: str = "", messages: List[Dict] = []):
        self.model = model
        self.messages = messages
        self.client = self.create_client()

    def request(self):
        raise ShouldImplement

    def create_client(self):
        raise ShouldImplement

    def validate_model(self) -> bool:
        raise ShouldImplement

    def get_model_variations(self) -> List[str]:
        raise ShouldImplement

    def get_tokenizer(self):
        return ModelTokenizer(self.model)

    def set_model(self, model: str):
        self.model = model

    def set_messages(self, messages: List[Dict]):
        self.messages = messages

class ModelTokenizer:
    def __init__(self, model):
        self.model = model
        self.prices_per_thousand_tokens = {}

    def calculate_text_cost(self, response):
        raise ShouldImplement

    def calculate_stream_cost(self, response):
        raise ShouldImplement


class ShouldImplement(Exception):
    def __init__(self):
        super().__init__("Child class should implement this method.")
