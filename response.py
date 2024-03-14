import time

def clean_response(response):
    return response.choices[0].message.content.strip()

def clean_chunk(chunk):
    return chunk.choices[0].delta.content

def animate_output(clean_res):
    for c in clean_res:
        print(c, end="", flush=True)
        time.sleep(0.01)