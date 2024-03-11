import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

VARIATIONS = ["claude-3-opus-20240229"]


class AnthropicAI(Model):
    def __init__(self, model: str, messages: List[Dict]):
        self.model = model
        self.messages = messages
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    def request(self):
        try:
            self.validate_model()
            return self.client.messages.create(
                model=model, max_tokens=1000, temperature=0.1
            )
        except Exception as e:
            print(e)


client = anthropic.Anthropic(os.env.get("anthropic_api_key"))
message = client.messages.create(
    model="claude-3-opus-20240229",
    max_tokens=1000,
    temperature=0,
    system="You are a specialist in classic rock",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Name the top 5 best selling classic rock bands of all time",
                }
            ],
        }
    ],
)
print(message.content)
