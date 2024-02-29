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
            item = {
                "name": item_name,
                "image": "",
                "quote": "",
                "id": "0.0.0",
                "tier": 0,
                "character": "",
                "transformations": [],
                "pools": [],
            }

            if item_name == "<3":
                item_name = "Less Than Three"

            url = f"https://bindingofisaacrebirth.fandom.com/wiki/{urllib.parse.quote(item_name)}"
            req = requests.get(url=url)

            item_page = BeautifulSoup(req.text, "lxml")
            item_card = item_page.find("aside")

            item_pools = item_card.find("div", {"data-source": "alias"})
            item_id = item_card.find("div", {"data-source": "id"}).find("code")
            item_image = item_card.find("div", {"data-source": "image"}).find(
                "img", alt="Item icon"
            )
            item_quote = item_card.find("div", {"data-source": "quote"}).find("div")
            item_tier = item_card.find_all("img", alt="Item quality full")
            item_tags = item_card.find("div", {"data-source": "tags"})
            item_unlock = item_card.find("div", {"data-source": "unlocked by"})

            item["id"] = item_id.text.strip()
            item["image"] = item_image["data-src"]
            item["quote"] = item_quote.text.replace('"', "").strip()
            item["pools"] = self.get_item_pool(pools=item_pools)
            item["tier"] = len(item_tier)
            item["tags"] = self.get_item_tags(item_tags)
            item["transformations"] = self.get_item_transformation(item["tags"])
            item["character"] = self.get_starting_character(item_page)
            item["unlock_method"] = self.get_unlock_method(item_unlock)

            return item
        except Exception as e:
            print(f"An error has occured with item: {item_name}\nError: {str(e)}")

    def get_item_pool(self, pools):
        pool_items = pools.find_all("li")
        return (
            [pool_item.find_all("a")[-1]["title"] for pool_item in pool_items]
            if pool_items != None
            else []
        )

    def get_starting_character(self, page):
        name_element = page.find(
            lambda tag: tag.name == "li" and "starts with this item" in tag.text
        )
        return name_element.find_all("a")[-1].text if name_element != None else "None"

    def get_item_tags(self, tags):
        if tags == None:
            return []

        return [tag["alt"] for tag in tags.find_all("img")]

    def get_unlock_method(self, unlock_section):
        if unlock_section != None:
            return unlock_section.find("div").text.strip()

        return "None"

    def get_item_transformation(self, tags):
        if tags == None:
            return []
        transformations = []

        for tag in tags:
            if "transformation" in tag:
                transformations.append(tag.split("transformation")[0].strip())

        return transformations


def write():
    t = Scrapper()

    items = {"passives": [], "actives": []}

    actives = t.actives
    passives = t.passives

    for active in range(len(actives)):
        items["actives"].append(t.get_item(actives[active]))
        print(f"{active}. {actives[active]} was scrapped.")

    for passive in range(len(passives)):
        items["passives"].append(t.get_item(passives[passive]))
        print(f"{passive}. {passives[passive]} was scrapped.")

    with open("items.json", "w") as f:
        f.write(json.dumps(items, indent=4))


if __name__ == "__main__":
    write()
