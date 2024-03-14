from typing import Tuple
from datetime import datetime

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


def write_to_file(model_name, response, file_name, write_to_file_flag):
    if write_to_file_flag:
        with open(file_name, "w") as f:
            f.write("Chatlog from " + datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
            f.write(f"\nModel: {model_name}\n")
            f.write(response)
        print(f"Response written to {file_name}")

def write_interactive_chat_to_file(model_name, messages, file_name, total_cost):
    with open(file_name, "w") as f:
        f.write("Chatlog from " + datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
        f.write(f"\nModel: {model_name}\n")
        f.write(f"SYSTEM PROMPT: {messages[0]['content']}\n\n")
        for message in messages[1:]:
            f.write(f"{message['role']}: {message['content']}\n")
        f.write(f"\n\nTotal conversation cost: {total_cost}$\n")