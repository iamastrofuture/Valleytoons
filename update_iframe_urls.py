import os
from bs4 import BeautifulSoup

# Define your shows and iframe URLs
video_urls = {
    "Lazarus Dub": {
        1: "https://iframe.mediadelivery.net/play/409377/f4c0f712-5a2a-4d2d-b399-1cae8528f5b4"
    },
    "Lazarus Sub": {
        1: "https://iframe.mediadelivery.net/play/409377/80c25c5f-7946-4fca-aa3a-8f7938a017fd"
    },
    "Gangsta Sub": {
        1: "https://iframe.mediadelivery.net/play/409607/dd6a3558-406b-4db1-b49b-36e4adfcc224",
        2: "https://iframe.mediadelivery.net/play/409607/dd6a3558-406b-4db1-b49b-36e4adfcc224",
        3: "https://iframe.mediadelivery.net/play/409607/deba9e53-9f72-4ccd-9e03-92b304a6d08e",
        4: "https://iframe.mediadelivery.net/play/409607/5bc5c6e4-0347-404f-a440-a3b6807865a4",
        5: "https://iframe.mediadelivery.net/play/409607/a8c086bf-e9c8-4090-aa21-16b74e60c813",
        6: "https://iframe.mediadelivery.net/play/409607/69052090-2286-4fdc-9f90-ea27a263c6c0",
        7: "https://iframe.mediadelivery.net/play/409607/684f8afb-8c9f-4f02-a0ca-c545284d319e",
        8: "https://iframe.mediadelivery.net/play/409607/2d14e925-e263-44f9-933d-84865e532678",
        9: "https://iframe.mediadelivery.net/play/409607/20aadb9e-ecc1-46df-bd0b-b26125ca8cd7",
        10: "https://iframe.mediadelivery.net/play/409607/962e1cd9-1c89-439a-8bbb-491fd7202146",
        11: "https://iframe.mediadelivery.net/play/409607/19dea156-0038-4c4e-bb0a-662d21549cb9",
        12: "https://iframe.mediadelivery.net/play/409607/2b7006ae-77c9-44e2-856b-36708e693f30",
    },
    "Gangsta Dub": {
        1: "https://iframe.mediadelivery.net/play/409609/7552b97e-98b4-4fec-b5fe-80ba36677e22",
        2: "https://iframe.mediadelivery.net/play/409609/415d8f73-6659-4c8e-8cbd-329cbf9a34e5",
        3: "https://iframe.mediadelivery.net/play/409609/8b649046-7344-4faf-a77d-ca9d142fcf75",
        4: "https://iframe.mediadelivery.net/play/409609/039d8750-4107-4d07-943f-cc027aacaf56",
        5: "https://iframe.mediadelivery.net/play/409609/f6512c69-b742-4b33-8dc3-025b461e71f8",
        6: "https://iframe.mediadelivery.net/play/409609/05d20a88-907b-4fb1-9b22-48f6aa4c3281",
        7: "https://iframe.mediadelivery.net/play/409609/92063e51-f91a-4c01-b3ee-55ec81cf549b",
        8: "https://iframe.mediadelivery.net/play/409609/f77c6e83-7154-4b9c-bb63-e33b9382d238",
        9: "https://iframe.mediadelivery.net/play/409609/fa2a1619-e692-4b0e-a3c6-d98ad296147c",
        10: "https://iframe.mediadelivery.net/play/409609/6ea99726-08e6-4a0a-a669-5e42e77418cc",
        11: "https://iframe.mediadelivery.net/play/409609/eecb62a9-1f0d-4474-b866-d91d7872433c",
        12: "https://iframe.mediadelivery.net/play/409609/775b3e54-f444-47b9-828a-4c016ce5241d",
    },
    "Erased Sub": {
        1: "https://iframe.mediadelivery.net/play/409611/e275cca8-5575-4e13-90e7-13501d2e4c4f",
        2: "https://iframe.mediadelivery.net/play/409611/acdaa675-dcc6-4750-9685-4006d8b37f80",
        3: "https://iframe.mediadelivery.net/play/409611/9c476fb3-a2af-471b-b2db-d9f5be82d170",
        4: "https://iframe.mediadelivery.net/play/409611/5f89f615-ce05-4145-8736-4e68dcf9a985",
        5: "https://iframe.mediadelivery.net/play/409611/3abb9782-7cf7-41fe-8b7b-5c72c7adf90d",
        6: "https://iframe.mediadelivery.net/play/409611/991de520-ec60-4efa-9719-5c7712992e33",
        7: "https://iframe.mediadelivery.net/play/409611/be377687-a0b8-466f-b9be-b5fbf99f9d31",
        8: "https://iframe.mediadelivery.net/play/409611/0d9e4052-8ad9-4391-8a03-818719c13e9c",
        9: "https://iframe.mediadelivery.net/play/409611/3cb4dc80-b578-4aa9-b8c0-7138678282d0",
        10: "https://iframe.mediadelivery.net/play/409611/563a3aee-fa73-4e2f-9121-8326199f00fe",
        11: "https://iframe.mediadelivery.net/play/409611/d03edd8e-4f55-4df2-b60f-837bfd1a0dad",
        12: "https://iframe.mediadelivery.net/play/409611/e2900fe3-72c0-4b54-b339-b440d6ef5ef0",
    },
}

# Update HTML files in your valleytoons project
def update_iframe_src(directory, show_dict):
    for show, episodes in show_dict.items():
        folder = show.replace(" ", "_").lower()
        for episode_num, new_url in episodes.items():
            ep_filename = f"episode{episode_num}.html"
            html_path = os.path.join(directory, folder, ep_filename)

            if not os.path.exists(html_path):
                print(f"Missing file: {html_path}")
                continue

            with open(html_path, "r") as file:
                soup = BeautifulSoup(file, "html.parser")

            iframe = soup.find("iframe")
            if iframe:
                old_src = iframe.get("src")
                iframe["src"] = new_url
                print(f"Updated {html_path}\n  {old_src} -> {new_url}")

                with open(html_path, "w") as file:
                    file.write(str(soup.prettify()))
            else:
                print(f"No iframe found in: {html_path}")

# Set path to the valleytoons folder on your Desktop
project_root = os.path.expanduser("~/Desktop/valleytoons")
update_iframe_src(project_root, video_urls)