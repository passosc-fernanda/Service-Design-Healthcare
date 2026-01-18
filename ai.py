from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()  # NÃO passe api_key aqui

def ask_ai(question, summaries):
    context = "\n\n".join(summaries)

    prompt = f"""You are an assistant that answers questions based on the following summaries:

{context}

Question:
{question}
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return response.output_text
