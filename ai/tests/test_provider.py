from django.test import TestCase
from openai import OpenAI
from decouple import config


class OpenRouterProviderTests(TestCase):

    def test_openrouter_provider_is_working(self):
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=config("OPENROUTER_API_KEY"),
        )

        response = client.chat.completions.create(
            model="openai/gpt-oss-20b:free",
            messages=[
                {
                    "role": "user",
                    "content": "Reply with exactly: OK"
                }
            ],
            temperature=0,
            stream=False
        )

        self.assertIsNotNone(response)

        answer = response.choices[0].message.content

        self.assertIn(
            "OK",
            answer.upper()
        )