from flask import Flask, render_template, request
from models.gpt import GPT, MODELS
from tokenizer import Tokenizer


def get_default_prompt():
    content = ""

    with open("default_sys_prompt.txt") as f:
        content = f.read()

    return {"role": "system", "content": content}


def clean_response(response):
    return response.choices[0].message.content.strip()


def build_history_prompt(prompt):
    contents = [msg.get("content") for msg in message_history]
    return f"This is the history of the last prompts and responses. Use it to get a better understanding of the conversation and answer the next question.{','.join(contents)}\n\n Prompt: {prompt}"


app = Flask(__name__)

message_history = []


@app.route("/")
def index():
    return render_template(
        "index.html", available_models=MODELS, message_history=message_history
    )


@app.route("/clean-history")
def clean_history():
    message_history = []
    return render_template(
        "index.html", available_models=MODELS, message_history=message_history
    )


@app.route("/submit", methods=["POST"])
def submit():
    # get data from the form
    model = request.form.get("models")
    system_prompt = request.form.get("system_prompt")
    prompt = request.form.get("prompt")
    history = request.form.get("history")

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    else:
        messages.append(get_default_prompt())

    if history:
        messages.append(
            {"role": "system", "content": build_history_prompt(prompt)})
    else:
        messages.append({"role": "user", "content": prompt})

    message_history.append({"sender": "You", "content": prompt})

    gpt = GPT(model, messages)
    tokenizer = Tokenizer(gpt)
    response = gpt.request()
    cost = tokenizer.calculate_text_cost(response)
    clean_res = clean_response(response)
    message_history.append({"sender": "GPT", "content": clean_res})
    return render_template(
        "submit.html", response=clean_res, cost=cost, message_history=message_history
    )


if __name__ == "__main__":
    app.run(debug=True)
