# Local GPT
This is a co-owned repository made together with [@Lorenzobattistela](https://github.com/Lorenzobattistela). Everything here is still a WIP.

Local GPT is a Python CLI and GUI tool that makes requests to OpenAI's models using their Python package, `openai`.

### Main features:
- Model selection
- Cost estimation using `tiktoken`
- Customizable system prompts (the default prompt is inside `default_sys_prompt.txt`)
- Reading inputs from files
- Writing outputs and chat logs to files
- Interactive chat mode: Ask follow up questions based on previous assistant answers, maintaining context

### Installation guide
To get started using Local GPT, simply clone the repository and install the requirements.
```
pip install -r requirements.txt
```
After that, copy `.env.example` into `.env` and provide your OpenAI API key.

### Execution guide
Navigate to the directory and simply execute either `cli.py` or `gui.py`, depending on whether you'd like to use the avaiable CLI or GUI.

### To-do List:
- Add image input with the vision model
- Save the chat history in a `.txt` file
- Add support for Anthropic models
- Add response streaming
