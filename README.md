# Local GPT
This is a co-owned repository made together with [@Lorenzobattistela](https://github.com/Lorenzobattistela). Everything here is still a WIP.

Local GPT is a Python CLI that makes requests to OpenAI's models using their Python package, `openai`.

### Main features:
- Model selection
- Cost estimation using `tiktoken`
- Customizable system prompts (the default prompt is inside `default_sys_prompt.txt`)
- Reading inputs from files
- Writing outputs to files

### Installation guide
To get started using Local GPT, simply clone the repository and install the requirements.
```
pip install -r requirements.txt
```
After that, copy `.env.example` into `.env` and provide your OpenAI API key.
Finally, just run `cli.py` and get started!
> Currently only the first model (option 0) is working. Prices for the other models need to be added in `tokens.py`.

### To-do List:
- Add image input with the vision model
- Save the chat history in a txt file
- Implement replies and follow up questions in the context of the original question
