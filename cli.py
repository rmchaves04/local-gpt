import time
from models import MODELS
from gpt import GPT
from tokenizer import Tokenizer

# TODO: historico -> salva o historico da conversa atual num txt da vida, e depois le o txt e passa como parametro para o GPT

def cli():
    print("=================================================")
    print("Welcome to GPT CLI")
    print("=================================================")
    print("Choose your model: ")

    i = 0
    for model in MODELS:
        print(f"{i}. {model}")
        i += 1

    model = int(input("Choose a model: "))
    if model < 0 or model > len(MODELS) - 1:
        print("Invalid model")
        return

    print("You chose:", MODELS[model])
    model = MODELS[model]
    print("=================================================")

    write_to_file_flag = False
    print("Do you want to write the response to a file? [Y/n] (default: n)")
    write_to_file = input()
    file_name = None
    if write_to_file.lower() == "y":
        write_to_file_flag = True
        print("Write the file name:")
        file_name = input()

    messages = []
    print("Do you want to write a system prompt? [Y/n] (default: n)")
    prompt = input()
    if prompt.lower() == "y":
        print("Write your system prompt:")
        messages.append({
            "role": "system",
            "content": input()
        })
    else:
        messages.append(get_default_prompt())
    print("=================================================")
    print("Do you want us to read the prompt from a file? [Y/n] (default: n)")
    read_from_file = input()
    if read_from_file.lower() == "y":
        print("Write the file name:")
        file_name = input()
        with open(file_name, "r") as f:
            messages.append({
                "role": "user",
                "content": f.read()
            })
    else:
        print("=================================================")
        print("Write your user prompt:")
        messages.append({
            "role": "user",
            "content": input()
        })
    print("=================================================")
    gpt = GPT(model, messages)
    tokenizer = Tokenizer(gpt)
    print("Calculating tokens...")
    prompt_tokens = tokenizer.tokens_per_prompt()
    print(f"Prompt tokens: {prompt_tokens}")
    print("Estimating cost...")
    estimated_cost = tokenizer.estimate_cost()
    print(f"Estimated cost without response: ${estimated_cost}")
    print("=================================================")
    print("Generating response...")
    response = gpt.request()

    clean_res = clean_response(response)
    cost = tokenizer.calculate_text_cost(response)
    print(f"Cost: ${cost}")
    print("=================================================")
    print("Response:")
    animate_response(clean_res)

    if write_to_file_flag:
        with open(file_name, "w") as f:
            f.write(clean_res)
        print(f"Response written to {file_name}")
        clean_file(file_name)


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

def clean_file(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()

    if len(lines) > 2:
        with open(file_name, 'w') as arquivo:
            for line in lines[1:-1]:
                arquivo.write(line)
    else:
        raise ValueError("O arquivo deve ter mais de duas linhas para remover a primeira e a última.")

def animate_response(clean_res):
    for c in clean_res:
        print(c, end='', flush=True)
        time.sleep(0.01)

cli()
