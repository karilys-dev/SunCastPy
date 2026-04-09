from pathlib import Path


def create_htlm(data: str, output_dir: Path) -> None:

    output_dir.mkdir(exist_ok=True)

    (output_dir / "index.html").write_text(data)
