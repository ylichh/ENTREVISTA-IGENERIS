import json
from pathlib import Path

from src.use_cases.port.memory_handler import MemoryHandler

STATE_PATH = Path("src/memory/autogen_state.json")


class InMemoryAutogenHandler(MemoryHandler):

    def __init__(self) -> None:
        STATE_PATH.parent.mkdir(parents=True, exist_ok=True)

    def get_state(self) -> dict:
        print(f"Cargando estado desde la ruta {STATE_PATH}")
        if not STATE_PATH.exists():
            return {}
        return json.loads(STATE_PATH.read_text(encoding="utf-8"))

    def update_state(self, state: dict) -> None:
        print(f"Persistiendo estado: {state} en la ruta {STATE_PATH}")
        STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")

    def add(self, message) -> None:
        raise NotImplementedError("AutoGen usa update_state() para persistir el estado completo.")
