import os
from groq import Groq

# Get a free key at https://console.groq.com
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL = "llama-3.3-70b-versatile"


def chat_with_llm(message: str, system_prompt: str, chat_history: list) -> str:
    messages = [{"role": "system", "content": system_prompt}]

    for m in chat_history:
        messages.append({"role": m["role"], "content": m["content"]})

    messages.append({"role": "user", "content": message})

    completion = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.7,
    )

    return completion.choices[0].message.content
