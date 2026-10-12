# Generador de contenido con IA

Prueba de concepto educativa que genera textos listos para publicar y adaptados a
Blog, LinkedIn, Instagram o Twitter/X. El usuario elige el tema, la audiencia y el
tono; la aplicación construye un prompt específico y obtiene el contenido mediante
un único modelo de lenguaje.

## Funcionalidades

- Formulario web creado con Streamlit.
- Generación para cuatro plataformas con reglas de formato diferentes.
- Prompt dinámico según tema, plataforma, audiencia y tono.
- Integración de Groq con LangChain.
- Validación de campos y manejo básico de errores.
- Visualización del prompt utilizado y descarga del resultado.

## Arquitectura

```text
Usuario
  ↓
app.py (interfaz y flujo)
  ↓
prompt_builder.py (prompt engineering)
  ↓
llm_service.py (LangChain + Groq)
  ↓
Modelo openai/gpt-oss-20b
```

La separación permite modificar la interfaz, los prompts o el proveedor del modelo
sin mezclar sus responsabilidades.

## Estructura

```text
.
├── app.py
├── llm_service.py
├── prompt_builder.py
├── requirements.txt
├── .env.example
├── .gitignore
├── docs/
│   └── articulo-medium.md
└── tests/
    ├── test_prompt_builder.py
    ├── test_app.py
    └── check_live_generation.py
```

## Requisitos

- Python 3.10 o superior.
- Una cuenta de Groq y una API key.

## Instalación

En PowerShell, desde la carpeta del proyecto:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Si PowerShell impide activar el entorno, ejecuta los comandos directamente con
`.\.venv\Scripts\python.exe`.

## Configuración

1. Crea una API key en la consola de Groq.
2. Copia el archivo de ejemplo:

```powershell
Copy-Item .env.example .env
```

3. Abre `.env` y sustituye el valor de ejemplo:

```dotenv
GROQ_API_KEY=tu_clave_real
GROQ_MODEL=openai/gpt-oss-20b
```

`.env` está incluido en `.gitignore` y nunca debe subirse al repositorio.

## Ejecución

```powershell
streamlit run app.py
```

Abre `http://localhost:8501`, completa los campos y pulsa **Generar contenido**.

## Prompt engineering

`prompt_builder.py` combina los datos variables del formulario con reglas fijas por
plataforma. Blog solicita un artículo estructurado; LinkedIn, una publicación
profesional; Instagram, un copy visual; y Twitter/X, un único texto de hasta 280
caracteres. De este modo no se utiliza un prompt genérico para todos los casos.

## Pruebas

Las pruebas verifican los prompts y el flujo del formulario con respuestas
simuladas. No llaman al LLM ni consumen cuota:

```powershell
python -m unittest discover -s tests -v
```

Para una prueba manual, utiliza el mismo tema con las cuatro plataformas y comprueba
que cambian la longitud, la estructura y los elementos propios de cada red.
El resultado se conserva durante la sesión y la interfaz avisa si una respuesta para
Twitter/X supera los 280 caracteres. Estos tests no verifican la calidad de las
respuestas reales: esa comprobación necesita una clave de Groq y conexión a Internet.

Para repetir la comprobación del formulario con respuestas reales de las cuatro
plataformas (consume cuota de Groq):

```powershell
.\.venv\Scripts\python.exe tests/check_live_generation.py
```

Puedes probar solo una plataforma con `--platforms LinkedIn`. Esta comprobación
muestra el texto y su longitud, y verifica que se visualiza y permanece en la sesión.

## Limitaciones de la POC

- Requiere conexión a Internet y una API key de Groq.
- Utiliza un único modelo y no guarda historial.
- No incluye imágenes, RAG, agentes, autenticación ni base de datos.
- La salida de un LLM puede contener errores y debe revisarse antes de publicarse.

## Artículo publicado en Medium

Puedes leer cómo se desarrolló el proyecto en
[De un formulario a un texto publicable: una POC de generación de contenido con Python y un LLM](https://medium.com/@fernandatorokpolito/de-un-formulario-a-un-texto-publicable-una-poc-de-generaci%C3%B3n-de-contenido-con-python-y-un-llm-bfc714f81044).

La copia del artículo se conserva en [docs/articulo-medium.md](docs/articulo-medium.md).

## Tecnologías

- Python
- Streamlit
- LangChain
- Groq
- `openai/gpt-oss-20b`
