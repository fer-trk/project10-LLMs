import unittest
from unittest.mock import patch

from streamlit.testing.v1 import AppTest


class AppTests(unittest.TestCase):
    def test_empty_form_does_not_call_model(self):
        with patch("llm_service.generate_content") as generate:
            app = AppTest.from_file("../app.py").run()
            app.button[0].click().run()
            self.assertEqual(len(app.exception), 0)
            self.assertEqual(len(app.warning), 1)
            generate.assert_not_called()

    def test_generation_flow_for_each_platform(self):
        for platform in ["Blog", "LinkedIn", "Instagram", "Twitter/X"]:
            with self.subTest(platform=platform):
                with patch(
                    "llm_service.generate_content", return_value="Contenido de prueba"
                ) as generate:
                    app = AppTest.from_file("../app.py").run()
                    app.text_area[0].set_value("Aprender inteligencia artificial")
                    app.text_input[0].set_value("Estudiantes principiantes")
                    app.selectbox[0].select(platform)
                    app.button[0].click().run()
                    self.assertEqual(len(app.exception), 0)
                    self.assertEqual(len(app.error), 0)
                    self.assertIn(platform, generate.call_args.args[0])
                    self.assertTrue(
                        any(m.value == "Contenido de prueba" for m in app.markdown)
                    )
                    app.run()
                    self.assertTrue(
                        any(m.value == "Contenido de prueba" for m in app.markdown)
                    )
                    generate.assert_called_once()

    def test_x_warns_when_output_exceeds_limit(self):
        with patch("llm_service.generate_content", return_value="a" * 281):
            app = AppTest.from_file("../app.py").run()
            app.text_area[0].set_value("Aprender IA")
            app.text_input[0].set_value("Estudiantes")
            app.selectbox[0].select("Twitter/X")
            app.button[0].click().run()
            self.assertEqual(len(app.warning), 1)
            self.assertIn("281", app.warning[0].value)

    def test_service_failure_shows_friendly_error(self):
        with patch("llm_service.generate_content", side_effect=RuntimeError("test")):
            app = AppTest.from_file("../app.py").run()
            app.text_area[0].set_value("Aprender IA")
            app.text_input[0].set_value("Estudiantes")
            app.button[0].click().run()
            self.assertEqual(len(app.exception), 0)
            self.assertEqual(len(app.error), 1)


if __name__ == "__main__":
    unittest.main()
