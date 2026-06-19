# fetch_vnoi.py

import re
import json
import requests

USERNAME = "minhthaihuu304"

html = requests.get(
    f"https://oj.vnoi.info/user/{USERNAME}",
    headers={"User-Agent": "Mozilla/5.0"}
).text

match = re.search(
    r'window\.init_submission_table\(\s*\$,\s*(\{.*?\})\s*,',
    html,
    re.S
)

if not match:
    raise RuntimeError("Could not find submission data")

data = json.loads(match.group(1))

with open("contributions.json", "w") as f:
    json.dump(data, f, indent=2)

print(f"Found {len(data)} active days")
