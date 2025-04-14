import os
import json
import re

# Load the JSON database
with open("shows.json", "r") as f:
    data = json.load(f)

# Folder where episode HTML files are stored
episode_folder = "episode"

# Loop through files in the folder
for filename in os.listdir(episode_folder):
    if not filename.endswith(".html"):
        continue

    filepath = os.path.join(episode_folder, filename)

    # Match pattern like "episode_3_gangsta_-sub.html"
    match = re.match(r"episode_(\d+)_([a-z0-9]+)_-?(sub|dub)\.html", filename, re.IGNORECASE)
    if not match:
        print(f"⚠️ Skipped (filename didn't match expected format): {filename}")
        continue

    ep_num, show_name, lang = match.groups()
    show_key = f"{show_name.capitalize()} {'Sub' if lang.lower() == 'sub' else 'Dub'}"
    episode_key = f"Episode {ep_num}"

    # Look up the iframe URL
    try:
        iframe_url = data[show_key]["episodes"][episode_key]
    except KeyError:
        print(f"❌ No match for: {show_key} - {episode_key}")
        continue

    # Read and update the HTML file
    with open(filepath, "r") as f:
        content = f.read()

    # Replace iframe src
    updated_content = re.sub(
        r'<iframe.*?src=".*?".*?></iframe>',
        f'<iframe src="{iframe_url}" width="100%" height="100%" frameborder="0" allowfullscreen></iframe>',
        content,
        flags=re.DOTALL
    )

    with open(filepath, "w") as f:
        f.write(updated_content)

    print(f"✅ Updated: {filename}")