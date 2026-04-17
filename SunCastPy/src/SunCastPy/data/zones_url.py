import json
from pathlib import Path

json_file = Path(__file__).as_posix().removesuffix("py") + "json"
with open(json_file, mode="r", encoding="utf-8") as fp:
    SJU_ZONES: dict[str, dict[str, str]] = json.load(fp)
