import os
import json
from bs4 import BeautifulSoup

# Path to your shows.json file (assumed to be in the same folder)
json_path = "shows.json"

# Load the JSON data from shows.json
with open(json_path, "r", encoding="utf-8") as f:
    shows = json.load(f)

# We'll process each HTML file in the current folder (which should be your episode folder)
folder = os.getcwd()

# Loop over each HTML file in the folder
for filename in os.listdir(folder):
    if filename.endswith(".html"):
        filepath = os.path.join(folder, filename)
        with open(filepath, "r", encoding="utf-8") as file:
            soup = BeautifulSoup(file, "html.parser")
        
        # Find the meta tag with the episode id
        meta_tag = soup.find("meta", {"name": "episode-id"})
        if not meta_tag:
            print(f"No meta tag found in {filename}")
            continue
        
        # Get the lookup key from the meta tag (should be like "gangsta subbed episode 8")
        key = meta_tag.get("content", "").strip()
        
        # Look up the correct iframe URL from the JSON
        if key in shows:
            new_url = shows[key]["iframe"]
        else:
            print(f"Lookup key '{key}' not found in shows.json for {filename}")
            continue
        
        # Find the <iframe> tag in the HTML
        iframe_tag = soup.find("iframe")
        if iframe_tag:
            old_url = iframe_tag.get("src", "")
            iframe_tag["src"] = new_url
            with open(filepath, "w", encoding="utf-8") as file:
                file.write(soup.prettify())
            print(f"Updated {filename}: {old_url} -> {new_url}")
        else:
            print(f"No <iframe> tag found in {filename}")