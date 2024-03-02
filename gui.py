from flask import Flask, render_template, request
from models import MODELS
from gpt import GPT
from tokenizer import Tokenizer

def get_default_prompt():
    content = ""

    with open("default_sys_prompt.txt") as f:
        content = f.read()

    return {
        "role": "system",
        "content": content
    }

def clean_response(response):
    return response.choices[0].message.content.strip()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', available_models = MODELS)

@app.route('/submit', methods=['POST'])
def submit():
    # get data from the form
    model = request.form.get('models')
    system_prompt = request.form.get('system_prompt')
    prompt = request.form.get('prompt')

    messages = []
    if system_prompt:
        messages.append({
            "role": "system",
            "content": system_prompt
        })
    else:
        messages.append(get_default_prompt())

    messages.append({
        "role": "user",
        "content": prompt
    })

    gpt = GPT(model, messages)
    tokenizer = Tokenizer(gpt)
    response = gpt.request()
    cost = tokenizer.calculate_text_cost(response)
    clean_res = clean_response(response)
    return render_template('submit.html', response=clean_res, cost=cost)

if __name__ == '__main__':
    app.run(debug=True)
