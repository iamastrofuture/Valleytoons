import os
import json

# Load show data
with open("shows.json", "r") as f:
    shows = json.load(f)

# Create output folders
os.makedirs("output", exist_ok=True)
os.makedirs("output/episodes", exist_ok=True)
os.makedirs("output/shows", exist_ok=True)

# HTML templates
episode_template = """<!DOCTYPE html>
<html>
<head>
    <title>{title}</title>
    <style>
        body {{ font-family: Arial; background: #0d0d0d; color: white; text-align: center; }}
        iframe {{ width: 90%; height: 500px; margin-top: 20px; }}
        a {{ color: #00ffff; }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    <iframe src="{video_url}" frameborder="0" allowfullscreen></iframe>
    <p><a href="../shows/{show_slug}.html">Back to Show</a></p>
</body>
</html>
"""

show_template = """<!DOCTYPE html>
<html>
<head>
    <title>{show_name}</title>
    <style>
        body {{ font-family: Arial; background: #1a1a1a; color: white; }}
        ul {{ list-style: none; padding: 0; }}
        li {{ margin: 10px 0; }}
        a {{ color: #00ffff; text-decoration: none; }}
    </style>
</head>
<body>
    <h1>{show_name}</h1>
    <ul>
        {episode_links}
    </ul>
    <p><a href="../index.html">Back to Home</a></p>
</body>
</html>
"""

home_template = """<!DOCTYPE html>
<html>
<head>
    <title>ValleyToons</title>
    <style>
        body {{ font-family: Arial; background: #111; color: white; }}
        .search-bar {{ text-align: center; margin: 20px; }}
        .grid {{ display: flex; flex-wrap: wrap; justify-content: center; }}
        .card {{ margin: 10px; text-align: center; }}
        img {{ width: 200px; border-radius: 8px; }}
        a {{ color: #00ffff; text-decoration: none; }}
    </style>
</head>
<body>
    <div class="search-bar">
        <input type="text" id="searchInput" placeholder="Search shows..." onkeyup="filterShows()" style="padding: 10px; width: 50%;">
    </div>
    <div class="grid" id="showGrid">
        {show_cards}
    </div>
    <script>
        function filterShows() {{
            var input = document.getElementById('searchInput').value.toLowerCase();
            var cards = document.querySelectorAll('.card');
            cards.forEach(card => {{
                const text = card.innerText.toLowerCase();
                card.style.display = text.includes(input) ? 'block' : 'none';
            }});
        }}
    </script>
</body>
</html>
"""

# Build pages
show_cards = ""

for show_name, data in shows.items():
    show_slug = show_name.lower().replace(" ", "_")
    episode_links_html = ""

    for ep_name, url in data["episodes"].items():
        ep_slug = ep_name.lower().replace(" ", "_") + "_" + show_slug
        ep_filename = f"{ep_slug}.html"

        # Generate episode page
        with open(f"output/episodes/{ep_filename}", "w") as ep_file:
            ep_file.write(episode_template.format(
                title=f"{show_name} - {ep_name}",
                video_url=url,
                show_slug=show_slug
            ))

        episode_links_html += f'<li><a href="../episodes/{ep_filename}">{ep_name}</a></li>\n'

    # Generate show page
    with open(f"output/shows/{show_slug}.html", "w") as show_file:
        show_file.write(show_template.format(
            show_name=show_name,
            episode_links=episode_links_html
        ))

    show_cards += f'''
    <div class="card">
        <a href="shows/{show_slug}.html">
            <img src="{data['thumbnail']}" alt="{show_name}"><br>
            {show_name}
        </a>
    </div>
    '''

# Generate homepage
with open("output/index.html", "w") as home_file:
    home_file.write(home_template.format(show_cards=show_cards))

print("Site built successfully in the 'output' folder.")