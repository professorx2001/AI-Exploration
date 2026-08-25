import json
import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel
from pypdf import PdfReader

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    raise ValueError("Groq API Key not found!!!")

client = Groq(api_key=groq_api_key)
model = "openai/gpt-oss-120b"

# define the schema of your output


class Resume(BaseModel):
    exp: int
    skills: list
    tools: list
    cgpa: float
    stream: str
    certification_count: int
    located_at: str
    email: str


schema = Resume.model_json_schema()
response_format = {
    "type": "json_object"
}

message_system = {
    "role": "system",
    "content": f"Extract the personal information from the Resume in json format, strictly based on this schema. {schema}"
}
# Making Path independent of where we run the script
file_path = Path(__file__).parent / "Resource" / "Resume.pdf"
reader = PdfReader(file_path)

resume_text = "\n".join(page.extract_text() or "" for page in reader.pages)

message = {
    "role": "user",
    "content": resume_text
}

messages = [message_system, message]

response = client.chat.completions.create(
    model=model, messages=messages, response_format=response_format)
answer = response.choices[0].message.content




resume_data = json.loads(answer)

#### print(resume_data) ####

# {
#   "exp": 1,
#   "skills": [
#     "Python",
#     "SQL",
#     "PySpark",
#     "AWS",
#     "Terraform",
#     "C++",
#     "PostgreSQL",
#     "MS SQL Server",
#     "DSA",
#     "CI/CD",
#     "AI",
#     "Apache Hudi",
#     "CDC",
#     "SCD Type 0",
#     "SCD Type 1",
#     "SCD Type 2",
#     "Dimensional Modelling",
#     "CloudFormation",
#     "Data Engineering",
#     "Lakehouse Architecture"
#   ],
#   "tools": [
#     "Terraform",
#     "Jenkins",
#     "CloudWatch",
#     "Amazon Q",
#     "Kiro IDE",
#     "VS Code",
#     "AWS Glue",
#     "AWS Lambda",
#     "AWS Step Functions",
#     "AWS EventBridge",
#     "AWS DMS",
#     "AWS Athena",
#     "AWS DynamoDB",
#     "AWS RDS",
#     "AWS IAM"
#   ],
#   "cgpa": 8.13,
#   "stream": "Computer Science & Engineering",
#   "certification_count": 2,
#   "located_at": "Kolkata, West Bengal",
#   "email": "mdzakihusain@gmail.com"
# }

#### Our checklist ####
# exp: int > 2
# skills: list [Python, PySpark, SQL, AWS, AI]
# tools: list [VS Code, Terraform, Jenkins]
# cgpa: float > 8
# stream: str CS/IT
# certification_count: int >= 1
# located_at: str India
# email: str It will used to send a confirmation mail to candidate

def check_resume(resume_data: dict) -> bool:
    
    print(f"Candidate looks good, A confirmation mail sent at {resume_data.email}")