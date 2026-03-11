import os

from openai import OpenAI

from src.use_cases.port.chat_handler import ChatHandler

PROMPT_TEMPLATE = """Eres un publicista, debes crear una imagen publicitariaen funcion del
siguiente analisis, recuerda hacerlo en funcion del publico mas interesado en el destino en cuestion.

{analysis}

Style: lifestyle photography, vibrant colors, aspirational travel mood."""


class DalleHandler(ChatHandler):

    def handle(self, user_input: str, state) -> tuple[str, dict]:
        prompt = PROMPT_TEMPLATE.format(analysis=user_input)
        url = OpenAI(api_key=os.environ["OPENAI_API_KEY"]).images.generate(
            model="dall-e-3",
            prompt=prompt,
            n=1,
            size="1024x1024",
        ).data[0].url
        return url, {}
