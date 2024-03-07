from openai import OpenAI
from typing import List, Dict
from dotenv import load_dotenv
from models import MODELS
import os

load_dotenv()

class GPT:

    def __init__(self, model: str, messages: List[Dict]):
        self.model = model
        self.messages = messages
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )

    def request(self):
        try:
            self.validate_model()
            return self.client.chat.completions.create(
                model=self.model,
                messages=self.messages,
                stream=True
            )
        except Exception as e:
            print(e)

    def validate_model(self):
        if self.model not in MODELS:
            raise ValueError("Invalid model name")