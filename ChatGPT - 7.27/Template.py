import os
import openai
import time

primary_key = ""
secondary_key = ""

openai.api_type = "azure"
openai.api_base = "https://api.hku.hk"
openai.api_version = "2023-03-15-preview"
openai.api_key = primary_key

def call_openai_api(prompt,temperature,max_tokens,top_p,frequency_penalty,presence_penalty,stop):
    retries = 3  # Number of times to retry on error

    for i in range(retries + 1):
        try:
            response = openai.ChatCompletion.create(
                engine="chatgpt",
                messages=[{"role": "system", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=top_p,
                frequency_penalty=frequency_penalty,
                presence_penalty=presence_penalty,
                stop=stop
            )
            return response
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            if i < retries:
                print("Retrying...")
                time.sleep(4)
            else:
                raise  # If all retries failed, raise the exception

prompt = "Give me a text to CSV file program"
temperature = 1
max_tokens = 300
top_p = 0.6
frequency_penalty = 0
presence_penalty = 0
stop = None

for i in range(3):
    start = time.time()
    response = call_openai_api(prompt,temperature,max_tokens,top_p,frequency_penalty,presence_penalty,stop)
    print(response)
    print("{} seconds".format(time.time() - start))
    print(i)
