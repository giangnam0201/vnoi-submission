import sys
import re
import json
import requests
from datetime import datetime

def fetch_vnoi_activity(username):
    url = f"https://oj.vnoi.info/user/{username}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Error fetching VNOI profile: {response.status_code}")
        sys.exit(1)
        
    # Search for the init_submission_table call containing the data dictionary
    match = re.search(r'window\.init_submission_table\(\s*\$,\s*(\{.*?\})\s*,\s*"[a-z]{2}"\s*\);', response.text)
    if not match:
        print("Could not find submission data on the page.")
        sys.exit(1)
        
    data = json.loads(match.group(1))
    
    # Format data to a flat list of entries
    contributions = []
    for date_str, count in data.items():
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            contributions.append({"date": date_str, "count": count})
        except ValueError:
            continue
            
    # Write directly as a flat list
    with open("vnoi_contributions.json", "w") as f:
        json.dump(contributions, f)
    print(f"Successfully processed {len(contributions)} activity days for {username}.")
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fetch_vnoi.py <vnoi_username>")
        sys.exit(1)
    fetch_vnoi_activity(sys.argv[1])
