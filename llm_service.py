import os

from langchain_groq import ChatGroq


DEFAULT_MODEL = "openai/gpt-oss-20b"


class LLMConfigurationError(RuntimeError):
    """Indica que falta una variable necesaria para utilizar el LLM."""


def generate_content(prompt: str) -> str:
    """Envía el prompt a Groq mediante LangChain y devuelve el texto generado."""
    if not os.getenv("GROQ_API_KEY"):
        raise LLMConfigurationError(
            "Falta GROQ_API_KEY. Copia .env.example como .env y añade tu clave de Groq."
        )

    model = ChatGroq(
        model=os.getenv("GROQ_MODEL", DEFAULT_MODEL),
        temperature=0.7,
        max_retries=2,
    )
    response = model.invoke(prompt)

    if not isinstance(response.content, str) or not response.content.strip():
        raise RuntimeError("El modelo devolvió una respuesta vacía.")

    return response.content.strip()
