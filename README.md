# Generador de contenido con IA

Prueba de concepto educativa que genera textos listos para publicar y adaptados a
Blog, LinkedIn, Instagram o Twitter/X. El usuario elige el tema, la audiencia y el
tono; la aplicación construye un prompt específico y obtiene el contenido mediante
un único modelo de lenguaje.

**Estado: Nivel Esencial implementado y comprobado con respuestas reales.** Los niveles
Medio, Avanzado y Experto se explican más abajo como una hoja de ruta: todavía no están
implementados. Esta guía describe tanto la aplicación actual como los pasos para ampliarla.

El proyecto responde al briefing educativo de una empresa ficticia, Digital Content,
que solicita una prueba de concepto de generación automática de contenido. Se prioriza
una solución pequeña que se pueda ejecutar, comprender y explicar durante una demo.

## Índice

- [Conceptos básicos](#conceptos-básicos)
- [Funcionalidades y alcance](#funcionalidades)
- [Arquitectura](#arquitectura)
- [Estructura de archivos](#estructura)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Ejecución](#ejecución)
- [Cómo se realizó el Nivel Esencial](#cómo-se-realizó-el-nivel-esencial)
- [Explicación del código](#explicación-del-código)
- [Prompt engineering](#prompt-engineering)
- [Pruebas](#pruebas)
- [Problemas frecuentes](#problemas-frecuentes)
- [Git y condiciones de entrega](#git-y-condiciones-de-entrega)
- [Nivel Medio: pasos para alcanzarlo](#nivel-medio-pasos-para-alcanzarlo)
- [Nivel Avanzado: pasos para alcanzarlo](#nivel-avanzado-pasos-para-alcanzarlo)
- [Nivel Experto: pasos para alcanzarlo](#nivel-experto-pasos-para-alcanzarlo)
- [Orden de trabajo recomendado](#orden-de-trabajo-recomendado)
- [Referencias oficiales](#referencias-oficiales)

## Conceptos básicos

| Concepto | Explicación para principiantes | Ejemplo en este proyecto |
| --- | --- | --- |
| POC | Prueba de concepto que demuestra que una idea funciona | Generar texto desde un formulario |
| MVP | Versión mínima que resuelve una necesidad concreta | Cuatro entradas y una respuesta |
| LLM | Modelo de lenguaje capaz de generar texto a partir de instrucciones | `openai/gpt-oss-20b` |
| Prompt | Texto de instrucciones que recibe el modelo | Tema, audiencia, tono y formato |
| Prompt engineering | Diseñar y probar instrucciones para orientar la respuesta | Reglas diferentes por plataforma |
| API | Interfaz para utilizar un servicio desde un programa | Petición de Python a Groq |
| API key | Credencial que autoriza peticiones a una cuenta | `GROQ_API_KEY` |
| Framework | Herramientas reutilizables para construir aplicaciones | Streamlit y LangChain |
| Token | Unidad con la que el modelo procesa texto; no equivale siempre a una palabra | Afecta al contexto y la cuota |
| Variable de entorno | Configuración que se lee sin escribirla directamente en el código | Clave y modelo |
| Alucinación | Respuesta convincente que contiene datos inventados o incorrectos | Riesgo que requiere revisión |

Aquí no se entrena ni se ajusta un modelo propio. Se utiliza un modelo existente
mediante una API. Cambiar un prompt no modifica los parámetros aprendidos del modelo.

## Funcionalidades

- Formulario web creado con Streamlit.
- Generación para cuatro plataformas con reglas de formato diferentes.
- Prompt dinámico según tema, plataforma, audiencia y tono.
- Integración de Groq con LangChain.
- Validación de campos y manejo básico de errores.
- Visualización del prompt utilizado y descarga del resultado.

El formulario solicita tema, plataforma, audiencia y tono. Las plataformas son Blog,
LinkedIn, Instagram y Twitter/X. Los tonos disponibles son Profesional, Cercano,
Divulgativo e Inspirador. La generación se solicita en castellano.

La interfaz también conserva el último resultado durante la sesión y avisa si una
respuesta para X supera 280 caracteres.

**Generar contenido no equivale a publicarlo automáticamente.** Esta aplicación no
se conecta a las cuentas de redes sociales. La persona revisa el texto y lo publica
por su cuenta. Tampoco guarda un historial permanente ni genera imágenes.

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

El modelo se ejecuta en Groq, no en el ordenador local. El prefijo `openai/` del
identificador no implica utilizar una clave de OpenAI: aquí se necesita una clave
de **Groq**. LangChain actúa como integración para acceder al modelo.

### Por qué se eligieron estas tecnologías

| Tecnología | Responsabilidad | Motivo |
| --- | --- | --- |
| Python | Lógica del proyecto | Código sencillo de leer y modificar |
| Streamlit | Interfaz web | Formulario construido desde Python |
| LangChain mediante `langchain-groq` | Acceso al LLM | Uso de un framework de aplicaciones LLM |
| Groq | Servicio de ejecución remota | Integración mediante API |
| `python-dotenv` | Lectura de `.env` | Separación de configuración y código |
| `unittest` y `AppTest` | Comprobaciones | Pruebas de lógica y flujo de interfaz |
| Git/GitHub | Historial y publicación del código | Cambios revisables y compartidos |

Las cuotas, precios y modelos disponibles pueden cambiar. Consultar la cuenta y la
documentación vigente antes de cambiar de modelo. Una alternativa local futura debe
considerar RAM, GPU y tiempo de respuesta; no basta con cambiar un nombre en `.env`.

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

- Python 3.12 recomendado para reproducir el entorno comprobado.
- Git para clonar el repositorio.
- Conexión a Internet para acceder a Groq.
- Una cuenta de Groq y una API key.

Las demás versiones de Python deben comprobarse contra las dependencias: no se han
probado todas en este proyecto.

## Instalación

### Paso 1. Comprobar Python y Git

En PowerShell en Windows:

```powershell
python --version
git --version
```

Si Windows no reconoce `python`, probar `py --version`. Si tampoco existe, instalar
Python desde su web oficial y habilitar su acceso desde el terminal. Después abrir
una nueva terminal.

### Paso 2. Obtener el código

```powershell
git clone https://github.com/fer-trk/project10-LLMs.git
cd project10-LLMs
```

Si ya tienes el repositorio, entrar en su carpeta en lugar de clonarlo de nuevo.
Todos los comandos siguientes se ejecutan desde esa carpeta.

### Paso 3. Crear el entorno e instalar dependencias

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip check
```

Un entorno virtual es una carpeta con Python y sus paquetes separados de los demás
proyectos. Evita que instalar una librería aquí cambie las dependencias de otra aplicación.
Si se utiliza `py`, puede crearse con `py -3.12 -m venv .venv`.

`pip` instala paquetes; `-r requirements.txt` indica la lista. `pip check` comprueba
incompatibilidades declaradas entre los paquetes instalados.

Los comandos anteriores usan directamente el Python de `.venv`, sin necesitar activación.
Otra opción es activar con `.\.venv\Scripts\Activate.ps1` y utilizar después `python`.

El proyecto fija Streamlit en `1.65.0` y utiliza rangos para `langchain-groq` y
`python-dotenv`. Estos rangos no fijan todas las dependencias exactamente. Para mayor
reproducibilidad, una mejora futura sería registrar versiones comprobadas y verificar
una instalación limpia.

En macOS o Linux, usar `.venv/bin/python`:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

## Configuración

### Paso 4. Obtener la clave de Groq

1. Entrar en [Groq API Keys](https://console.groq.com/keys).
2. Crear una cuenta o iniciar sesión.
3. Crear una API key con un nombre reconocible para este proyecto.
4. Copiarla para utilizarla en el archivo local `.env`.

La clave autoriza acceso a tu cuenta. No debe incluirse en código, capturas de pantalla,
artículos, mensajes públicos ni commits.

### Paso 5. Completar `.env`

Solo si todavía no existe el archivo `.env`, copiar la plantilla:

```powershell
Copy-Item .env.example .env
```

Si ya existe con una clave, editarlo sin sobrescribirlo con la plantilla.
Abrir `.env` y sustituir el valor de ejemplo:

```dotenv
GROQ_API_KEY=tu_clave_real
GROQ_MODEL=openai/gpt-oss-20b
```

`.env` está incluido en `.gitignore` y nunca debe subirse al repositorio.

`.env.example` explica qué variables se necesitan; `.env` contiene los valores privados.
Comprobar que Git ignora el archivo sin mostrar su contenido:

```powershell
git check-ignore .env
```

El resultado esperado es `.env`. Las variables definidas previamente en el entorno
tienen prioridad sobre las cargadas por `load_dotenv()` con su configuración actual.

## Ejecución

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Abre `http://localhost:8501`, completa los campos y pulsa **Generar contenido**.

Mantener la terminal abierta mientras se utiliza la aplicación. Para detenerla,
pulsar `Ctrl+C`. La vista previa no mantiene por sí sola el servidor encendido.

En macOS o Linux el comando equivalente es
`.venv/bin/python -m streamlit run app.py`.

Para una primera generación:

```text
Tema: Cómo empezar a aprender programación con Python
Plataforma: LinkedIn
Audiencia: Personas adultas sin experiencia en programación
Tono: Cercano
```

Después revisar el texto, desplegar **Ver el prompt utilizado** y descargarlo si interesa.

## Cómo se realizó el Nivel Esencial

### 1. Revisar el briefing y definir el alcance

Se separaron las funciones esenciales de las de niveles superiores. La primera versión
debía generar texto mediante prompts y ofrecer una interfaz web. Se eligieron cuatro
plataformas, un único modelo y una estructura fácil de explicar para un proyecto de dos días.

### 2. Preparar Git y construir el formulario

Se conservó `main` como rama estable y se creó `feature/essential-mvp` para desarrollar.
La interfaz inicial recogía tema, plataforma, audiencia y tono y mostraba los datos.
Esto permitía comprobar las entradas antes de incorporar la API.

### 3. Diseñar el prompt engineering

Se creó un diccionario con reglas por plataforma y una función que combina esas reglas
con los datos del usuario. Cambiar la plataforma modifica las instrucciones enviadas
al modelo, no solamente una etiqueta en pantalla.

### 4. Integrar el modelo y conectar el flujo

Se añadió `ChatGroq` en un archivo independiente. El servicio lee la configuración,
envía el prompt y devuelve texto. La interfaz coordina las llamadas y presenta la respuesta.

### 5. Añadir comprobaciones y documentar

Se añadieron validación de entradas, mensajes de error, conservación del resultado y
aviso de longitud para X. Se probaron prompts y formulario, se realizaron peticiones
reales para las cuatro plataformas y se publicó el artículo de Medium.

### Correspondencia con el briefing

| Requisito esencial | Implementación o evidencia |
| --- | --- |
| Texto sobre temas del usuario | Tema libre enviado al modelo |
| Adaptación a plataformas y audiencias | Reglas por plataforma y audiencia en el prompt |
| Uso de prompts | `build_prompt()` con instrucciones explícitas |
| Interfaz web | Formulario de Streamlit |
| Artículo redactado y publicado | Enlace de Medium en esta documentación |
| Git organizado | Ramas y commits por unidades comprensibles |
| Documentación del código y README | Funciones documentadas, comentarios y esta guía |

## Explicación del código

### `app.py`: interacción y coordinación

`load_dotenv()` carga la configuración de `.env`. `st.set_page_config()` configura
el título de la pestaña y el aspecto general de la página.

Dentro de `st.form()` se utilizan:

- `st.text_area()` para el tema, que puede ocupar varias líneas.
- `st.text_input()` para la audiencia.
- `st.selectbox()` para elegir plataforma y tono.
- `st.form_submit_button()` para enviar el formulario.

Streamlit vuelve a ejecutar el script ante determinadas interacciones. El formulario
agrupa las entradas y `if submitted:` controla cuándo generar contenido.

`not topic.strip()` comprueba si el tema queda vacío después de quitar espacios de
los extremos. Escribir únicamente espacios no supera la validación. Se hace la misma
comprobación con la audiencia.

Con entradas válidas, se construye el prompt y se llama al servicio dentro de un bloque
`try/except`. El indicador `st.spinner()` muestra que la petición está en curso. La
interfaz distingue la falta de configuración de otros fallos, aunque estos últimos
comparten un mensaje genérico.

El resultado se guarda en `st.session_state["result"]` junto al prompt y la plataforma.
Así puede mostrarse de nuevo durante la sesión sin repetir la petición. Descargarlo
tampoco necesita una nueva generación. No es un historial persistente: puede perderse
al terminar la sesión.

Si una generación posterior falla, el resultado anterior permanece. Su encabezado indica
la plataforma a la que pertenece; no debe confundirse con una nueva respuesta exitosa.

`st.markdown()` muestra texto con encabezados y listas; `st.download_button()` permite
guardarlo en `.txt`. La comprobación de X utiliza `len(content)`: es un conteo básico de
caracteres de Python, no una implementación completa de las reglas de esa plataforma.

### `prompt_builder.py`: decisiones editoriales

`PLATFORM_INSTRUCTIONS` relaciona cada nombre de plataforma con sus instrucciones.
`build_prompt()` recibe cuatro cadenas de texto y devuelve otra: el prompt completo.
Las anotaciones `str` ayudan a entender los parámetros, pero no validan por sí solas
todos los valores en tiempo de ejecución.

Una cadena `f"..."` permite insertar datos en el texto. Ejemplo de uso de la función:

```python
prompt = build_prompt(
    topic="Cómo empezar con Python",
    platform="Twitter/X",
    audience="Personas principiantes",
    tone="Cercano",
)
```

El resultado contiene esas entradas, las instrucciones de X y las reglas generales.
Si recibe una plataforma desconocida, lanza `ValueError`. El selector de la interfaz
evita normalmente ese caso.

### `llm_service.py`: comunicación con Groq

`os.getenv()` lee clave y modelo. Si falta una clave no vacía, se lanza
`LLMConfigurationError`. Esto no comprueba si la clave es válida: una clave incorrecta
se detecta cuando se intenta utilizar la API.

| Parámetro de `ChatGroq` | Valor | Significado |
| --- | --- | --- |
| `model` | `GROQ_MODEL` o valor por defecto | Qué modelo se ejecuta |
| `temperature` | `0.7` | Influye en la variabilidad, no mide exactitud |
| `timeout` | `60` | Tiempo configurado para esperar una petición |
| `max_retries` | `2` | Reintentos para fallos que el cliente considere reintentables |

El tiempo total puede superar 60 segundos debido a los reintentos. No todos los errores
son reintentables. `model.invoke(prompt)` devuelve un mensaje; el servicio verifica que
su contenido sea una cadena no vacía y devuelve el texto sin espacios en los extremos.

`GROQ_MODEL` permite cambiar configuración, pero todavía no existe selector de modelos
en el formulario. Esa variable no satisface por sí sola el requisito de elegir entre
dos LLMs del Nivel Medio.

### Archivos de configuración

- `requirements.txt`: paquetes necesarios para instalar el proyecto.
- `.env.example`: configuración de ejemplo sin claves reales.
- `.gitignore`: excluye el entorno virtual, la clave y archivos temporales.
- `tests/`: comprobaciones del prompt y de la aplicación.

LangChain puede instalar `langsmith` como dependencia transitiva. Eso no significa que
la trazabilidad del Nivel Avanzado esté implementada o activada en este proyecto.

## Prompt engineering

`prompt_builder.py` combina los datos variables del formulario con reglas fijas por
plataforma. Blog solicita un artículo estructurado; LinkedIn, una publicación
profesional; Instagram, un copy visual; y Twitter/X, un único texto de hasta 280
caracteres. De este modo no se utiliza un prompt genérico para todos los casos.

| Plataforma | Extensión solicitada | Elementos |
| --- | --- | --- |
| Blog | 500–700 palabras | Título, introducción, secciones y conclusión |
| LinkedIn | 120–220 palabras | Gancho, párrafos breves, conversación y 3–5 hashtags |
| Instagram | 80–150 palabras | Inicio llamativo, saltos de línea, emojis, CTA y 5–8 hashtags |
| Twitter/X | Hasta 280 caracteres | Publicación única, sin hilo, hasta 2 hashtags |

Estos rangos son decisiones de diseño de la POC, no todos los límites oficiales de las
redes. El prompt pide castellano, vocabulario adecuado, tono consistente y contenido
final sin explicar el proceso. También pide no inventar estadísticas, estudios ni citas.

**Un prompt orienta; no garantiza.** La aplicación no verifica automáticamente la
exactitud factual, los rangos de palabras ni todos los hashtags. En la interfaz, el
aviso de X es la única comprobación de longitud implementada.

## Pruebas

Las pruebas verifican los prompts y el flujo del formulario con respuestas
simuladas. No llaman al LLM ni consumen cuota:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
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

### Qué demuestran las siete pruebas automáticas

| Comprobación | Qué se verifica |
| --- | --- |
| Datos del prompt | Incluye tema, plataforma, audiencia y tono |
| Reglas por plataforma | Se incluyen las instrucciones correspondientes |
| Plataforma desconocida | Se lanza el error esperado |
| Formulario vacío | Aviso sin llamar al modelo |
| Flujo de cuatro plataformas | Muestra y conserva una respuesta simulada |
| Fallo del servicio | Mensaje de error sin una excepción visible de la aplicación |
| X demasiado largo | Aviso ante una salida simulada de 281 caracteres |

Un **mock** sustituye temporalmente el servicio por una respuesta controlada para
probar la interfaz. Estas pruebas no demuestran que el modelo conozca un tema o que
siempre cumpla el prompt. Tampoco sustituyen una revisión visual completa en un navegador.

El script real muestra conteos para revisión; no rechaza automáticamente todas las
desviaciones editoriales. Separa palabras por espacios y cuenta apariciones de hashtags,
no necesariamente hashtags únicos.

### Resultados reales observados durante el desarrollo

Tema: «Cómo empezar a aprender programación con Python». Audiencia: personas adultas
sin experiencia en programación. Tono: Cercano.

| Plataforma | Resultado observado |
| --- | --- |
| Blog | 674 palabras, título, secciones y conclusión |
| LinkedIn | 157 palabras, pregunta final y 5 hashtags |
| Instagram | 96 palabras, emojis y llamada a la acción |
| Twitter/X | 237 caracteres |

Las cuatro muestras cumplieron las extensiones y se mostraron correctamente. Las
ejecuciones futuras pueden dar otros resultados; esto no es un benchmark general.

### Práctica manual para comprender el sistema

1. Generar el mismo tema en las cuatro plataformas y comparar estructura y extensión.
2. Mantener el tema y cambiar la audiencia de principiante a experta.
3. Cambiar únicamente el tono y comparar el vocabulario.
4. Consultar los prompts para identificar las instrucciones que cambiaron.
5. Revisar afirmaciones concretas antes de publicar.
6. Probar campos vacíos y observar la validación.

Registrar ejemplos problemáticos y cambiar una regla cada vez ayuda a entender qué
mejora el resultado, en lugar de modificar todo el prompt por una impresión aislada.

## Problemas frecuentes

| Problema | Qué revisar |
| --- | --- |
| Windows no reconoce `python` | Instalación, PATH o lanzador `py`; abrir una terminal nueva |
| PowerShell bloquea la activación | Utilizar directamente `.venv\Scripts\python.exe` |
| `ModuleNotFoundError` | Instalar dependencias con el mismo Python que ejecuta la aplicación |
| Falta la clave | Archivo `.env`, nombre `GROQ_API_KEY` y valor no vacío |
| Clave escrita pero generación fallida | Validez, espacios, cuota, conexión y modelo disponible |
| La vista previa no abre | Confirmar que Streamlit está ejecutándose y abrir su URL |
| Puerto 8501 ocupado | Ejecutar con `--server.port 8502` y abrir el puerto nuevo |
| X supera 280 caracteres | Acortar el texto o volver a generar |
| Se pierde el texto al terminar la sesión | Descargarlo antes: no hay almacenamiento permanente |

Si se modifica `.env` con el servidor en marcha, detener y reiniciar Streamlit evita
reutilizar valores ya cargados. Revisar también variables de entorno externas que
puedan tener prioridad sobre `.env`.

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py --server.port 8502
```

Si una clave se publica por accidente, revocarla en el proveedor y crear otra.
Eliminarla del archivo actual no la elimina del historial de Git.

## Git y condiciones de entrega

Se desarrolló en `feature/essential-mvp` y se integró el resultado en `main`. Se guardaron
unidades identificables: versión inicial, mejoras y pruebas, artículo y enlace publicado.

Para una mejora futura, utilizar una rama descriptiva mientras esa unidad esté en curso.
No hace falta crear una rama por archivo ni todas las ramas del roadmap por anticipado.
Ejemplo de flujo futuro, no una orden para ejecutarlo ahora:

```powershell
git switch main
git pull --ff-only
git switch -c feature/brand-context
# Implementar y comprobar la unidad de trabajo.
git status
git diff
git add archivo_modificado.py
git commit -m "feat: add brand context to content prompts"
git push -u origin feature/brand-context
```

Un commit guarda una versión local; un push la sube al remoto; una integración la
incorpora a la rama de destino. Revisar los archivos antes de guardar y abrir una
revisión o PR cuando corresponda.

El Esencial incluye interfaz, prompts, documentación, Git y artículo publicado. Las
condiciones generales también piden demo en vivo, presentación técnica y tablero Kanban.
El repositorio no certifica por sí solo que estos tres entregables estén preparados.

Para la demo:

1. Arrancar la aplicación y comprobar conexión antes de presentar.
2. Mostrar un tema, audiencia y tono concretos.
3. Generar contenido y enseñar el prompt.
4. Cambiar la plataforma y explicar la diferencia de formato.
5. Mostrar validación y descarga.
6. Explicar pruebas y limitaciones.

La presentación debe cubrir problema, alcance, arquitectura, prompts, tecnologías,
resultados y próximos pasos. El Kanban debe reflejar tareas pendientes, en curso y
terminadas con evidencia de finalización.

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

## Nivel Medio: pasos para alcanzarlo

**Plan futuro, no implementado.** El briefing requiere cuatro capacidades: Docker,
elección entre al menos dos LLMs, contexto de empresa o persona e imágenes integradas.
Las sugerencias de módulos de esta guía no existen todavía y sus nombres son orientativos.

### 1. Añadir información de empresa o persona

El tema dice sobre qué se publica; el contexto de marca explica quién publica y cómo
quiere comunicarse. Esto puede resolverse incorporando datos al prompt, sin necesitar RAG.

Pasos:

1. Definir campos mínimos: nombre, actividad, estilo de comunicación, valores y términos
   que se desea evitar.
2. Añadir una sección de configuración o formulario en Streamlit.
3. Pasar esos datos a `build_prompt()` como contexto de marca.
4. Incorporarlos a todas las generaciones realizadas con ese perfil.
5. Decidir si basta conservar el perfil durante la sesión o si necesita persistencia.
6. Probar el mismo tema con dos perfiles distintos y comparar el estilo.

Qué tener en cuenta: limitar la extensión del contexto, no incluir datos privados
innecesarios y mantener diferenciadas las instrucciones del sistema y los datos del
usuario. La marca no sustituye a la audiencia ni al tono.

**Criterio de finalización:** demostrar que el contexto se incorpora a los prompts
de las cuatro plataformas y se refleja en los resultados.

### 2. Permitir seleccionar dos o más LLMs

Un proveedor es el servicio; un modelo es el sistema que genera la respuesta. Dos
modelos podrían utilizar el mismo proveedor si la evaluación del proyecto lo admite.
Cambiar de proveedor añade credenciales, dependencias y configuración.

Pasos:

1. Seleccionar dos modelos disponibles para la cuenta y adecuados para generar texto.
2. Revisar idiomas, cuota, latencia, coste y requisitos en documentación actual.
3. Añadir un selector de modelos con opciones permitidas y nombres comprensibles.
4. Modificar `generate_content()` para recibir la elección del usuario.
5. Conservar una salida textual común para no acoplar la interfaz a un proveedor.
6. Probar elección de modelo, configuración incorrecta y errores de cada opción.
7. Comparar ambos modelos usando los mismos datos y prompts.

Qué tener en cuenta: no aceptar identificadores arbitrarios sin validar. No todos los
modelos admiten los mismos parámetros. Si se incluye una opción local, comprobar RAM,
GPU y conectividad desde el entorno donde corre la aplicación.

**Criterio de finalización:** elegir dos LLMs desde la interfaz y demostrar generación
real con ambos, informando los fallos de cada opción cuando proceda.

### 3. Incorporar imágenes relevantes

El briefing permite generarlas con IA u obtenerlas de otra fuente. Una API de fotografías
puede ser una primera opción; un modelo de imágenes añade requisitos, coste y latencia.

Pasos:

1. Elegir una fuente y revisar permisos de uso, atribución, límites y condiciones.
2. Definir una búsqueda o descripción de imagen a partir del tema.
3. Separar esa consulta de la generación de texto, por ejemplo en un servicio de imágenes.
4. Recuperar imagen, descripción y atribución cuando proceda.
5. Integrarla con el contenido en pantalla y definir una exportación adecuada.
6. Añadir texto alternativo para accesibilidad.
7. Probar búsquedas sin resultados y errores de la fuente sin perder el texto generado.

Qué tener en cuenta: una imagen decorativa no demuestra relevancia. Revisar su relación
con tema y audiencia. Un blog puede necesitar imágenes entre secciones; Instagram,
una pieza visual asociada al copy. Una descarga `.txt` no conserva imágenes.

**Criterio de finalización:** presentar texto e imagen como una pieza coherente y
conservar la atribución necesaria. Si se ofrece exportación combinada, comprobar que
el archivo o paquete entregado mantiene la relación entre ambos.

### 4. Dockerizar la aplicación

Una imagen de Docker empaqueta aplicación y entorno. Un contenedor es una ejecución
de esa imagen. Docker facilita reproducir la instalación, pero no elimina la dependencia
de Groq ni convierte un modelo remoto en local.

Pasos:

1. Comprobar una instalación limpia y las versiones necesarias.
2. Crear un `Dockerfile` con una imagen oficial de Python compatible.
3. Instalar dependencias y copiar los archivos necesarios.
4. Configurar Streamlit para escuchar en `0.0.0.0` dentro del contenedor.
5. Crear `.dockerignore`, excluyendo `.env`, `.venv`, `.git` y archivos innecesarios.
6. Proporcionar secretos al ejecutar, no al construir la imagen.
7. Mapear el puerto del contenedor al ordenador y comprobar el formulario y la generación.
8. Documentar construcción, ejecución y parada.

Qué tener en cuenta: `.gitignore` no sustituye `.dockerignore`; no copiar el entorno
virtual de Windows a una imagen Linux. Revisar versiones y tamaño de imagen. Consultar
las [buenas prácticas de Docker](https://docs.docker.com/build/building/best-practices/).

**Criterio de finalización:** ejecutar la aplicación con las funciones del Medio en
un contenedor y un entorno limpio, sin secretos incluidos en la imagen.

## Nivel Avanzado: pasos para alcanzarlo

**Plan futuro, no implementado.** El briefing pide trazabilidad, cuatro idiomas,
noticias financieras actuales y divulgación científica mediante RAG con documentos de arXiv.

### 1. Añadir trazabilidad de peticiones y respuestas

Una traza permite reconstruir una petición: entradas, prompt, modelo, respuesta,
duración y errores. Ayuda a depurar y comparar ejecuciones; mostrar un prompt en la
interfaz no equivale a conservar trazas históricas.

Pasos:

1. Definir qué observar y qué información excluir o anonimizar.
2. Elegir LangSmith u otra herramienta y comprobar su configuración vigente.
3. Registrar construcción del prompt y llamada al modelo con un identificador.
4. Añadir plataforma, versión del prompt y modelo utilizado.
5. Registrar duración, estado y tokens cuando el proveedor los facilite.
6. Revisar privacidad, retención y acceso; no registrar la API key.
7. Provocar un fallo controlado y localizarlo en la herramienta.

Qué tener en cuenta: las trazas pueden contener temas, datos personales o información
de marca. Decidir qué datos se envían a un servicio externo antes de activarlo.

**Criterio de finalización:** consultar una petición exitosa y una fallida, identificar
sus entradas y salidas y explicar dónde ocurrió el fallo.

### 2. Generar en castellano, inglés, francés e italiano

Pasos:

1. Añadir un selector con los cuatro idiomas.
2. Sustituir la instrucción fija de castellano por una dependiente de la selección.
3. Mantener el formato de cada plataforma en todos los idiomas.
4. Revisar ejemplos con lectores capaces de evaluar naturalidad y precisión.
5. Adaptar expresiones, hashtags y llamadas a la acción al contexto lingüístico.
6. Incorporar el idioma a pruebas y trazas.

Qué tener en cuenta: generar en otro idioma no implica traducir la interfaz. Probar
nombres propios, acentos y terminología específica. No basta con que el idioma elegido
aparezca en el prompt; debe reflejarse en la respuesta.

**Criterio de finalización:** demostrar contenido en los cuatro idiomas y revisar su
calidad y adaptación por plataforma.

### 3. Crear la funcionalidad de noticias financieras actuales

El conocimiento previo del modelo no garantiza actualidad. Se necesita consultar una
API y aportar al LLM datos con fuente y fecha.

Pasos:

1. Definir mercados, instrumentos y antigüedad máxima aceptada para las noticias.
2. Elegir una API y revisar licencia, cuota, cobertura y retraso de los datos.
3. Crear un servicio que recupere titulares, fecha de publicación, fuente, enlace y
   contenido disponible. Una cotización aislada no implementa noticias.
4. Registrar también cuándo se consultaron los datos y eliminar duplicados.
5. Pasar un conjunto acotado de noticias al prompt como contexto externo.
6. Pedir referencias y distinguir hechos de interpretaciones.
7. Comunicar falta de actualidad cuando la respuesta esté vacía o sea demasiado antigua.
8. Probar zonas horarias, API caída, duplicados y ausencia de novedades.

Qué tener en cuenta: definir qué significa «actualizado». No sustituir una consulta
fallida por noticias inventadas. Tratar los datos recuperados como contenido, no como
instrucciones. No presentar un resumen generado como recomendación de inversión.

**Criterio de finalización:** demostrar que el contenido utiliza datos recientes
obtenidos mediante API y que se pueden identificar sus fuentes y fechas.

### 4. Construir un RAG científico con arXiv

**RAG** significa recuperar información relevante antes de generar una respuesta.
No entrena el modelo: le proporciona contexto documental para esa petición.
Un **embedding** representa un texto mediante números para buscar semejanza semántica.

```text
Preparación:
arXiv → selección → extracción de texto → fragmentos → embeddings → índice

Consulta:
Pregunta → búsqueda de fragmentos → contexto con fuentes → LLM → divulgación
```

Pasos:

1. **Acotar la especialidad.** Elegir una cuestión concreta de IA, física o biomedicina,
   en lugar de intentar cubrir toda la literatura científica.
2. **Buscar en arXiv.** Utilizar su API respetando condiciones y límites.
3. **Seleccionar documentos.** Registrar identificador, título, autores, fecha, versión
   y enlace. Definir criterios de relevancia. arXiv contiene preprints; su presencia
   no garantiza revisión por pares ni validez de todas las conclusiones.
4. **Extraer texto.** Revisar columnas, tablas y fórmulas para no mezclar contenido.
   Revisar licencias antes de redistribuir documentos completos.
5. **Dividir en fragmentos.** Elegir tamaño y solapamiento con ejemplos: fragmentos pequeños
   pueden perder contexto y los demasiado grandes dificultan la recuperación precisa.
6. **Crear embeddings.** Elegir un modelo compatible para indexar y consultar. Cambiar
   de modelo o dimensión puede exigir reconstruir el índice.
7. **Guardar el índice.** Elegir una solución de búsqueda vectorial o almacenamiento
   adecuada al volumen, conservando metadatos para localizar y citar cada fragmento.
8. **Recuperar evidencia.** Revisar qué fragmentos devuelve la búsqueda antes de integrar
   el generador. Si recupera documentos irrelevantes, mejorar esta etapa primero.
9. **Generar divulgación.** Aportar fragmentos y pedir explicaciones comprensibles,
   referencias y distinción entre resultados y limitaciones del estudio.
10. **Evaluar.** Preparar preguntas con fuentes y respuestas esperadas, incluyendo
    preguntas que el corpus no permite responder.

Qué tener en cuenta: evitar duplicar versiones, limitar el contexto, gestionar PDFs
que no se pueden procesar y comprobar que las citas respaldan lo afirmado. Comunicar
evidencia insuficiente en lugar de completar huecos con suposiciones.

**Criterio de finalización:** responder preguntas científicas con evidencia recuperada
de arXiv y referencias verificables, incluyendo un caso sin información suficiente.
Guardar PDFs en una carpeta por sí solo no constituye un RAG.

## Nivel Experto: pasos para alcanzarlo

**Plan futuro, no implementado.** El briefing pide Graph RAG, un sistema multiagente
y guardarraíles, evaluación o benchmark para mejorar calidad y controlar alucinaciones.

### 1. Ampliar el RAG mediante un grafo de conocimiento

Un grafo representa entidades y relaciones. Un nodo puede ser un artículo, método o
conjunto de datos; una relación puede indicar que un artículo utiliza un método.
Graph RAG usa esas relaciones como contexto para responder.

Pasos:

1. Elegir preguntas donde las relaciones aporten valor respecto al RAG vectorial.
2. Definir esquema: entidades, relaciones permitidas y propiedades.
3. Extraer relaciones mediante reglas o un modelo y revisarlas.
4. Conservar procedencia de cada relación: documento, versión y fragmento que la respalda.
5. Resolver duplicados, sinónimos y entidades ambiguas.
6. Elegir almacenamiento y consultas con límites de profundidad y resultados.
7. Recuperar relaciones junto a fragmentos originales cuando proceda.
8. Comparar con el RAG vectorial usando preguntas iguales y evidencia verificada.

Qué tener en cuenta: una relación extraída por un LLM puede ser incorrecta. No convertirla
automáticamente en hecho validado. Conservar y explicar contradicciones entre estudios.
Un dibujo de nodos no demuestra que se use el grafo para recuperar información.

**Criterio de finalización:** mostrar una respuesta que utiliza relaciones recuperadas
con procedencia y medir si mejora las respuestas a las preguntas objetivo.

### 2. Crear un sistema multiagente

Un agente combina instrucciones, un modelo y herramientas para realizar una tarea.
Un sistema multiagente coordina especialistas. Un flujo con reglas explícitas puede
ser un punto de partida más fácil de comprobar que decisiones totalmente autónomas.

Pasos:

1. Definir especialistas: contenido general, noticias financieras y divulgación científica.
2. Especificar entradas, salidas, herramientas y límites de cada uno.
3. Crear un mecanismo de selección que envíe cada caso al especialista adecuado.
4. Dar acceso solo a las herramientas necesarias para esa especialidad.
5. Incorporar prompts o modelos distintos cuando exista una razón comprobable.
6. Definir entrega de resultados, fallos y solicitudes ambiguas.
7. Limitar pasos, tiempo, tokens y llamadas para evitar bucles y gasto excesivo.
8. Registrar la ruta seguida y probar selección correcta e incorrecta.

Qué tener en cuenta: el agente financiero debe utilizar datos actuales y el científico,
las fuentes del RAG. Los mensajes entre agentes no sustituyen la evidencia original.
Publicar automáticamente requeriría un diseño y autorización específicos.

**Criterio de finalización:** mostrar casos enviados a agentes distintos y demostrar
que cambian instrucciones o herramientas según la tarea. Cambiar solamente el tono
de un prompt no constituye un sistema multiagente.

### 3. Incorporar guardarraíles, evaluación y benchmark

Los **guardarraíles** son comprobaciones que limitan o revisan entradas, acciones y
salidas. Un **benchmark** es un conjunto estable de casos para comparar versiones.

Pasos:

1. Definir fallos: longitud, idioma, citas inexistentes, afirmaciones sin respaldo,
   noticias antiguas o instrucciones maliciosas introducidas en documentos.
2. Añadir validaciones deterministas donde sea posible: límites, formatos y referencias,
   comprobando también su relación con fuentes recuperadas.
3. Definir qué hacer al fallar: avisar, pedir revisión, rechazar o regenerar con un límite.
4. Preparar casos normales, ambiguos y adversarios con resultados esperados.
5. Establecer métricas de formato, respaldo factual, recuperación, claridad, latencia y coste.
6. Separar los casos utilizados para ajustar prompts de los reservados para evaluar.
7. Combinar revisión humana con comprobaciones automáticas. Si otro LLM evalúa, contrastar
   sus juicios y documentar sus limitaciones.
8. Registrar versión del prompt, modelo, corpus y configuración para comparar cambios.

Qué tener en cuenta: un segundo modelo puede repetir el mismo error. Tener una cita no
prueba que respalde la afirmación. Definir umbrales antes de comparar y una salida para
los casos donde no haya evidencia suficiente.

**Criterio de finalización:** presentar resultados medidos sobre casos definidos,
mostrar errores detectados y explicar qué ocurre cuando falla una validación. Ningún
guardarraíl permite prometer ausencia absoluta de alucinaciones.

## Orden de trabajo recomendado

La secuencia siguiente es una propuesta de aprendizaje, no una estimación de horas:

| Orden | Unidad de trabajo | Evidencia para avanzar |
| --- | --- | --- |
| 1 | Estabilizar el Esencial | Instalación, pruebas y demo reproducibles |
| 2 | Contexto de marca | Diferencias observables entre perfiles |
| 3 | Dos LLMs | Generación real con ambas opciones |
| 4 | Imágenes | Integración con texto y permisos revisados |
| 5 | Docker | Ejecución reproducible del Medio |
| 6 | Trazabilidad | Peticiones exitosas y fallidas localizables |
| 7 | Cuatro idiomas | Ejemplos revisados por idioma |
| 8 | Noticias financieras | Fuentes y fechas verificables |
| 9 | RAG científico | Fragmentos relevantes y citas respaldadas por arXiv |
| 10 | Evaluación base | Casos y criterios para medir nuevas funciones |
| 11 | Graph RAG | Valor comprobado de las relaciones del grafo |
| 12 | Multiagente | Selección correcta y límites de ejecución |
| 13 | Evaluación ampliada | Comparación de calidad, tiempo y coste |

Aunque la evaluación formal aparece en el Experto, definir criterios desde el inicio
ayuda a saber si una ampliación aporta valor o introduce errores.

Para cada unidad: definir una entrada y salida de ejemplo, implementar un cambio pequeño,
probarlo, explicar lo aprendido, actualizar documentación y guardar un commit descriptivo.
Completar todas las capacidades de un nivel antes de darlo por terminado: una función
destacada del siguiente nivel no sustituye a las demás condiciones de entrega.

## Referencias oficiales

Las herramientas, cuotas y APIs evolucionan. Consultar documentación vigente antes
de implementar la hoja de ruta. Los pasos anteriores son propuestas para este proyecto.

- [Python: entornos virtuales](https://docs.python.org/3/library/venv.html)
- [Streamlit](https://docs.streamlit.io/)
- [ChatGroq en LangChain](https://docs.langchain.com/oss/python/integrations/chat/groq)
- [Groq: inicio rápido](https://console.groq.com/docs/quickstart)
- [Groq: modelos](https://console.groq.com/docs/models)
- [Groq: límites](https://console.groq.com/docs/rate-limits)
- [Docker: buenas prácticas](https://docs.docker.com/build/building/best-practices/)
- [LangSmith: observabilidad](https://docs.langchain.com/langsmith/observability)
- [arXiv: manual de su API](https://info.arxiv.org/help/api/user-manual.html)
- [LangChain: recuperación de información](https://docs.langchain.com/oss/python/deepagents/retrieval)
- [LangChain: multiagente](https://docs.langchain.com/oss/python/langchain/multi-agent)
- [LangChain: guardarraíles](https://docs.langchain.com/oss/python/langchain/guardrails)
