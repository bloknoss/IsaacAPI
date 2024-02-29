from bs4 import BeautifulSoup
import json
import sys
import urllib
import requests


class Scrapper:
    def __init__(self) -> None:

        ITEMS_URL = "https://bindingofisaacrebirth.fandom.com/wiki/Items"
        req = requests.get(url=ITEMS_URL)

        self.bs = BeautifulSoup(req.text, "lxml")
        self.tables = self.bs.find_all("table")
        self.actives = self.get_table_items(self.tables[0])
        self.passives = self.get_table_items(self.tables[1])

    def get_table_items(self, table):
        items = []
        trs = table.find_all("tr")
        for item in trs:
            td = item.find("td")
            if td != None:
                items.append(td.text.strip())

        return items

    def get_item(self, item_name):
        try:
            item = {"name": item_name, "tier": 0, "description": "", "pools": []}
            if item_name == "<3":
                item_name = "Less Than Three"

            url = f"https://bindingofisaacrebirth.fandom.com/wiki/{urllib.parse.quote(item_name)}"
            req = requests.get(url=url)

            item_page = BeautifulSoup(req.text, "lxml")
            item_card = item_page.find("aside")
            item_card_sections = item_card.findAll(
                True,
                {"class": ["pi-item", "pi-data", "pi-item-spacing", "pi-border-color"]},
            )
            item_pools = item_card.find("div", class_="item-pool-list").find_all("li")
            item_tier = item_card.find_all("img", alt="Item quality full")

            item["pools"] = [pool.text.strip() for pool in item_pools]
            item["description"] = item_card_sections[2].find("div").text.strip("\"")
            item["tier"] = len(item_tier)

            return item
        except:
            print(item_name)

if __name__ == "__main__":
    t = Scrapper()
    passive_items = t.passives
    for item in range(len(passive_items)):
        (json.dumps(t.get_item(passive_items[item]), indent=4))
