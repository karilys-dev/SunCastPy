"""Module that exports to file"""

import json
import logging
from pathlib import Path
from typing import Any, Callable

logger = logging.getLogger(__name__)


def export_file(
    data: Any,
    output_dir: Path,
    name: str,
    writer: Callable,
) -> None:
    """Export data using a provided writer function."""

    output_dir.mkdir(parents=True, exist_ok=True)
    data_file = output_dir / name

    with open(data_file, "w", encoding="utf-8") as file:
        writer(file, data)

    logger.info("File was successfully exported.")


def export_html(data: str, output_dir: Path, name: str) -> None:
    """Export data as html

    Args:
        data (str): contents of the html file
        output_dir (Path): Location where the file will be saved
        name (str): Name of the html file
    """
    export_file(
        data,
        output_dir,
        name,
        lambda file, data: file.write(data),
    )


def export_json(data: dict, output_dir: Path, name: str) -> None:
    """Export data as json

    Args:
        data (dict): Contents of the json file
        data_file (Path): Name and full path to json file
    """
    export_file(
        data,
        output_dir,
        name,
        lambda file, data: json.dump(data, file, indent=4),
    )
