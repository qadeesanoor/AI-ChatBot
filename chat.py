from models.llm import chat_with_llm
from roles import get_system_prompt
from database import save_message, get_chat_history


def process_message(message: str, role: str, session_id: str):

    system_prompt = get_system_prompt(role)

    chat_history = get_chat_history(session_id)

    save_message(session_id, "user", message)

    response = chat_with_llm(
        message=message,
        system_prompt=system_prompt,
        chat_history=chat_history
    )

    save_message(session_id, "assistant", response)

    return response
