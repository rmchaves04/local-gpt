from files import write_to_file, write_to_file_option, write_interactive_chat_to_file
from response import clean_chunk, animate_output, clean_response
from prompts import get_system_prompt, get_user_prompt
from typing import List
from models.model_factory import get_valid_models, get_ai_model

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
    model = prepare_model()
    print("=================================================")
    model.set_messages([])
    system_prompt = get_system_prompt()
    model.messages.append(system_prompt)
    print("=================================================")
    print("YOU'RE NOW STARTING INTERACTIVE CONVERSATION MODE. TYPE 'exit' TO QUIT THE PROGRAM.")
    print("=================================================")

    tokenizer = model.get_tokenizer()
    total_cost = 0

    while True:
        user_prompt = input("You: ")
        print()

        if user_prompt.lower() == "exit":
            break

        model.messages.append({"role": "user", "content": user_prompt})
        stream = model.request(stream=True)

        response = ""

        print("Assistant: ", end='')
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                chunk = clean_chunk(chunk)
                animate_output(chunk)
                response += chunk

        print('\n')

        total_cost += tokenizer.calculate_stream_cost(response)
        model.messages.append({"role": "assistant", "content": response})

    print("=================================================")
    print("Would you like to save this chatlog to a file? [Y/n] (default: n)")
    save_chatlog = input()
    if save_chatlog.lower() == "y":
        file_name = input("Write the file name: ")
        write_interactive_chat_to_file(model.model, model.messages, file_name, total_cost)
        print(f"Chatlog written to {file_name}")


    
def one_prompt_mode():
    model = prepare_model()
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
    tokenizer = model.get_tokenizer()
    print("=================================================")
    print("Generating response...")
    stream = model.request(stream=True)

    response = ""
    user_msg = messages[0].get("content") + messages[1].get("content")

    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            chunk = clean_chunk(chunk)
            animate_output(chunk)
            response += chunk

    print()

    entire_prompt = { "response": response, "user_prompt": user_msg }
    cost = tokenizer.calculate_stream_cost(entire_prompt)
    print(f"Cost: ${cost}")
    print("=================================================")

    write_to_file(model.model, response, file_name, write_to_file_flag)


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

def prepare_model():
    model_class = choose_model()
    model = model_class("", [])
    VARIATIONS = model.get_model_variations()
    print("Choose your model: ")

    model_variation = choose_model_variation(VARIATIONS)
    model.set_model(model_variation)

    return model

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

cli()
