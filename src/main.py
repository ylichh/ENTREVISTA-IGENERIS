import os

from dotenv import load_dotenv

load_dotenv()


def main_autogen(host: str, port: int):
    from src.autogen_config import create_iterate_analysis
    from src.fastapi_controller.controller import AnalysisController

    use_case = create_iterate_analysis()
    AnalysisController(use_case=use_case).run(host=host, port=port)


def main_langchain(host: str, port: int):
    from src.langchain_config import create_iterate_analysis
    from src.fastapi_controller.controller import AnalysisController

    use_case = create_iterate_analysis()
    AnalysisController(use_case=use_case).run(host=host, port=port)


if __name__ == "__main__":
    handler = os.environ.get("CHAT_HANDLER", "langchain")
    host = os.environ.get("API_HOST", "0.0.0.0")
    port = int(os.environ.get("API_PORT", "8000"))
    if handler == "autogen":
        main_autogen(host=host, port=port)
    else:
        main_langchain(host=host, port=port)