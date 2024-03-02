from bs4 import BeautifulSoup
import requests


req = requests.get("https://bindingofisaacrebirth.fandom.com/wiki/All_Bosses_(Bosses)")

page = BeautifulSoup(req.text, "lxml")

images = page.find_all(lambda tag: tag.name == "img" and "Boss " in tag["alt"])[:-2]

for img in images:
    image_url = img["data-src"]
    image_name = img["alt"].split('Boss')[1].replace('ingame','').replace('portrait','').strip()
    image_request = requests.get(image_url)

    with open(f"./original/{image_name}.png", "wb") as file:
        file.write(image_request.content)