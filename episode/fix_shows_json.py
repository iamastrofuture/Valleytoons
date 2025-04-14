import os
import json

folder = "."  # Your working directory
json_file = "shows.json"

# Load existing JSON
if os.path.exists(json_file):
    with open(json_file, "r") as f:
        shows = json.load(f)
else:
    shows = {}

updated_shows = {}

# Process HTML filenames
for file in os.listdir(folder):
    if file.endswith(".html") and file.startswith("episode_"):
        parts = file.replace(".html", "").split("_")
        if len(parts) < 4:
            continue

        episode_number = int(parts[1])
        title = parts[2]
        if len(parts) > 4:
            # Merge titles with underscores (like gangsta_night)
            title = "_".join(parts[2:-1])
        subdub = parts[-1]

        # Create standardized key
        key = f"{title.replace('_', ' ')} {subdub} episode {episode_number}".lower()

        # Add from existing or create blank
        if key in shows:
            updated_shows[key] = shows[key]
        else:
            print(f"Adding missing key: {key}")
            updated_shows[key] = {
                "title": title.replace('_', ' ').title(),
                "episode": episode_number,
                "subdub": "subbed" if subdub == "sub" else "dubbed",
                "iframe": "",  # Leave blank for now
                "series_slug": title.lower().replace(' ', '_'),
                "subdub_slug": subdub
            }

# Save fixed JSON
with open(json_file, "w") as f:
    json.dump(updated_shows, f, indent=2)

print(f"\n✅ Updated '{json_file}' with {len(updated_shows)} entries.")
