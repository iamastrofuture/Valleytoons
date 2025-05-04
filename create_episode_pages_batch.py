import os
import json

# Folder to save HTML files
save_folder = "shows"
os.makedirs(save_folder, exist_ok=True)

# Load shows.json
with open("shows_batch.json", "r", encoding="utf-8") as f:
    shows = json.load(f)

# HTML template
html_template = """<!DOCTYPE html>
<html>
<head>
    <title>{show_title} - Episode {episode_num}</title>
    <style>
        body {{ font-family: Arial; background: #111; color: white; text-align: center; }}
        iframe {{ width: 80%; height: 500px; margin: 20px 0; border: none; border-radius: 8px; }}
        a.button {{ display: inline-block; margin: 10px; padding: 10px 20px; background: #00ffff; color: #111; border-radius: 5px; text-decoration: none; font-weight: bold; }}
        a.home-link {{ display: block; margin: 20px 0; color: #00ffff; }}
    </style>
</head>
<body>
    <h1>{show_title} - Episode {episode_num}</h1>

    <!-- 🔥 PASTE YOUR BUNNY STREAM DIRECT LINK BELOW INSIDE SRC="..." 🔥 -->
    <iframe src="<!-- PASTE BUNNY STREAM LINK HERE -->" allowfullscreen></iframe>

    <div style="margin-top: 20px;">
        {prev_button}
        {next_button}
    </div>

    <a class="home-link" href="../index.html">← Back to Home</a>
</body>
</html>
"""

for show in shows:
    show_name = show["show_name"]
    file_prefix = show["file_prefix"]
    num_episodes = show["num_episodes"]

    for ep_num in range(1, num_episodes + 1):
        prev_button = ""
        next_button = ""

        if ep_num > 1:
            prev_file = f"{file_prefix}_ep{ep_num-1}.html"
            prev_button = f'<a class="button" href="{prev_file}">Previous Episode</a>'
        if ep_num < num_episodes:
            next_file = f"{file_prefix}_ep{ep_num+1}.html"
            next_button = f'<a class="button" href="{next_file}">Next Episode</a>'

        # Fill in the HTML
        html_content = html_template.format(
            show_title=show_name,
            episode_num=ep_num,
            prev_button=prev_button,
            next_button=next_button
        )

        # Save the file
        file_name = f"{file_prefix}_ep{ep_num}.html"
        file_path = os.path.join(save_folder, file_name)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        print(f"✅ Created: {file_path}")

print("\n🎯 All episode pages created! Now just paste the Bunny Stream links inside each file.")