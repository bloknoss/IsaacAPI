from bs4 import BeautifulSoup
import requests


req = requests.get("https://bindingofisaacrebirth.fandom.com/wiki/All_Bosses_(Bosses)")

page = BeautifulSoup(req.text, "lxml")

images = page.find_all(lambda tag: tag.name == "img" and "Boss " in tag["alt"])

images = [(image["data-src"]) for image in images][:-2]


#TODO: Download the images