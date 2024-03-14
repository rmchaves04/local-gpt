from typing import Dict

def get_system_prompt() -> Dict:
    print("Do you want to write a system prompt? [Y/n] (default: n)")
    prompt = input()
    if prompt.lower() == "y":
        print("Write your system prompt:")
        return {"role": "system", "content": input()}
    else:
        return get_default_prompt()

def get_default_prompt():
    content = ""

    with open("default_sys_prompt.txt") as f:
        content = f.read()

    return {"role": "system", "content": content}

def get_user_prompt() -> Dict:
    print("Do you want us to read the prompt from a file? [Y/n] (default: n)")
    read_from_file = input()
    if read_from_file.lower() == "y":
        print("Write the file name:")
        file_name = input()
        with open(file_name, "r") as f:
            return {"role": "user", "content": f.read()}
    else:
        print("=================================================")
        print("Write your user prompt:")
        return {"role": "user", "content": input()}