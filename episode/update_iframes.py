import os
import json
import re
from bs4 import BeautifulSoup

# Load JSON data from shows.json
with open("shows.json", "r", encoding="utf-8") as f:
    shows = json.load(f)

# Regular expression to match file names.
# Expected filename format: episode_<number>_<show>_<type>.html
pattern = re.compile(r"episode_(\d+)_([a-z]+)_(subbed|dubbed|sub|dub)\.html", re.IGNORECASE)

# Iterate over each HTML file in the current directory
for filename in os.listdir():
    if filename.endswith(".html") and filename.lower().startswith("episode_"):
        match = pattern.match(filename)
        if not match:
            print(f"Filename didn't match expected pattern: {filename}")
            continue
        ep_num, show_name, type_str = match.groups()
        # Normalize: convert to lowercase and remove any leading zeros on episode number
        ep_key = f"{show_name.lower()} {'subbed' if 'sub' in type_str.lower() else 'dubbed'} episode {int(ep_num)}"
        
        if ep_key in shows:
            iframe_url = shows[ep_key]["iframe"]
            if not iframe_url:
                print(f"No iframe URL provided for key: {ep_key} in file {filename}")
                continue
            filepath = os.path.join(os.getcwd(), filename)
            with open(filepath, "r", encoding="utf-8") as file:
                soup = BeautifulSoup(file, "html.parser")
            iframe = soup.find("iframe")
            if iframe:
                old_url = iframe.get("src", "")
                iframe["src"] = iframe_url
                with open(filepath, "w", encoding="utf-8") as file:
                    file.write(soup.prettify())
                print(f"✅ Updated {filename}: {old_url} -> {iframe_url}")
            else:
                print(f"❌ No iframe found in {filename}")
        else:
            print(f"❌ Lookup key not found: {ep_key} (from file {filename})")