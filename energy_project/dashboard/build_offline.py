import base64
from pathlib import Path


dashboard = Path(__file__).resolve().parent
html = (dashboard / "index.html").read_text(encoding="utf-8")
data = (dashboard / "data.json").read_text(encoding="utf-8").replace("<", "\\u003c")
image = base64.b64encode((dashboard / "shap_summary.png").read_bytes()).decode("ascii")
image_url = "data:image/png;base64," + image

start = "/* DATA_LOADER_START */"
end = "/* DATA_LOADER_END */"
before, rest = html.split(start, 1)
_, after = rest.split(end, 1)
html = before + start + "\nD=" + data + ";shell();\n" + end + after
html = html.replace("./shap_summary.png", image_url)

output = dashboard.parent / "dashboard_offline.html"
output.write_text(html, encoding="utf-8")
print(output, output.stat().st_size, "bytes")
