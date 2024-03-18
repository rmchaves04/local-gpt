import os
import tiktoken
from openai import OpenAI
from typing import List, Dict
from dotenv import load_dotenv
from models.model import Model, ModelTokenizer
from response import animate_output, clean_chunk

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

    def stream_response(self, stream):
        response = ""
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                chunk = clean_chunk(chunk)
                animate_output(chunk)
                response += chunk
        return response

    def get_model_variations(self):
        return VARIATIONS

    def get_tokenizer(self):
        return GptTokenizer(self.model)


class GptTokenizer(ModelTokenizer):
    def __init__(self, gpt):
        super().__init__(gpt)
        self.prices_per_thousand_tokens = {
            "gpt-3.5-turbo-0125": {"input": 0.0005, "output": 0.0015},
            "gpt-4": {"input": 0.03, "output": 0.06},
            "gpt-4-turbo-preview": {"input": 0.01, "output": 0.03},
            "gpt-4-vision-preview": {"input": 0.01, "output": 0.03},
        }
        assert (
            self.model in self.prices_per_thousand_tokens
        ), "Model not found in the price table"
        self.encoding = self.get_encoding()

    def get_encoding(self) -> str:
        return tiktoken.encoding_for_model(self.model)

    def tokens_per_string(self, string: str) -> int:
        encoded_str = self.encoding.encode(string)
        return len(encoded_str)

    def calculate_text_cost(self, response):
        prompt_tokens = response.usage.prompt_tokens
        completion_tokens = response.usage.completion_tokens

        input_cost = (prompt_tokens / 1000) * self.prices_per_thousand_tokens[
            self.model
        ]["input"]
        output_cost = (completion_tokens / 1000) * self.prices_per_thousand_tokens[
            self.model
        ]["output"]

        total_cost = input_cost + output_cost
        return total_cost

    def calculate_stream_cost(self, response, user_prompt):
        response_tokens = self.tokens_per_string(response) + self.tokens_per_string(
            user_prompt
        )

        stream_cost = (response_tokens / 1000) * self.prices_per_thousand_tokens[
            self.model
        ]["output"]

        return stream_cost
