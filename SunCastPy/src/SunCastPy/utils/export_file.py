import json
import logging
from pathlib import Path


def create_htlm(data: str, output_dir: Path) -> None:

    output_dir.mkdir(exist_ok=True)

    (output_dir / "index.html").write_text(data)


def export_json(data, data_file) -> None:
    with open(data_file, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)  # noqa: F821
    logging.info("File was successfully updated.")
