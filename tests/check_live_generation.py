"""Prueba manual con Groq: ejecutarla consume cuota de la API (cuatro llamadas)."""

import argparse
import re
import sys

from streamlit.testing.v1 import AppTest


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--platforms", nargs="+",
        choices=["Blog", "LinkedIn", "Instagram", "Twitter/X"],
        default=["Blog", "LinkedIn", "Instagram", "Twitter/X"],
    )
    args = parser.parse_args()
    for platform in args.platforms:
        app = AppTest.from_file("../app.py", default_timeout=180).run()
        app.text_area[0].set_value("Cómo empezar a aprender programación con Python")
        app.text_input[0].set_value("Personas adultas sin experiencia en programación")
        app.selectbox[0].select(platform)
        app.selectbox[1].select("Cercano")
        app.button[0].click().run()

        if app.exception or app.error:
            print(f"{platform}: ERROR; no se obtuvo una respuesta.", flush=True)
            raise SystemExit(1)

        result = app.session_state["result"]
        content = result["content"]
        print(f"\n--- {platform} ---", flush=True)
        print(content, flush=True)
        print(
            f"Palabras: {len(content.split())}; caracteres: {len(content)}; "
            f"hashtags: {len(re.findall(r'#\w+', content))}",
            flush=True,
        )
        assert any(m.value == content for m in app.markdown)
        app.run()
        assert any(m.value == content for m in app.markdown)
        print("Respuesta visible y conservada al recargar la interfaz.", flush=True)


if __name__ == "__main__":
    main()
