from typing import Dict, List
from functools import reduce
from gpt import GPT
import tiktoken
import openai

# TODO: add other models token pricing

class Tokenizer:
    def __init__(self, gpt: GPT):
        self.gpt = gpt
        self.encoding = self.get_encoding()
        self.prices_per_thousand_tokens = {
            "gpt-4-0125-preview": {"input": 0.01, "output": 0.03},
            "gpt-4-1106-preview": {"input": 0.01, "output": 0.03},
            "gpt-4-1106-vision-preview": {"input": 0.01, "output": 0.03},
        }
        assert self.gpt.model in self.prices_per_thousand_tokens, "Model not found in the price table."

    def get_encoding(self) -> str:
        return tiktoken.encoding_for_model(self.gpt.model)

    def tokens_per_string(self, string: str) -> int:
        encoded_str = self.encoding.encode(string)
        return len(encoded_str)

    def tokens_per_prompt(self) -> int:
        return reduce(lambda x, y: x + y, map(lambda x: self.tokens_per_string(x.get("content")), self.gpt.messages))

    def calculate_text_cost(self, response: openai.types.Completion) -> float:
        prompt_tokens = response.usage.prompt_tokens
        completion_tokens = response.usage.completion_tokens

        input_cost = (prompt_tokens / 1000) * self.prices_per_thousand_tokens[self.gpt.model]["input"]
        output_cost = (completion_tokens / 1000) * self.prices_per_thousand_tokens[self.gpt.model]["output"]

        total_cost = input_cost + output_cost
        return total_cost

    def estimate_cost(self):

        return (self.tokens_per_prompt() / 1000) * self.prices_per_thousand_tokens[self.gpt.model]["input"]
