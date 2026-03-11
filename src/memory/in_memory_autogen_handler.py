import json
from pathlib import Path

from src.use_cases.port.memory_handler import MemoryHandler

STATE_DIR = Path("memory/autogen")


class InMemoryAutogenHandler(MemoryHandler):

    def __init__(self) -> None:
        STATE_DIR.mkdir(parents=True, exist_ok=True)

    def _path(self, conversation_id: str) -> Path:
        return STATE_DIR / f"{conversation_id}.json"

    def get_state(self, conversation_id: str) -> dict:
        path = self._path(conversation_id)
        print(f"[AutogenHandler] Cargando estado {conversation_id} desde {path}")
        if not path.exists():
            return {}
        return json.loads(path.read_text(encoding="utf-8"))

    def update_state(self, conversation_id: str, state: dict) -> None:
        path = self._path(conversation_id)
        print(f"[AutogenHandler] Persistiendo estado {conversation_id} en {path}")
        path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")

    def add(self, _message) -> None:
        raise NotImplementedError("AutoGen usa update_state() para persistir el estado completo.")
