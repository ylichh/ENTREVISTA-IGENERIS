from openai import OpenAI


class DalleTools:

    def get_tools(self) -> list:
        def generate_tourism_ad(prompt: str) -> str:
            """Genera una imagen publicitaria turística con DALL-E 3. Devuelve la URL."""
            response = OpenAI().images.generate(
                model="dall-e-3",
                prompt=prompt,
                n=1,
                size="1024x1024",
            )
            return response.data[0].url

        return [generate_tourism_ad]


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()

    tool = DalleTools().get_tools()[0]
    url = tool("A photorealistic tourism ad for Madagascar targeting German adventure travelers, lush rainforest with lemurs, lifestyle photography style")
    print(url)
