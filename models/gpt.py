import os
from openai import OpenAI
from typing import List, Dict
from dotenv import load_dotenv
from models.model import Model

load_dotenv()


VARIATIONS = [
    "gpt-3.5-turbo-0125",
    "gpt-4",
    "gpt-4-turbo-preview",
    "gpt-4-vision-preview",
]


class GPT(Model):
    def __init__(self, model: str, messages: List[Dict]):
        self.model = model
        self.messages = messages
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def request(self, stream=False):
        try:
            self.validate_model()
            return self.client.chat.completions.create(
                model=self.model, messages=self.messages, stream=stream
            )
        except Exception as e:
            print(e)

    def validate_model(self):
        if self.model not in VARIATIONS:
            raise ValueError("Invalid model name")

    def get_model_variations(self):
        return VARIATIONS
