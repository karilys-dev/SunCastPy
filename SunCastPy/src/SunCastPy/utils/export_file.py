"""Module that exports to file"""

import json
import logging
from pathlib import Path


def export_html(data: str, output_dir: Path, name: str) -> None:
    """Export data as html

    Args:
        data (str): contents of the html file
        output_dir (Path): Location where the file will be saved
        name (str): Name of the html file
    """
    if isinstance(output_dir, str):
        output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True, parents=True)

    (output_dir / name).write_text(data)


def export_json(data: str, data_file: Path) -> None:
    """Export data as json

    Args:
        data (str): Contents of the json file
        data_file (Path): Name and full path to json file
    """
    if isinstance(data_file, str):
        data_file = Path(data_file)

    with open(data_file, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)  # noqa: F821
    logging.info("File was successfully updated.")
