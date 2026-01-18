from pathlib import Path
from dotenv import load_dotenv
import os

# FORÇA o caminho do .env
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

print("DEBUG key loaded:", os.getenv("OPENAI_API_KEY") is not None)

from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="gpt-4.1-mini",
    input="Say hello in one short sentence."
)

print(response.output_text)
