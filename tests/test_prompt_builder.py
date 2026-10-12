import unittest

from prompt_builder import PLATFORM_INSTRUCTIONS, build_prompt


class BuildPromptTests(unittest.TestCase):
    def test_prompt_contains_user_inputs(self):
        prompt = build_prompt(
            topic="Inteligencia artificial",
            platform="LinkedIn",
            audience="Estudiantes",
            tone="Divulgativo",
        )

        self.assertIn("Inteligencia artificial", prompt)
        self.assertIn("LinkedIn", prompt)
        self.assertIn("Estudiantes", prompt)
        self.assertIn("Divulgativo", prompt)

    def test_each_platform_adds_its_own_instruction(self):
        prompts = {
            platform: build_prompt("Tema", platform, "Audiencia", "Cercano")
            for platform in PLATFORM_INSTRUCTIONS
        }

        for platform, instruction in PLATFORM_INSTRUCTIONS.items():
            self.assertIn(instruction, prompts[platform])

        self.assertEqual(len(set(prompts.values())), len(PLATFORM_INSTRUCTIONS))

    def test_unsupported_platform_raises_error(self):
        with self.assertRaisesRegex(ValueError, "Plataforma no compatible"):
            build_prompt("Tema", "TikTok", "Audiencia", "Cercano")


if __name__ == "__main__":
    unittest.main()
