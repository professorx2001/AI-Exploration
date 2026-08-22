import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    raise ValueError("Groq API Key not found!!!")

client = Groq(api_key=groq_api_key)
model = "openai/gpt-oss-120b"

# define the schema of your output
class Ticket(BaseModel):
    name: str
    email: str
    phone: int


schema = Ticket.model_json_schema()
response_format = {
    "type": "json_object"
}

# You'll have to specifically mention json format here
message_system = {
    "role": "system",
    "content": f"Extract the personal information from the ticket in json format, strictly based on this schema. {schema}"
}
message = {
    "role": "user",
    "content": "Dear Apple, I am Md Zaki Hussain, I recently bought Macbook Air M5 and it is working absolutely fine. If Tim Cook is seeing it he can reply to me at mdzakihusain@gmail.com or reach me at 7548484848. I am currently in Kolkata. I have started reading a book my Mark Manson named Everything is f*cked."
}
messages = [message_system, message]

# limit the usage of tokens
response = client.chat.completions.create(
    model=model, messages=messages, response_format=response_format)
answer = response.choices[0].message.content
print(answer)



# Extracting the value now, this can be used by other system/application anything 
import json

data = json.loads(answer)
print(data["name"])


ticket_obj = Ticket(**data)
print(f"I am {ticket_obj.name}")
print(f"My Mail is {ticket_obj.email}")
print(f"You can contact me at {ticket_obj.phone}")