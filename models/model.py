from typing import List, Dict


class Model:
    def __init__(self, model: str, messages: List[Dict]):
        self.model = model
        self.messages = messages
        self.client = self.create_client()

    def request(self):
        raise ShouldImplement

    def create_client(self):
        raise ShouldImplement

    def validate_model(self) -> bool:
        raise ShouldImplement


class ShouldImplement(Exception):
    def __init__(self):
        super().__init__("Child class should implement this method.")
