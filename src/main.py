import os

from dotenv import load_dotenv

load_dotenv()


def main_autogen():
    from src.config import create_iterate_analysis

    use_case = create_iterate_analysis()
    question = "¿A quién podría vender experiencias turísticas en Andalucía?"
    print("=== Autogen: análisis de demanda turística ===\n")
    response = use_case.execute(question)
    print(response)


def main_langchain():
    from src.app_config import create_iterate_analysis

    use_case = create_iterate_analysis()
    question = "¿A quién podría vender experiencias turísticas en Lima? necesito ademas las regiones de ese pais en concreto de donde vienen las consultas"
    print("=== LangChain: análisis turístico ===\n")
    response = use_case.execute(question)
    print(response)


if __name__ == "__main__":
    handler = os.environ.get("CHAT_HANDLER", "langchain")
    if handler == "autogen":
        main_autogen()
    else:
        main_langchain()
