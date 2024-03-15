import os
from typing import List, Dict
from models.model import Model, ModelTokenizer
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

VARIATIONS = ["claude-3-opus-20240229"]


class AnthropicAI(Model):
    def __init__(self, model: str, messages: List[Dict]):
        self.model = model
        self.messages = messages
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    def request(self, stream=False):
        try:
            self.validate_model()
            system_prompt = self.messages[0]["content"]
            self.messages.pop(0)

            return self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                temperature=0.1,
                system=system_prompt,
                messages=self.messages,
                stream=stream,
            )
        except Exception as e:
            print(e)

    def validate_model(self):
        if self.model not in VARIATIONS:
            raise ValueError("Invalid model name")

    def get_model_variations(self):
        return VARIATIONS

    def get_tokenizer(self):
        return AnthropicTokenizer(self.model)


class AnthropicTokenizer(ModelTokenizer):
    def __init__(self, anthropic):
        super().__init__(anthropic)
        self.prices_per_thousand_tokens = {}
        assert self.anthropic.model in self.prices_per_thousand_tokens, "Model not found in the price table."
        


