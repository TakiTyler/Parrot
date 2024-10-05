import openai
from openai import  OpenAI
import os

client = OpenAI()

messages = [
{"role": "system", "content": "You are a talking parrot companion named polly who loves to teach."},
    {"role": "user", "content": "Hello, how are you?"}
]

response = client.chat.completions.create(
        model="gpt-3.5-turbo",
    messages=messages,
    temperature=0.7,
    max_tokens=50,
)


print(response.choices[0].message.content)