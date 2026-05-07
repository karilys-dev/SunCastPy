import json
from pathlib import Path

from SunCastPy.utils import export_file


def test_json_export(tmp_path):
    json_data = {"temp": 80, "location": "PR", "periods": [1, 2, 3]}
    output_file = tmp_path / "example.json"

    export_file.export_json(json_data, tmp_path, output_file.name)
    content = json.loads(output_file.read_text())

    assert output_file.exists()
    assert "location" in content
    assert isinstance(content["periods"], list)


def test_export_html(tmp_path: Path) -> None:
    html_data = "<h1>Hello World</h1>"
    output_file = tmp_path / "index.html"

    export_file.export_html(data=html_data, output_dir=tmp_path, name=output_file.name)

    assert output_file.exists()
    assert output_file.read_text(encoding="utf-8") == html_data
