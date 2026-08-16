import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    raise ValueError("Groq API Key not found!!!")
# connect to server
client = Groq(api_key = groq_api_key)

model = "llama-3.3-70b-versatile"
role = "user"
content = "Do you know professorx2001"
message = {
    "role": role,
    "content": content
}
# list of messageges
messages = [message]


response = client.chat.completions.create(model=model, messages = messages)
# print(response)

answer = response.choices[0].message.content
print(answer)