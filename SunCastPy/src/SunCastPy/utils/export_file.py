"""Module that exports to file"""

import json
import logging
from pathlib import Path


def _convert_path(path_name: Path | str) -> Path:
    """Verify if its a Path object otherwise convert it."""
    if not isinstance(path_name, Path):
        return Path(path_name)
    return path_name


def export_html(data: str, output_dir: Path, name: str) -> None:
    """Export data as html

    Args:
        data (str): contents of the html file
        output_dir (Path): Location where the file will be saved
        name (str): Name of the html file
    """
    output_dir = _convert_path(output_dir)
    output_dir.mkdir(exist_ok=True, parents=True)

    (output_dir / name).write_text(data)


def export_json(data: dict, output_dir: Path, name: str) -> None:
    """Export data as json

    Args:
        data (dict): Contents of the json file
        data_file (Path): Name and full path to json file
    """
    data_file = _convert_path(output_dir).joinpath(name)

    with open(data_file, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)  # noqa: F821
    logging.info("File was successfully updated.")
