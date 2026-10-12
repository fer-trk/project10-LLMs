# De un formulario a un texto publicable: una POC de generación de contenido con Python y un LLM

Publicado en [Medium](https://medium.com/@fernandatorokpolito/de-un-formulario-a-un-texto-publicable-una-poc-de-generaci%C3%B3n-de-contenido-con-python-y-un-llm-bfc714f81044).

## Cómo construimos una aplicación educativa con Streamlit, LangChain y Groq

Un mismo tema puede convertirse en un artículo de blog, una publicación de LinkedIn,
un copy de Instagram o un texto para Twitter/X. Sin embargo, cambiar el nombre de la
plataforma no basta: también tienen que cambiar la extensión, la estructura y la
forma de dirigirse al público.

Ese fue el punto de partida de este proyecto de bootcamp: crear una prueba de concepto
de generación de contenido que permita indicar un tema, una plataforma, una audiencia
y un tono, y obtener un texto adaptado a esas decisiones.

El código está disponible en [GitHub](https://github.com/fer-trk/project10-LLMs).

## Un alcance que se puede construir y explicar

El briefing proponía distintos niveles de complejidad. Con un plazo de dos días,
elegimos concentrarnos en el nivel esencial: generación de texto mediante prompts,
una interfaz web y documentación suficiente para instalar y comprender la aplicación.

La POC utiliza Python, Streamlit para la interfaz y LangChain para comunicarse con
un único modelo servido por Groq: `openai/gpt-oss-20b`. No entrenamos un modelo propio;
utilizamos uno existente y diseñamos las instrucciones que recibe.

La decisión de limitar el alcance nos permitió dedicar atención al objetivo educativo
principal: entender cómo los datos de un formulario se convierten en un prompt y cómo
ese prompt condiciona la respuesta del modelo.

## Tres archivos, tres responsabilidades

El funcionamiento se divide en tres piezas:

- `app.py` recoge los datos y muestra el resultado.
- `prompt_builder.py` construye las instrucciones de generación.
- `llm_service.py` envía el prompt al modelo y devuelve el texto.

El recorrido completo es formulario → prompt → LangChain → Groq → respuesta → interfaz.

Streamlit permite construir el formulario con componentes de Python. Agrupamos sus
campos en `st.form()` para que la generación se solicite al pulsar el botón, una vez
introducidos los parámetros. Antes de llamar al modelo, comprobamos que el tema y la
audiencia estén completos.

Esta separación facilita leer el proyecto: las reglas editoriales están en un lugar y
la comunicación con la API en otro. No hace falta una arquitectura más compleja para
explicar o modificar este recorrido.

## El prompt engineering es el centro del proyecto

La función `build_prompt()` combina el tema, la audiencia y el tono con instrucciones
específicas de la plataforma elegida. Estas son nuestras reglas iniciales:

- Blog: entre 500 y 700 palabras, título, introducción, secciones y conclusión.
- LinkedIn: entre 120 y 220 palabras, gancho inicial, párrafos breves, llamada a la
  conversación y entre 3 y 5 hashtags.
- Instagram: entre 80 y 150 palabras, inicio llamativo, saltos de línea, emojis con
  moderación, llamada a la acción y entre 5 y 8 hashtags.
- Twitter/X: una única publicación de hasta 280 caracteres, sin hilo y con un máximo
  de 2 hashtags.

Estos rangos son decisiones de diseño de nuestra POC, no una descripción de todos
los límites o formatos posibles de cada plataforma.

El prompt también pide redactar en castellano, adaptar el vocabulario a la audiencia,
mantener el tono y devolver únicamente el contenido final. Añadimos la instrucción
de no inventar estadísticas, estudios o citas. Esa instrucción orienta la respuesta,
pero no garantiza su exactitud: el texto sigue necesitando revisión humana.

Para hacer visible este proceso, la interfaz incluye la opción «Ver el prompt utilizado».
Así podemos comparar las instrucciones de dos plataformas usando exactamente el mismo
tema y observar qué cambió antes de enviar la petición.

## La conexión con el modelo

En `llm_service.py` utilizamos `ChatGroq`, la integración de LangChain con Groq. El
servicio crea el cliente, ejecuta `invoke(prompt)` y devuelve el contenido textual.
Configuramos una temperatura de 0,7, un timeout de 60 segundos por petición y hasta
dos reintentos. Los reintentos pueden aumentar el tiempo total de espera.

La clave de acceso se carga desde una variable de entorno. En desarrollo utilizamos
un archivo `.env`, cargado con `python-dotenv`, y lo excluimos de Git. El repositorio
incluye `.env.example` para explicar qué variables se necesitan sin compartir la clave.

Si falta la configuración o la llamada falla, la interfaz muestra un mensaje. Si la
generación termina correctamente, presenta el texto y permite descargarlo. Usamos
`st.session_state` para conservar el resultado cuando Streamlit vuelve a ejecutar
la página durante la misma sesión; esto no constituye un historial persistente.

## Qué comprobamos

Las siete pruebas automáticas verifican el constructor de prompts, los campos
obligatorios, el flujo de generación para las cuatro plataformas, la conservación
del resultado, el manejo de errores y el aviso de longitud para Twitter/X. En las
pruebas de interfaz simulamos las respuestas para que no dependan de una API externa.

Después hicimos una comprobación real con el tema «Cómo empezar a aprender programación
con Python», dirigida a personas adultas sin experiencia y con tono cercano. Los
resultados obtenidos fueron:

- Blog: 674 palabras, con título, secciones y conclusión.
- LinkedIn: 157 palabras, pregunta final y 5 hashtags.
- Instagram: 96 palabras, emojis y llamada a la acción.
- Twitter/X: 237 caracteres.

Las cuatro respuestas se visualizaron correctamente y permanecieron en la sesión.
Estas muestras cumplieron las extensiones solicitadas, pero no constituyen una
evaluación exhaustiva de la calidad del modelo. Otras peticiones pueden producir
resultados diferentes. Por eso la interfaz avisa cuando una respuesta para X supera
los 280 caracteres, en lugar de asumir que el prompt siempre se cumple.

## Lo que aprendimos

Una aplicación pequeña permite observar con claridad tres conceptos: los datos
del usuario, las instrucciones que guían al modelo y la respuesta que debe revisarse.
El valor de esta POC está en conectar esas piezas y hacer que el formato cambie según
el contexto de publicación.

También aprendimos a distinguir una petición de una garantía. Pedir un límite de
caracteres no asegura que el modelo lo respete; pedir que no invente datos tampoco
elimina los errores. Las comprobaciones y la revisión editorial siguen siendo parte
del trabajo.

El resultado es una base sencilla para demostrar generación de contenido y explicar
su funcionamiento durante una presentación técnica. Antes de ampliar el proyecto,
el siguiente paso sería probar más temas, audiencias y tonos, y ajustar los prompts
a partir de los resultados observados.

## Referencias

- [Código del proyecto](https://github.com/fer-trk/project10-LLMs)
- [Streamlit](https://docs.streamlit.io/)
- [Integración ChatGroq de LangChain](https://docs.langchain.com/oss/python/integrations/chat/groq)
- [Guía de inicio de Groq](https://console.groq.com/docs/quickstart)
