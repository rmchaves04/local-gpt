from typing import Tuple

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

def clean_file(file_name):
    with open(file_name, "r") as file:
        lines = file.readlines()

    if lines[0].startswith("```") and lines[-1].endswith("```"):
        with open(file_name, "w") as arquivo:
            for line in lines[1:-1]:
                arquivo.write(line)
        print("File cleaned successfully")