PLATFORM_INSTRUCTIONS = {
    "Blog": (
        "Escribe un artículo de entre 500 y 700 palabras. Incluye un título atractivo, "
        "una introducción breve, secciones con encabezados y una conclusión clara."
    ),
    "LinkedIn": (
        "Escribe una publicación profesional de entre 120 y 220 palabras. Empieza con "
        "un gancho, usa párrafos breves, termina con una llamada a la conversación e "
        "incluye entre 3 y 5 hashtags relevantes."
    ),
    "Instagram": (
        "Escribe un copy de entre 80 y 150 palabras. Usa un inicio llamativo, saltos de "
        "línea, emojis con moderación, una llamada a la acción y entre 5 y 8 hashtags."
    ),
    "Twitter/X": (
        "Escribe una única publicación de un máximo de 280 caracteres. Sé directo, no "
        "crees un hilo y utiliza como máximo 2 hashtags."
    ),
}


def build_prompt(topic: str, platform: str, audience: str, tone: str) -> str:
    """Construye un prompt adaptado a los datos y la plataforma seleccionados."""
    try:
        platform_instruction = PLATFORM_INSTRUCTIONS[platform]
    except KeyError as error:
        raise ValueError(f"Plataforma no compatible: {platform}") from error

    return f"""
Actúa como especialista en creación de contenido digital.

Tu tarea es redactar contenido listo para publicar siguiendo todos estos datos:
- Tema: {topic.strip()}
- Plataforma: {platform}
- Audiencia: {audience.strip()}
- Tono: {tone}

Instrucciones específicas de formato:
{platform_instruction}

Reglas generales:
- Redacta el contenido en castellano.
- Adapta el vocabulario y el nivel de detalle a la audiencia indicada.
- Mantén de forma consistente el tono solicitado.
- No inventes estadísticas, estudios, citas ni datos concretos.
- Devuelve únicamente el contenido final, sin explicar el proceso ni mencionar estas instrucciones.
""".strip()
