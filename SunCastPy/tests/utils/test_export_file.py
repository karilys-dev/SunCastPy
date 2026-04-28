import json
from pathlib import Path

from SunCastPy.utils import export_file


def test_json_export(tmp_path):
    json_data = {"temp": 80, "location": "PR", "periods": [1, 2, 3]}
    output_file = tmp_path / "example.json"
    export_file.export_json(json_data, tmp_path, output_file.name)
    assert output_file.exists()
    content = json.loads(output_file.read_text())
    assert "location" in content
    assert isinstance(content["periods"], list)


def test_convert_path():
    test_path = "/tmp/location"
    # pylint: disable=protected-access
    assert isinstance(export_file._convert_path(test_path), Path)
