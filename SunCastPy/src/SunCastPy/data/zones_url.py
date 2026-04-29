"""Module that returns the data of Puerto Rico zones"""

from pathlib import Path

from SunCastPy.utils.utils import get_json_data

json_file = Path(__file__).parent
name = Path(__file__).stem
SJU_ZONES: dict[str, dict[str, str]] = get_json_data(json_file.joinpath(name + ".json"))
SJU_ZONES_GROUPED: dict[str, dict[str, str]] = get_json_data(
    json_file.joinpath(name + "_grouped.json")
)
