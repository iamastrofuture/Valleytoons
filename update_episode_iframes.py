import os
import re
import json
from bs4 import BeautifulSoup

# Set folder paths (adjust if needed)
episode_folder = "episode"      # Folder where your episode HTML files are stored
json_path = "shows.json"          # JSON file with your correct iframe URLs

# Load your JSON data from shows.json
with open(json_path, "r", encoding="utf-8") as f:
    shows_data = json.load(f)

# Build a normalized lookup dictionary from the JSON.
# We'll map keys like "lazarus subbed episode 1" to the correct URL.
lookup = {}
for show_key, details in shows_data.items():
    # Determine the type and show name from show_key.
    # Example: "Lazarus Dubbed" becomes show_name = "Lazarus", typ = "Dubbed"
    parts = show_key.split()
    if len(parts) < 2:
        continue
    show_name = parts[0]
    typ = parts[1]
    episodes = details.get("episodes", {})
    for ep, url in episodes.items():
        # Create a lookup key in lowercase.
        lookup_key = f"{show_name} {typ} {ep}".lower()  # e.g., "lazarus dubbed episode 1"
        lookup[lookup_key] = url

# Mapping for file type strings in filenames
type_mapping = {
    "subbed": "Subbed",
    "sub": "Subbed",
    "dubbed": "Dubbed",
    "dub": "Dubbed"
}

# Define a regex pattern to match filenames.
# This expects filenames like: episode_1_lazarus_subbed.html
pattern = re.compile(r"episode_(\d+)_([a-z]+)[_-](subbed|dubbed|sub|dub)\.html", re.IGNORECASE)

# Iterate over each HTML file in the episode folder
for filename in os.listdir(episode_folder):
    if not filename.endswith(".html"):
        continue
    filepath = os.path.join(episode_folder, filename)
    match = pattern.match(filename)
    if not match:
        print(f"⚠️ Skipping file (pattern mismatch): {filename}")
        continue

    ep_num, show_raw, type_raw = match.groups()
    ep_num_int = int(ep_num)  # remove leading zeros
    # Convert show name: e.g., "lazarus" → "Lazarus"
    show_name_norm = show_raw.capitalize()
    # Convert type using mapping
    typ_norm = type_mapping.get(type_raw.lower(), type_raw.capitalize())

    # Build lookup key: e.g., "lazarus subbed episode 1"
    lookup_key = f"{show_name_norm} {typ_norm} Episode {ep_num_int}".lower()

    if lookup_key in lookup:
        new_url = lookup[lookup_key]
    else:
        print(f"❌ Lookup key not found for: {lookup_key} (from file {filename})")
        continue

    # Open and parse the HTML file
    with open(filepath, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    # Find the iframe tag – assume there's one iframe in the file
    iframe_tag = soup.find("iframe")
    if not iframe_tag:
        print(f"❌ No iframe tag found in {filename}")
        continue

    # Update the iframe's src attribute with the new URL
    old_url = iframe_tag.get("src", "no src")
    iframe_tag["src"] = new_url

    # Write the updated HTML back to the file
    with open(filepath, "w", encoding="utf-8") as file:
        file.write(str(soup.prettify()))

    print(f"✅ Updated {filename}: {old_url} -> {new_url}")