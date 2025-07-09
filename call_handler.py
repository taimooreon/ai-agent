import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

async def handle_call(text, business):
    prompt = f"""
    You are a receptionist for {business['name']}.

    Services: {business['services']}
    Address: {business['address']}
    Hours: {business['hours']}

    Customer said: "{text}"
    Respond helpfully and professionally.
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": text}
        ]
    )

    return response['choices'][0]['message']['content']