import time
from replies import ask_usage_mode, format_user_prompt
from prompts import get_system_prompt, get_user_prompt
from typing import List, Tuple
from models.gpt import GPT
from tokenizer import Tokenizer
from models.model_factory import get_valid_models, get_ai_model

# TODO: historico -> salva o historico da conversa atual num txt da vida, e depois le o txt e passa como parametro para o GPT


def cli():
    print("=================================================")
    print("Welcome to GPT CLI")
    print("=================================================")

    print("Choose your usage mode")
    usage_mode = ask_usage_mode()

    if usage_mode == 1:
        one_prompt_mode()
    else:
        interactive_conversation_mode()


def interactive_conversation_mode():
    model_class = choose_model()
    model = model_class("", [])
    VARIATIONS = model.get_model_variations()
    print("Choose your model: ")
    model_variation = choose_model_variation(VARIATIONS)
    model.set_model(model_variation)
    print("=================================================")
    model.set_messages([])
    system_prompt = get_system_prompt()
    model.messages.append(system_prompt)
    print("=================================================")
    print("YOU'RE NOW STARTING INTERACTIVE CONVERSATION MODE. TYPE 'exit' TO QUIT THE PROGRAM.")
    print("=================================================")

    while True:
        user_prompt = input("You: ")
        print()

        if user_prompt.lower() == "exit":
            break

        model.messages.append({"role": "user", "content": user_prompt})
        stream = model.request(stream=True)

        response = ""

        print("GPT: ", end='')
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                chunk = clean_chunk(chunk)
                animate_output(chunk)
                response += chunk

        print('\n')

        model.messages.append({"role": "assistant", "content": response})

    exit()


    
def one_prompt_mode():
    model_class = choose_model()
    model = model_class("", [])
    VARIATIONS = model.get_model_variations()
    print("Choose your model: ")

    model_variation = choose_model_variation(VARIATIONS)
    model.set_model(model_variation)
    print("=================================================")
    write_to_file_flag, file_name = write_to_file_option()
    print("=================================================")

    messages = []

    system_prompt = get_system_prompt()
    messages.append(system_prompt)
    print("=================================================")

    user_prompt = get_user_prompt()
    messages.append(user_prompt)
    print("=================================================")

    model.set_messages(messages)
    tokenizer = None
    estimated_cost = None
    if isinstance(model, GPT):
        tokenizer = Tokenizer(model)
        print("Calculating tokens...")
        prompt_tokens = tokenizer.tokens_per_prompt()
        print(f"Prompt tokens: {prompt_tokens}")
        print("Estimating cost...")
        estimated_cost = tokenizer.estimate_cost()
        print(f"Estimated cost without response: ${estimated_cost}")
    print("=================================================")
    print("Generating response...")
    stream = model.request(stream=True)

    response = ""

    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            chunk = clean_chunk(chunk)
            animate_output(chunk)
            response += chunk

    print()

    if isinstance(model, GPT) and tokenizer and estimated_cost:
        cost = tokenizer.calculate_stream_cost(estimated_cost, response)
        print(f"Cost: ${cost}")
    print("=================================================")

    write_to_file(response, file_name, write_to_file_flag)


def ask_usage_mode():
    modes = ["One Prompt Mode", "Interactive Conversation Mode"]
    
    i = 1
    for mode in modes:
        print(f"[{i}] {mode}")
        i += 1
    mode = int(input())

    if mode < 1 or mode > len(modes):
        raise ValueError("Invalid mode")
    
    return mode


def choose_model():
    valid_models = get_valid_models()
    print("=================================")
    print("Choose a valid AI Model:\n")
    i = 1
    for model in valid_models:
        print(f"[{i}] {str(model)}")
        i += 1
    ai_choosen = int(input())
    if ai_choosen < 1 or ai_choosen > len(valid_models):
        print("Invalid choice.")
        exit()
    return get_ai_model(valid_models[ai_choosen - 1])


def choose_model_variation(variations: List[str]) -> str:
    i = 0
    for variation in variations:
        print(f"{i}. {variation}")
        i += 1

    variation = int(input("Choose a model: "))
    if variation < 0 or variation > len(variations) - 1:
        print("Invalid model")
        exit()
    print("You chose:", variations[variation])
    return variations[variation]


def write_to_file_option() -> Tuple[bool, str]:
    write_to_file_flag = False
    print("Do you want to write the response to a file? [Y/n] (default: n)")
    write_to_file = input()
    file_name = None
    if write_to_file.lower() == "y":
        write_to_file_flag = True
        print("Write the file name:")
        file_name = input()
    return write_to_file_flag, file_name


def write_to_file(response, file_name, write_to_file_flag):
    if write_to_file_flag:
        with open(file_name, "w") as f:
            f.write(response)
        print(f"Response written to {file_name}")
        clean_file(file_name)


def clean_response(response):
    return response.choices[0].message.content.strip()


def clean_chunk(chunk):
    return chunk.choices[0].delta.content


def clean_file(file_name):
    with open(file_name, "r") as file:
        lines = file.readlines()

    if lines[0].startswith("```") and lines[-1].endswith("```"):
        with open(file_name, "w") as arquivo:
            for line in lines[1:-1]:
                arquivo.write(line)
        print("File cleaned successfully")


def animate_output(clean_res):
    for c in clean_res:
        print(c, end="", flush=True)
        time.sleep(0.01)

cli()