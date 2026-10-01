from pathlib import Path


index_path = Path(__file__).resolve().parent / "build" / "web" / "index.html"
if not index_path.is_file():
    raise FileNotFoundError(f"Web build index not found: {index_path}")

html = index_path.read_text(encoding="utf-8")
default = "autorun : 0,"
enabled = "autorun : 1,"
default_count = html.count(default)
enabled_count = html.count(enabled)
if default_count == 1 and enabled_count == 0:
    html = html.replace(default, enabled, 1)
elif default_count != 0 or enabled_count != 1:
    raise RuntimeError("Expected exactly one pygbag autorun setting.")

index_path.write_text(html, encoding="utf-8")
