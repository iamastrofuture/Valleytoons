import os
import re
from bs4 import BeautifulSoup

# Regular expression to match filenames like "episode_8_gangsta_sub.html"
pattern = re.compile(r"episode_(\d+)_([a-z]+)_(subbed|dubbed|sub|dub)\.html", re.IGNORECASE)

folder = os.getcwd()  # Current folder, should be your episode folder

for filename in os.listdir(folder):
    if filename.endswith(".html") and filename.lower().startswith("episode_"):
        filepath = os.path.join(folder, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")
        
        # Check if a meta tag with name "episode-id" already exists
        if soup.find("meta", {"name": "episode-id"}):
            print(f"Meta tag already exists in {filename}")
            continue
        
        match = pattern.match(filename)
        if not match:
            print(f"Filename didn't match expected pattern: {filename}")
            continue

        ep_num, show_raw, typ_raw = match.groups()
        # Remove any leading zeros and normalize
        ep_num_int = int(ep_num)
        # Use "subbed" if type contains "sub", otherwise "dubbed"
        typ_norm = "subbed" if "sub" in typ_raw.lower() else "dubbed"
        lookup_key = f"{show_raw.lower()} {typ_norm} episode {ep_num_int}"
        
        # Create a new meta tag using the 'attrs' parameter.
        new_meta = soup.new_tag("meta", attrs={"name": "episode-id", "content": lookup_key})
        
        # Insert the new meta tag into the head. Create a head if none exists.
        if soup.head:
            soup.head.append(new_meta)
        else:
            head_tag = soup.new_tag("head")
            head_tag.append(new_meta)
            soup.insert(0, head_tag)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(soup.prettify())
            
        print(f"Added meta tag to {filename} with content: {lookup_key}")