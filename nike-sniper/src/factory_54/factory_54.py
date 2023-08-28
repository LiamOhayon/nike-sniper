from bs4 import BeautifulSoup
import requests
import json

from ..utils import get_urls, get_stored_sizes, check_for_updates
from ..Shoe import Shoe
from ..factory_54.scrape_functions import get_sizes


"""
SITE ALGORITHM STARTS HERE

SITE NAME: Factory 54
"""

factory_api = "https://www.factory54.co.il/on/demandware.store/Sites-factory54-Site/iw_IL/Product-Variation?pid="


def get(url: list, keywords: list):

    start_param = 0
    for i in range(15):

        urls = get_urls("factory_54")

        content = requests.get(f"{url}{str(start_param)}").content
        soup = BeautifulSoup(content, 'html.parser')
        product_parents = soup.find_all('div', class_='present-product product also-like__img')

        for product_children in product_parents:
            name = f"""{json.loads(product_children.get("data-gtm-product"))["item_name"]} {json.loads(product_children.get("data-gtm-product"))["item_brand"]} {json.loads(product_children.get("data-gtm-product"))["item_variant"]}"""
            price = json.loads(product_children.get("data-gtm-product"))["price"]
            image = product_children.find('img', class_='tile-image also-like__img--tile primary-image').get('src')
            p_url = f"https://www.factory54.co.il{product_children.find('a', class_='link tile-body__product-name').get('href')}"
            id = product_children.get('data-pid')
            for keyword in keywords:
                if keyword in name.lower():
                    sec_content = requests.get(f"{factory_api}{id}").content
                    sizes = get_sizes(sec_content)
                    shoe = Shoe("factory_54", name, p_url, price, image, sizes)

                    if p_url not in urls:
                        shoe.discord_message()
                        shoe.update()
                        urls.append(shoe.url)

                    else:
                        check_for_updates(sizes, get_stored_sizes(shoe.site, shoe.url), shoe)

                    start_param += 48
