import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    raise ValueError("Groq API Key not found!!!")

client = Groq(api_key = groq_api_key)

model = "llama-3.3-70b-versatile"

message = {
    "role": "user",
    "content": "Hi there, Groq"
}
messages = [message]

#limit the usage of tokens
response = client.chat.completions.create(model=model, messages = messages, max_tokens = 100)
answer = response.choices[0].message.content

usage = response.usage
# input tokens usage
prompt_tokens = usage.prompt_tokens
# output tokens usage
completion_tokens = usage.completion_tokens

print(f"{answer}: Input/Prompt tokens used = {prompt_tokens}, Output/Completion tokens used = {completion_tokens}, Finish reason = {response.choices[0].finish_reason}")

# If finish reason is stop means it stopped naturally but if it is length that means, the answer crossed the max_tokens we defined.

# Hello. It's nice to meet you. Is there something I can help you with, or would you like to chat?: Input/Prompt tokens used = 40, Output/Completion tokens used = 26, Finish reason = stop