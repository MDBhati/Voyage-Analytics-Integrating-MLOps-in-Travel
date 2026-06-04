from pathlib import Path

TEMPLATES_DIR = Path(__file__).resolve().parent
STATIC_DIR = TEMPLATES_DIR.parent / "static"


def load_template(template_name: str) -> str:
    template_path = TEMPLATES_DIR / template_name
    if not template_path.is_file():
        raise FileNotFoundError(f"Template not found: {template_path}")
    return template_path.read_text(encoding="utf-8")
