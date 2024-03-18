import os
from typing import List, Dict
from models.model import Model, ModelTokenizer
from anthropic import Anthropic
from dotenv import load_dotenv

from response import animate_output

load_dotenv()

VARIATIONS = ["claude-3-opus-20240229"]


class AnthropicAI(Model):
    def __init__(self, model: str, messages: List[Dict]):
        self.model = model
        self.messages = messages
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.usage = {}

    def request(self, stream=False):
        try:
            self.validate_model()
            msgs = self.messages.copy()
            system_prompt = msgs[0]["content"]
            msgs.pop(0)

            message = self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                temperature=0.1,
                system=system_prompt,
                messages=msgs,
                stream=stream,
            )
            return message
        except Exception as e:
            print(e)

    def stream_response(self, stream):
        response = ""
        for chunk in stream:
            if chunk.type in [
                "message_stop",
                "content_block_stop",
                "message_stop",
                "content_block_start",
            ]:
                continue

            if chunk.type == "message_start":
                self.usage["input"] = chunk.message.usage.input_tokens
                continue

            if chunk.type == "message_delta":
                self.usage["output"] = chunk.usage.output_tokens
                continue

            animate_output(chunk.delta.text)
            response += chunk.delta.text
        return response

    def validate_model(self):
        if self.model not in VARIATIONS:
            raise ValueError("Invalid model name")

    def get_model_variations(self):
        return VARIATIONS

    def get_tokenizer(self):
        return AnthropicTokenizer(self.model, self.usage)


class AnthropicTokenizer(ModelTokenizer):
    def __init__(self, anthropic, usage):
        super().__init__(anthropic)
        self.usage = usage
        self.prices_per_thousand_tokens = {
            "claude-3-opus-20240229": {"input": 0.0015, "output": 0.0075},
        }
        assert (
            self.model in self.prices_per_thousand_tokens
        ), "Model not found in the price table."

    def calculate_text_cost(self, reponse):
        pass

    def calculate_stream_cost(self, response, user_prompt):
        prices = self.prices_per_thousand_tokens[self.model]
        cost = (int(self.usage["input"]) * prices["input"]) + (
            int(self.usage["output"]) * prices["output"]
        )
        return cost
