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
    data_file = Path(output_dir).joinpath(name)

    with open(data_file, "w", encoding="utf-8") as file:
        file.write(data)
    logging.info("File was successfully exported.")


def export_json(data: dict, output_dir: Path, name: str) -> None:
    """Export data as json

    Args:
        data (dict): Contents of the json file
        data_file (Path): Name and full path to json file
    """
    data_file = Path(output_dir).joinpath(name)

    with open(data_file, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)  # noqa: F821
    logging.info("File was successfully exported.")
