from discordwebhook import Discord
import json

from keys import discord_webhooks


class Shoe:
    def __init__(self, site, name, url, price, img, sizes):
        self.site = site
        self.name = name
        self.url = url
        self.img = img
        self.price = price
        self.sizes = sizes

    def json(self):
        return {
            "name": self.name,
            "url": self.url,
            "img": self.img,
            "price": self.price,
            "sizes": self.sizes,
            "stock": "In Stock"
        }

    def discord_message(self):
        for webhook in discord_webhooks[self.site]:
            discord = Discord(url=webhook)
            discord.post(embeds=[
                    {
                        "color": 0x00ff00,
                        "type": "rich",
                        "url": self.url,

                        "author": {
                            "name": self.site,
                            "url": self.url,
                        },

                        "title": "New Shoe Listed!",
                        "description": f"New shoe has been listed on {self.site}",

                        "fields": [
                            {"name": "Product Name", "value": self.name, "inline": True},
                            {"name": "Price", "value": f"{self.price} ILS", "inline": True},
                            {"name": "Status", "value": "In Stock"},
                            {"name": "Sizes", "value": f"{' '.join(self.sizes)}"},
                        ],

                        "thumbnail": {"url": f"{self.img}"},

                        "footer": {
                            "text": "SneakMonitor by Ori Friedman",
                        },
                    }
                ],
            )

    def update(self):
        with open("./data.json", 'r+') as file:
            file_data = json.load(file)
            file_data[self.site].append(self.json())
            file.seek(0)
            file.truncate()
            json.dump(file_data, file, indent=4)

    def update_sizes(self, sizes):
        with open("./data.json", 'r+') as file:
            file_data = json.load(file)
            for shoe in file_data[self.site]:
                if shoe["url"] == self.url:
                    shoe["sizes"] = sizes
                    break
            file.seek(0)
            file.truncate()
            json.dump(file_data, file, indent=4)

    def update_sizes_message(self, added_sizes, removed_sizes):
        for webhook in discord_webhooks[self.site]:
            discord = Discord(url=webhook)
            discord.post(embeds=[
                    {
                        "color": 0x00ff00,
                        "type": "rich",
                        "url": self.url,

                        "author": {
                            "name": self.site,
                            "url": self.url,
                        },

                        "title": "Sizes Updated!",
                        "description": f"Sizes have been updated on {self.site}",

                        "fields": [
                            {"name": "Product Name", "value": self.name, "inline": True},
                            {"name": "Price", "value": f"{self.price} ILS", "inline": True},
                            {"name": "Status", "value": "In Stock"},
                            {"name": "Added Sizes", "value": f"{' '.join(added_sizes)}", "inline": True},
                            {"name": "Removed Sizes", "value": f"{' '.join(removed_sizes)}", "inline": True},
                            {"name": "Sizes", "value": f"{' '.join(self.sizes)}"},
                        ],

                        "thumbnail": {"url": f"{self.img}"},

                        "footer": {
                            "text": "Dori Dadon Shoes Monitor",
                        },
                    }
                ],
            )
