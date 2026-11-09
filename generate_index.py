import json
import pathlib
from build_parts.styles import CSS_STYLES
from build_parts.sections import get_sections_html
from build_parts.scripts import JS_SCRIPTS

BASE_DIR = pathlib.Path(r"C:\Users\Gayatri\OneDrive\Desktop\carbon-scheduler")
CHARTS_FILE = BASE_DIR / "data" / "charts_base64.json"
SUMMARY_FILE = BASE_DIR / "data" / "summary.json"
CARBON_REPLAY_FILE = BASE_DIR / "data" / "carbon_replay.json"
OUTPUT_HTML = BASE_DIR / "index.html"

with open(CHARTS_FILE, "r") as f:
    charts = json.load(f)

with open(SUMMARY_FILE, "r") as f:
    summary_data = json.load(f)

with open(CARBON_REPLAY_FILE, "r") as f:
    carbon_replay = json.load(f)

summary_json_str = json.dumps(summary_data)
carbon_replay_json_str = json.dumps(carbon_replay)

# Insert data into JS
js_content = JS_SCRIPTS.replace("__SUMMARY_JSON__", summary_json_str).replace("__CARBON_REPLAY_JSON__", carbon_replay_json_str)

sections_html = get_sections_html(charts)

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>CARBONFLOW — Carbon-Aware Serverless Function Scheduling on AWS</title>
  <meta name="description" content="Research project demonstration of carbon-aware serverless function scheduling across AWS regions. Student: Gayatri, B.Tech CS, 2026.">
  <style>
{CSS_STYLES}
  </style>
</head>
<body>

{sections_html}

  <script>
{js_content}
  </script>
</body>
</html>
"""

with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Successfully generated {OUTPUT_HTML} ({len(html_content)} bytes)")
