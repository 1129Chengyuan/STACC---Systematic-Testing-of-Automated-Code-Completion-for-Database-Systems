import os
import openai
import time

key1 = ""
key2 = ""

openai.api_type = "azure"
openai.api_base = "https://api.hku.hk"
openai.api_version = "2023-03-15-preview"
openai.api_key = key2

key1 = "8e8db5e1ad184b9e815ee8cf55b46147"
key2 = "ce72cb6e937743debc8a5dc5a2a5db29"

#write a try: except block to retry when there is an error

# print(response)
# print("{} seconds".format(time.time() - start))
for i in range(100):
    start = time.time()
    response = openai.ChatCompletion.create(
        engine="chatgpt",
        # replace this value with the deployment name you chose when you deployed the associated model.
        messages=[{"role": "system", "content": "Give me a text to CSV file program"}],
        temperature=1,
        max_tokens=300, #the bigger the slower it is
        top_p=0.6,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None)

    time.sleep(4)

    print(response)
    # print(response["choices"][0]["message"]["content"])
    print("{} seconds".format(time.time() - start))
    print(i)