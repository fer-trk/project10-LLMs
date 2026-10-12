import streamlit as st
from dotenv import load_dotenv

from llm_service import LLMConfigurationError, generate_content
from prompt_builder import build_prompt


load_dotenv()

st.set_page_config(
    page_title="Generador de contenido",
    page_icon="✍️",
    layout="centered",
)

st.title("Generador de contenido con IA")
st.write(
    "Crea contenido adaptado a una plataforma, una audiencia y un tono concretos."
)

with st.form("content_form"):
    topic = st.text_area(
        "Tema",
        placeholder="Ejemplo: beneficios de aprender inteligencia artificial",
    )
    platform = st.selectbox(
        "Plataforma",
        options=["Blog", "LinkedIn", "Instagram", "Twitter/X"],
    )
    audience = st.text_input(
        "Audiencia",
        placeholder="Ejemplo: personas que están empezando a programar",
    )
    tone = st.selectbox(
        "Tono",
        options=["Profesional", "Cercano", "Divulgativo", "Inspirador"],
    )
    submitted = st.form_submit_button("Generar contenido", type="primary")

if submitted:
    if not topic.strip() or not audience.strip():
        st.warning("Completa el tema y la audiencia antes de continuar.")
    else:
        prompt = build_prompt(
            topic=topic,
            platform=platform,
            audience=audience,
            tone=tone,
        )

        try:
            with st.spinner("Generando contenido..."):
                generated_content = generate_content(prompt)
        except LLMConfigurationError as error:
            st.error(str(error))
        except Exception:
            st.error(
                "No se pudo generar el contenido. Comprueba tu conexión, "
                "la clave de Groq y vuelve a intentarlo."
            )
        else:
            # Conserva el resultado cuando Streamlit vuelve a ejecutar la interfaz.
            st.session_state["result"] = {
                "content": generated_content,
                "prompt": prompt,
                "platform": platform,
            }

if "result" in st.session_state:
    result = st.session_state["result"]
    st.subheader(f"Contenido generado para {result['platform']}")
    st.markdown(result["content"])
    if result["platform"] == "Twitter/X" and len(result["content"]) > 280:
        st.warning(
            f"El texto tiene {len(result['content'])} caracteres y supera el límite "
            "de 280. Acórtalo antes de publicar o vuelve a generar."
        )
    st.download_button(
        "Descargar como texto",
        data=result["content"],
        file_name="contenido_generado.txt",
        mime="text/plain",
    )
    with st.expander("Ver el prompt utilizado"):
        st.code(result["prompt"], language="text")
